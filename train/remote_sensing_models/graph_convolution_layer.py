import numpy as np
import tensorflow as tf


def dense_to_sparse(m):
    mask = tf.math.not_equal(m, 0)
    return tf.sparse.SparseTensor(
        indices = tf.where(mask),
        values = tf.boolean_mask(m, mask),
        dense_shape = m.shape)

def ChebyshevPolynomials(adj, max_degree=3):
    assert type(max_degree) is int
    assert adj.dtype == tf.float32
    tf.debugging.Assert(tf.equal(tf.shape(tf.shape(adj))[0], 2), [adj])
    tf.debugging.Assert(tf.equal(tf.shape(adj)[0], tf.shape(adj)[1]), [adj])
    if type(adj) is not tf.sparse.SparseTensor:
        adj_sparse = dense_to_sparse(adj)
    else:
        adj_sparse = adj
    # 1) get graph laplacian matrix
    # d_mat_inv_sqrt = D^{-1/2}
    rowsum = tf.sparse.reduce_sum(adj_sparse, axis=1, output_is_sparse=True)
    d_inv_sqrt = tf.sparse.SparseTensor(
        indices = rowsum.indices,
        values = tf.math.pow(rowsum.values, -0.5),
        dense_shape = rowsum.dense_shape)
    mask = tf.math.logical_not(tf.math.is_inf(d_inv_sqrt.values)) # leave non-inf values
    d_inv_sqrt = tf.sparse.SparseTensor(
        indices = tf.boolean_mask(d_inv_sqrt.indices, mask),
        values = tf.boolean_mask(d_inv_sqrt.values, mask),
        dense_shape = d_inv_sqrt.dense_shape)
    d_mat_inv_sqrt = tf.sparse.SparseTensor(
        indices = tf.concat([d_inv_sqrt.indices, d_inv_sqrt.indices], axis=-1),
        values = d_inv_sqrt.values,
        dense_shape = tf.concat([d_inv_sqrt.dense_shape, d_inv_sqrt.dense_shape], axis=0))
    # normalized_adj = D^{-1/2} * A * D^{-1/2}
    normalized_adj = dense_to_sparse(
        tf.sparse.sparse_dense_matmul(
            d_mat_inv_sqrt,
            tf.transpose(
                tf.sparse.sparse_dense_matmul(d_mat_inv_sqrt, tf.sparse.to_dense(adj_sparse), True, True))))
    # laplacian = I - D^{-1/2} * A * D^{-1/2}
    laplacian = tf.sparse.add(tf.sparse.eye(tf.shape(normalized_adj)[0]), normalized_adj.__mul__(-1))
    # 2) get scaled graph laplacian matrix
    # scaled_laplacian = 2/lambda_max * laplacian - I
    e = tf.math.reduce_max(tf.linalg.eigvalsh(tf.sparse.to_dense(laplacian)))
    scaled_laplacian = tf.sparse.add(laplacian.__mul__(2. / e), tf.sparse.eye(tf.shape(normalized_adj)[0]).__mul__(-1))
    # 3) get chebyshev polynomial sequences
    # t_k(i) = T_i(scaled_laplacian)
    t_k = list()
    t_k.append(tf.sparse.eye(tf.shape(normalized_adj)[0]))
    t_k.append(scaled_laplacian)
    for i in range(2, max_degree + 1):
        m = tf.sparse.add(
            dense_to_sparse(tf.sparse.sparse_dense_matmul(scaled_laplacian, tf.sparse.to_dense(t_k[i-1]))).__mul__(2),
            t_k[i-2].__mul__(-1))
        t_k.append(m)
    return t_k

class GraphConvolution(tf.keras.layers.Layer):
    def __init__(self, filters=None, supports=None, dropout_rate=0., use_bias=True, activation=None, adj=None, max_degree=3, **kwargs):

        assert type(filters) is int and 0 < filters
        assert type(dropout_rate) is float and 0 <= dropout_rate < 1
        assert type(supports) is list
        assert tf.math.reduce_all([type(support) is tf.sparse.SparseTensor and tf.shape(tf.shape(support))[0] == 2 for support in supports])
        self.filters = filters # Dout
        self.dropout_rate = dropout_rate
        self.use_bias = use_bias
        self.activation = activation
        if supports is not None:
            self.supports = supports
        else:
            assert adj is not None
            assert type(max_degree) is int
            self.supports = ChebyshevPolynomials(adj, max_degree=max_degree)
        super(GraphConvolution, self).__init__(**kwargs)

    def build(self, input_shape):
        self.kernel = [self.add_weight(name='kernel' + str(i), shape=(input_shape[-1], self.filters), initializer=tf.keras.initializers.GlorotUniform(), trainable=True) for i in range(len(self.supports))]
        if self.use_bias:
            # self.bias.shape = (Dout)
            self.bias = self.add_weight(name='bias', shape=(self.filters,), initializer=tf.keras.initializers.Zeros(), trainable=True)

    def call(self, inputs):
        if type(inputs) is tf.sparse.SparseTensor:
            random = tf.keras.layers.Lambda(lambda x, y: (1 - y) + tf.random.uniform(tf.shape(x)), arguments={"y": self.dropout_rate})(inputs)
            mask_indices = tf.keras.layers.Lambda(lambda x: tf.where(tf.gather_nd(tf.math.greater_equal(x[0], 1),x[1].indices)))([random, inputs])
            results = tf.keras.layers.Lambda(lambda x: tf.sparse.SparseTensor(indices=tf.gather_nd(x[0].indices, x[1]), values=tf.gather_nd(x[0].values, x[1]), dense_shape=x[0].dense_shape))([inputs, mask_indices])
            results = tf.keras.layers.Lambda(lambda x, y: x / (1 - y), arguments={"y": self.dropout_rate})(results)
        else:
            results = tf.keras.layers.Dropout(self.dropout_rate)(inputs)
        # graph convolution
        outputs = list()
        for i in range(len(self.supports)):
            # res.shape = (batch, N, Dout)
            if type(results) is tf.sparse.SparseTensor:
                res = tf.keras.layers.Lambda(lambda x: tf.sparse.sparse_dense_matmul(x[0], x[1]))([results, self.kernel[i]])
            else:
                res = tf.keras.layers.Lambda(lambda x: tf.linalg.matmul(x[0], x[1]))([results, self.kernel[i]])
            # res.shape = (batch, N, Dout)
            res = tf.keras.layers.Lambda(lambda x: tf.map_fn(lambda y: tf.sparse.sparse_dense_matmul(self.supports[i], y), x))(res)
            outputs.append(res)
        # results.shape = (batch, N, Dout)
        results = tf.keras.layers.Add()(outputs)
        if self.use_bias:
            results = tf.keras.layers.Lambda(lambda x: x[0] + x[1])([results, self.bias])
        if self.activation is not None:
            results = self.activation(results)
        return results

    def get_config(self):
        config = {
            'filters': self.filters,
            'supports': self.supports,
            'dropout_rate': self.dropout_rate,
            'use_bias': self.use_bias,
            'activation': self.activation,
            'adj': self.adj,
            'max_degree': self.max_degree
        }
        base_config = super(GraphConvolution, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))

    @classmethod
    def from_config(cls, config):
        return cls(**config)
