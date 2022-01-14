"""This function removes the nuclei on the border.

Given a time series of already tracked nuclei, this function check the nuclei that
appear even ones on the border of the images and removes them.

"""


import numpy as np
from skimage.morphology import remove_small_objects
from PyQt5 import QtWidgets


class RemoveBorderNuclei:
    def __init__(self, nuclei_tracked, px_brd):

        mask                                     =  np.ones(nuclei_tracked.shape, dtype='uint16')        # B&W matrix, having 1 on the border (px_brd thick)
        mask[:, px_brd:-px_brd, px_brd:-px_brd]  =  0
        idxs_rmv                                 =  np.unique(mask * nuclei_tracked)[1:]                 # multiplication of the matrix with image to have the indexes of the nuclei touching the border

        pbar  =  ProgressBar(total1=idxs_rmv.size)
        pbar.show()
        pbar_idx  =  1

        for k in idxs_rmv:
            pbar.update_progressbar1(pbar_idx)
            pbar_idx       +=  1
            nuclei_tracked  *=  (1 - (nuclei_tracked == k)).astype('bool')                                                  # removal of all these nuclei

        pbar.close()    

        self.nuclei_tracked         =  nuclei_tracked


class RemoveSmallNuclei:
    def __init__(self, nuclei_tracked, area_thr):

        steps        =  nuclei_tracked.shape[0]
        nuclei_thrd  =  np.zeros_like(nuclei_tracked)

        for t in range(steps):
            nuclei_thrd[t]  =  remove_small_objects(nuclei_tracked[t], area_thr)

        self.nuclei_thrd  =  nuclei_thrd


class ProgressBar(QtWidgets.QWidget):
    def __init__(self, parent=None, total1=20):
        super().__init__(parent)
        self.name_line1  =  QtWidgets.QLineEdit()

        self.progressbar1  =  QtWidgets.QProgressBar()
        self.progressbar1.setMinimum(1)
        self.progressbar1.setMaximum(total1)

        main_layout  =  QtWidgets.QGridLayout()
        main_layout.addWidget(self.progressbar1, 0, 0)

        self.setLayout(main_layout)
        self.setWindowTitle("Progress")
        self.setGeometry(500, 300, 300, 50)


    def update_progressbar1(self, val1):
        self.progressbar1.setValue(val1)
        QtWidgets.qApp.processEvents()



# class ProgressBar(QtGui.QWidget):
#     def __init__(self, parent=None, total1=20):
#         super(ProgressBar, self).__init__(parent)
#         self.name_line1  =  QtGui.QLineEdit()

#         self.progressbar1  =  QtWidgets.QProgressBar()
#         self.progressbar1.setMinimum(1)
#         self.progressbar1.setMaximum(total1)

#         self.progressbar2  =  QtWidgets.QProgressBar()
#         self.progressbar2.setMinimum(1)

#         main_layout  =  QtGui.QGridLayout()
#         main_layout.addWidget(self.progressbar1, 0, 0)
#         main_layout.addWidget(self.progressbar2, 1, 0)

#         self.setLayout(main_layout)
#         self.setWindowTitle("Progress")
#         self.setGeometry(500, 300, 300, 50)


#     def update_progressbar1(self, val1):
#         self.progressbar1.setValue(val1)
#         QtWidgets.qApp.processEvents()


#     def update_progressbar2(self, val2):
#         self.progressbar2.setValue(val2)
#         QtWidgets.qApp.processEvents()


#     def pbar2_setmax(self, total2):
#         self.progressbar2.setMaximum(total2)
