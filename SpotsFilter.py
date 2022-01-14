"""This function filters binary individual spots series.

Given the binary time series of a spot, this function removes FIRST series of 'k_zeros'
zeros surrounded by ones and than series of 'k_ones' ones surrounded by zeros.
"""


import numpy as np
from skimage.morphology import label


class SpotsFilter:
    def __init__(self, prof, filter_set):

        prof2      =  np.copy(prof)
        prof2_neg  =  1 - prof2

        prof_neg_lbl  =  label(prof2_neg)

        for l in np.unique(prof_neg_lbl)[1:]:
            if np.sum(prof_neg_lbl == l).sum() <= filter_set[0]:
                prof2_neg  *=  1 - (prof_neg_lbl == l)

        prof2  =  1 - prof2_neg

        prof_lbls  =  label(prof2)

        for l in range(1, prof_lbls.max() + 1):
            if np.sum(prof_lbls == l) <= filter_set[1]:
                prof2  *=  1 - (prof_lbls == l)

        part_sum  =  0                                                          # the last consecutive zeros (if there are) of the serie are kept
        j_sum     =  0
        while part_sum == 0 and j_sum < filter_set[0]:
            j_sum     +=  1
            part_sum  =   prof[-j_sum:].sum()

        if part_sum == 0:
            prof2[-j_sum:]  =  prof[-j_sum:]

        self.prof_f  =  prof2




# prof  =  np.sign((spots == k).sum(2).sum(1))
# prof_f = SpotsFilter.SpotsFilter(prof, 2, 2).prof_f
# w = pg.plot(prof, symbol='s')
# w.plot(prof_f, symbol='x', pen='r')
