import tensorflow as tf


class Loss(tf.keras.Model):

    def __init__(self, model):
        super(Loss, self).__init__()
        self.model = model

    def call(self, inputs):
        loss = 0
        # for variable in self.model.trainable_variables:
        #     loss += 5e-4 * tf.nn.l2_loss(variable)
        # loss_reg = loss

        ssim = tf.image.ssim(inputs[0], inputs[1], max_val=1)
        loss_ssim = tf.reduce_mean((1.0 - ssim)/2)
        loss += 9 * loss_ssim

        l2_loss = tf.reduce_mean(tf.square(inputs[0] - inputs[1]))
        loss_l2 = l2_loss
        loss += 7 * l2_loss

        l1_loss = tf.reduce_mean(tf.abs(inputs[0] - inputs[1]))
        loss_l1 = l1_loss
        loss += l1_loss

        return loss_ssim, loss_l2, loss_l1, loss
