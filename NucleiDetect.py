"""This function  thresholds raw data to deetct nuclei.

It uses the Ostu adaptive thresholding algorithm.
"""


import numpy as np
from skimage.morphology import label
from skimage import filters
from scipy import ndimage
from scipy.ndimage.morphology import binary_dilation
from scipy.ndimage.morphology import binary_erosion

from PyQt5 import QtWidgets


class NucleiDetect:
    """Only class, does all the job"""
    def __init__(self, nucleiMatx, gauss_filter_size):

        nucleiMatxSM  =  np.zeros(nucleiMatx.shape)
        steps, xlen   =  nucleiMatx.shape[:2]

        for t in range(steps):
            nucleiMatxSM[t, :, :] = filters.gaussian(nucleiMatx[t, :, :], gauss_filter_size)        # presmoothing

        im_seg = np.zeros(nucleiMatxSM.shape)

        block_size  =  xlen / 5                                                                     # for adaptive thresholding
        if block_size % 2 == 0:
            block_size  +=  1

        for t in range(steps):
            val              =  filters.threshold_local(nucleiMatxSM[t, :, :], block_size)          # otsu
            im_seg[t, :, :]  =  nucleiMatxSM[t, :, :] > val                                         # thresholdig

        im_segO    =  np.zeros(im_seg.shape)
        im_segOC   =  np.zeros(im_seg.shape)
        nucs_fin   =  np.zeros(im_seg.shape)
        nucs_fsm   =  np.zeros(im_seg.shape)

        for k in range(im_segO[:, 0, 0].size):
            im_segO[k, :, :] = ndimage.morphology.binary_opening(im_seg[k, :, :])

        for k in range(im_segO[:, 0, 0].size):
            im_segOC[k, :, :] = ndimage.morphology.binary_closing(im_segO[k, :, :])

        pbar  =  ProgressBar(total1=steps)
        pbar.update_progressbar(0)
        pbar.show()

        for tt in range(steps):
            pbar.update_progressbar(tt)
            nucs_fin[tt, :, :]  =  binary_erosion(im_segOC[tt, :, :], iterations=3)                   # from here on is just to smooth nuclei borders
            nucs_fin[tt, :, :]  =  binary_dilation(nucs_fin[tt, :, :], iterations=4)
            nucs_fsm[tt, :, :]  =  filters.median(nucs_fin[tt, :, :], np.ones((7, 7)))
            nucs_fsm[tt, :, :]  =  label(nucs_fsm[tt, :, :], connectivity=1)

        pbar.close()
        self.labbs   =  nucs_fsm.astype(np.int32)


class ProgressBar(QtWidgets.QWidget):
    """Simple progressbar widget"""
    def __init__(self, total1=20):
        super().__init__()
        self.name_line1  =  QtWidgets.QLineEdit()

        self.progressbar1  =  QtWidgets.QProgressBar()
        self.progressbar1.setMinimum(1)
        self.progressbar1.setMaximum(total1)

        main_layout  =  QtWidgets.QGridLayout()
        main_layout.addWidget(self.progressbar1, 0, 0)

        self.setLayout(main_layout)
        self.setWindowTitle("Progress")
        self.setGeometry(500, 300, 300, 50)

    def update_progressbar(self, val1):
        """Update progressbar"""
        self.progressbar1.setValue(val1)
        QtWidgets.qApp.processEvents()

