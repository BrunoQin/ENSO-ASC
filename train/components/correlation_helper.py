import numpy as np

from scipy.stats import pearsonr


def correlation_helper(y_predict, y_real):
    print("create nested numpy array list...")
    lst_np_ras = []
    for i in range(12):
        lst_np_ras.append([y_predict[i], y_real[i]])

    print("read props numpy data...")
    ras_np = lst_np_ras[0][0]
    rows = ras_np.shape[0]
    cols = ras_np.shape[1]

    print("create output numpy array...")
    ras_np_res_corr = np.ndarray((rows, cols))
    ras_np_res_pear = np.ndarray((rows, cols))
    print(" - out rows:", ras_np_res_corr.shape[0])
    print(" - out cols:", ras_np_res_corr.shape[1])

    print("loop through pixels...")
    pix_cnt = 0
    count = 0
    for row in range(rows):
        for col in range(cols):
            pix_cnt += 1
            if pix_cnt % 5000 == 0:
                print(" - row:", row, "  col:", col, "  pixel:", pix_cnt)
            lst_vals1 = []
            lst_vals2 = []
            try:
                for lst_pars in lst_np_ras:
                    lst_vals1.append(lst_pars[0][row, col])
                    lst_vals2.append(lst_pars[1][row, col])
                # perform calculation on list
                correlation = calculate_correlation(lst_vals1, lst_vals2)
                ras_np_res_corr[row, col] = correlation
                if correlation >= 0.9:
                    count += 1
                pearson = calculate_pearsons(lst_vals1, lst_vals2)
                ras_np_res_pear[row, col] = pearson
            except Exception as e:
                print("ERR:", e)
                print(" - row:", row, "  col:", col, "  pixel:", pix_cnt)
                print(" - lst_vals1:", lst_vals1)
                print(" - lst_vals2:", lst_vals2)

    return ras_np_res_corr, ras_np_res_pear


def calculate_correlation(a, b):
    coef = np.corrcoef(a, b)
    return coef[0][1]


def calculate_pearsons(a, b):
    x = np.array(a)
    y = np.array(b)
    r, p = pearsonr(a, y)
    return p
