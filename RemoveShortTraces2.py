"""This function recognizes and removes spots with short activation events.

It works on already filtered data.
"""

import numpy as np
from skimage.morphology import label
from scipy.ndimage import median_filter
from PyQt5 import QtGui, QtWidgets



class RemoveShortTraces2:
    def __init__(self, good_tags, min_length, spots_tracked_3d):

        bad_idxs  =  np.array([], dtype=int)

        pbar1   =  ProgressBar.ProgressBar(total1=good_tags.size)
        pbar1.show()

        for k in range(good_tags.size):
            pbar1.update_progressbar(k)
            if np.sign((spots_tracked_3d == good_tags[k]).sum(2).sum(1)).sum() < min_length:                           # check the length for each spot
                bad_idxs  =  np.append(bad_idxs, k)
                # print good_tags[k]

        new_tags  =  np.delete(good_tags, bad_idxs, axis=0)
        pbar1.close()

        pbar2   =  ProgressBar(total1=good_tags.size)
        pbar2.show()

        new_bad_idxs  =  np.array([], dtype=int)

        for k in range(new_tags.size):                                                                                    # check for each selected spots that there are no short chops                                                                                                  
            pbar2.update_progressbar(k)
            prof    =  np.sign((spots_tracked_3d == new_tags[k]).sum(2).sum(1))
            prof_f  =  median_filter(prof, 3)
            prof_l  =  label(prof_f)
            for l in range(1, prof_l.max() + 1):
                if (prof_l == l).sum() < min_length:
                    pts  =  np.where((prof_l == l) == 1)[0]
                    spots_tracked_3d[pts[0]:pts[-1] + 1, :, :]  *=  (1 - (spots_tracked_3d[pts[0]:pts[-1] + 1, :, :] == new_tags[k])).astype('uint16')

            if (spots_tracked_3d == new_tags[k]).sum() == 0:
                new_bad_idxs  =  np.append(new_bad_idxs, k)

        new_tags  =  np.delete(new_tags, new_bad_idxs, axis=0)
        pbar2.close()

        self.spots_tracked_3d  =  spots_tracked_3d
        self.new_tags          =  new_tags



class ProgressBar(QtGui.QWidget):
    def __init__(self, parent=None, total1=20):
        super(ProgressBar, self).__init__(parent)
        self.name_line1  =  QtGui.QLineEdit()

        self.progressbar1  =  QtWidgets.QProgressBar()
        self.progressbar1.setMinimum(1)
        self.progressbar1.setMaximum(total1)

        main_layout  =  QtGui.QGridLayout()
        main_layout.addWidget(self.progressbar1, 0, 0)

        self.setLayout(main_layout)
        self.setWindowTitle("Progress")
        self.setGeometry(500, 300, 300, 50)

    def update_progressbar(self, val1):
        self.progressbar1.setValue(val1)
        QtWidgets.qApp.processEvents()
