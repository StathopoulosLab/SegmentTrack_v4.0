"""This function loads analysis and prepares
matrices for the single nuclei inspection.
"""
import numpy as np


class VisualNucSpot:
    def __init__(self, nucs, raw_red, spts, raw_sp, tag):

        spt_sing   =  raw_sp * (spts == tag)
        spts_prof  =  spt_sing.sum(2).sum(1)

        msk                =  nucs == tag
        mtx3c              =  np.zeros(np.append(nucs.shape, 3))
        mtx3c[:, :, :, 0]  =  (raw_red * (1 - msk)) / 2 + raw_red * msk
        mtx3c[:, :, :, 1]  =  raw_red * (1 - msk) / 2
        mtx3c[:, :, :, 2]  =  raw_red * (1 - msk) / 2

        spt_sing_enhances  =  mtx3c[:, :, :, 0].max() * spt_sing / float(spt_sing.max())
        mtx3c[:, :, :, 0]  *=  (1 - np.sign(spt_sing))
        mtx3c[:, :, :, 1]  *=  (1 - np.sign(spt_sing))
        mtx3c[:, :, :, 2]  *=  (1 - np.sign(spt_sing))
        mtx3c[:, :, :, 1]  +=  spt_sing_enhances

        self.mtx3c      =  mtx3c
        self.spts_prof  =  spts_prof


class IntensityMaximum:
    def __init__(self, spts, raw_sp):

        spts_tags  =  np.unique(spts)[1:]
        ints       =  np.zeros((spts_tags.size, spts.shape[0]))

        for k in range(spts_tags.size):
            ints[k, :]  =  (raw_sp * (spts == spts_tags[k])).sum(2).sum(1)

        self.int_max  =  ints.max()
