"""This function tracks nuclei.

Starting from a time series of already detected and segmented nuclei,
it tracks them using the positions of the center of mass of nuclei in consecutive
time frames. The closest are associated. There is a threshold on the distance to
avoid misleading associations.
"""


import numpy as np
from skimage.measure import regionprops
from importlib import reload

import NucleiConnectSingle


class NucleiConnect:
    def __init__(self, input_args):
        nuclei    =  input_args[0].astype(np.int32)
        dist_thr  =  input_args[1]
        reload(NucleiConnectSingle)
        t_tot  =  nuclei.shape[0]
        ctrs   =  np.zeros((t_tot, 2, nuclei.max()))

        for tt in range(t_tot):
            # rgp    =  regionprops(nuclei[tt, :, :].astype(np.int))
            rgp    =  regionprops(nuclei[tt, :, :])
            for j in range(len(rgp)):
                if nuclei[tt, np.round(rgp[j]['Centroid'][0]).astype(np.int), np.round(rgp[j]['Centroid'][1]).astype(np.int)] > 0:
                    ctrs[tt, :, j]  =  rgp[j]['Centroid']
                else:
                    bff_square  =  nuclei[tt, np.round(rgp[j]['Centroid'][0]).astype(np.int) - 1:np.round(rgp[j]['Centroid'][0]).astype(np.int) + 2, np.round(rgp[j]['Centroid'][1]).astype(np.int) - 1:np.round(rgp[j]['Centroid'][1]).astype(np.int) + 2]

                    bff_square  =  np.unique(bff_square)
                    bff_square  =  np.trim_zeros(bff_square)

                    if bff_square > 0:
                        nuclei[tt, np.round(rgp[j]['Centroid'][0]).astype(np.int), np.round(rgp[j]['Centroid'][1]).astype(np.int)]  =  bff_square
                        ctrs[tt, :, j]  =  rgp[j]['Centroid']

        nuclei_tracked     =  np.zeros(nuclei.shape, dtype=np.int32)

        k  =  0
        while ctrs[:-1, :, :].sum() > 0:
            [t, i_ref]  =  np.argwhere(ctrs.sum(1) != 0)[0]
            bffr_data   =  NucleiConnectSingle.NucleiConnectSingle(ctrs, nuclei, i_ref, t, dist_thr)

            if bffr_data.labbs2.sum() > 0:
                nuclei_tracked  +=  (k + 1) * bffr_data.labbs2
                ctrs            =   bffr_data.ctrs
                k               +=  1

        self.nuclei_tracked         =  nuclei_tracked
