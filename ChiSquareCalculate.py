"""This function calculates the chi square for comparison of two different samples: input parameters are
the two series of data and the binning. The output is the chi square and the number of degree of freedom
plus the histogram frequencies"""



import numpy as np


class ChiSquareCalculate:
    def __init__(self, s_one, s_two, bbinn):
        self.s_one  =  s_one
        self.s_two  =  s_two
        self.bbinn  =  bbinn

        y_one, x_one  =  np.histogram(self.s_one, bins=bbinn)                                                           # calculates the histogram frequencies of the series
        y_two, x_two  =  np.histogram(self.s_two, bins=bbinn)

        chisq  = 0
        df     =  0
        k_one  =  np.sqrt(y_one.sum() / y_two.sum().astype(np.float))                                                   # correction factor that takes into account the different sample sizes
        k_two  =  np.sqrt(y_two.sum() / y_one.sum().astype(np.float))

        for b in range(bbinn.size - 1):
            if y_two[b] + y_one[b] > 0:
                chisq  +=  (y_two[b] * k_one - y_one[b] * k_two) ** 2 / (y_two[b] + y_one[b]).astype(np.float)          # chi_square
                df     +=  1

        self.y_one  =  y_one
        self.y_two  =  y_two
        self.chisq  =  chisq
        self.df     =  df
