""" This function organizes visualization of spots traces.

Given the analysis folder, removes border nuclei e prepares the intensity traces of all
the detected spots. It calculates the maximum intensity value to have a common scale
in the plots and the list of all the indexes.
"""

import numpy as np
import xlrd
from PyQt5 import QtGui, QtWidgets
# import RemoveBorderNuclei
# import SpotsFilter


class MultiTracePlotting:
    def __init__(self, folder_name):

        spots_tracked_3d = np.fromfile(folder_name + '/spots_tracked.bin', 'uint16')
        spots_tracked_3d = spots_tracked_3d[3:].reshape((spots_tracked_3d[2], spots_tracked_3d[1], spots_tracked_3d[0]))

        book = xlrd.open_workbook(folder_name + '/ComprehensiveBurstingData.xls')
        sheet1 = book.sheet_by_index(0)

        k_in = 0
        while str(sheet1.col(0)[k_in].value)[:3] != 'Nuc':
            k_in += 1

        for k_fin in range(k_in + 1, sheet1.nrows):
            if str(sheet1.col(0)[k_fin].value)[:3] != 'Nuc':
                k_fin -= 1
                break

        # nuclei_tracked  =  np.fromfile(folder_name + '/nuclei_tracked.bin', 'uint16')
        # nuclei_tracked  =  nuclei_tracked[3:].reshape((nuclei_tracked[2], nuclei_tracked[1], nuclei_tracked[0]))
        # nuclei_tracked  =  RemoveBorderNuclei.RemoveBorderNuclei(nuclei_tracked, 2).nuclei_tracked
        # #
        # tags_spts  =  np.unique(spots_tracked_3d)[1:]
        # tags_nucs  =  np.unique(nuclei_tracked)[1:]
        # tags_list  =  set(list(tags_nucs)).intersection(list(tags_spts))
        # tags_list  =  np.array(list(tags_list))


        tags_list = np.array([], dtype=int)
        for j in range(k_in + 1, k_fin + 1):
            tags_list = np.append(tags_list, int(sheet1.col(0)[j].value[4:]))

        k_flt = 0
        while str(sheet1.col(0)[k_flt].value) != 'Zeros':
            k_flt += 1

        raw_sp  =  np.fromfile(folder_name + '/spots_3D_ints.bin', 'uint16')
        raw_sp  =  raw_sp[3:].reshape((raw_sp[2], raw_sp[1], raw_sp[0]))

        pbar = ProgressBar(total1=tags_list.size)
        pbar.show()

        y_sup = np.zeros(tags_list.size)
        for k in range(y_sup.size):  # calculate the maximum value among the spots intensity traces
            y_sup[k] = (raw_sp * (spots_tracked_3d == tags_list[k])).sum(2).sum(1).max()
            pbar.update_progressbar(k)

        y_sup = y_sup.max()
        pbar.close()

        self.tags_list         =  tags_list
        self.raw_sp            =  raw_sp
        self.spots_tracked_3d  =  spots_tracked_3d
        self.y_sup             =  y_sup



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
