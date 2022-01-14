"""This works on a single frame, with nuclei detected and labeled but not segmented."""


import numpy as np
import skimage.morphology as skmr
from scipy import ndimage
from skimage.measure import regionprops
from skimage.feature import peak_local_max
from skimage import filters
# from skimage.morphology import watershed
from skimage.segmentation import watershed

import CircularityEstimate


class NucleiSegment:
    """Only class, does all the job"""
    def __init__(self, frame1, circ_thr, lmp):
        # self.frame1    =  frame1
        # self.circ_thr  =  circ_thr
        # self.lmp       =  np.int(lmp)

        circ  =  CircularityEstimate.CircularityEstimate(frame1.astype(np.int)).circ
        aa    =  np.where(circ[0, :] > circ_thr)[0]

        frame1_sgm  =  np.zeros(frame1.shape, dtype=np.int32)
        for i in aa:
            frame1_sgm += (frame1 == circ[1, i]).astype(np.int32)

        lbl       =  skmr.label(frame1_sgm, connectivity=1).astype(np.int32)
        left      =  np.sign(frame1) - np.sign(frame1_sgm)
        left_lbl  =  skmr.label(left, connectivity=1).astype(np.int32)
        left      =  np.sign(left_lbl)
        left_er   =  ndimage.morphology.binary_erosion(left)

        distance      =  ndimage.distance_transform_edt(left_er)
        local_maxi    =  peak_local_max(distance, indices=False, footprint=np.ones((lmp, lmp)), labels=skmr.label(left_er))
        local_mx      =  filters.gaussian(local_maxi, 1) > 0
        local_mx_lbl  =  skmr.label(local_mx, connectivity=1).astype(np.int32)
        local_mx_rgp  =  regionprops(local_mx_lbl)
        ctrs_mx       =  np.zeros(frame1.shape)

        for i in range(len(local_mx_rgp)):
            ctrs_mx[np.round(local_mx_rgp[i]['Centroid'][0]).astype(np.int), np.round(local_mx_rgp[i]['Centroid'][1]).astype(np.int)]  =  1

        markers  =  ndimage.label(ctrs_mx)[0]
        labels   =  watershed(-distance, markers, mask=np.sign(left_lbl))

        lbl_fin  =  lbl + (lbl.max() + 1) * np.sign(labels) + labels
        lbl_fin  =  skmr.label(lbl_fin, connectivity=1).astype(np.int32)

        left_left  =  skmr.label(np.sign(frame1) - np.sign(lbl_fin), connectivity=1).astype(np.int32)

        lbl_fin  =  lbl_fin + (lbl_fin.max() + 1) * np.sign(left_left) + left_left
        lbl_fin  =  skmr.remove_small_objects(lbl_fin, 60)

        lbl_fin  =  skmr.label(lbl_fin, connectivity=1).astype(np.int32)

        self.lbl_fin  =  lbl_fin




