"""This function writes the activation curve into the cropped region.

An excell file is written inside the analysis folder in which you have both the
instantaneous activation curve and the cumulativative activation curve. This
data are extracted after filtering. As input it takes some output from
ComprehensiveBurstAnalysisWriter in order to not calculate the same things
twice.
"""

import datetime
import numpy as np
import xlsxwriter
from skimage.morphology import label
from PyQt5 import QtWidgets

import SpotsFilter


class ComprehensiveActivationWriter:
    """Only class, does all the job"""
    def __init__(self, foldername, nucs_trk, spots_trk, idxs_in, filter_set, pix_size, coords2write, numb_nucs_area, time_step_value, time_zero):

        pbar  =  ProgressBar(total1=idxs_in.size * 2 + nucs_trk.shape[0])
        pbar.show()
        pbar_idx  =  1

        nucs_selected  =  np.zeros(nucs_trk.shape)
        for k in idxs_in:
            pbar.update_progressbar(pbar_idx)
            pbar_idx  +=  1

            nucs_selected  +=  k * (nucs_trk == k)

        nucs_segm  =  np.zeros(nucs_trk.shape)
        for t in range(nucs_trk.shape[0]):
            pbar.update_progressbar(pbar_idx)
            pbar_idx  +=  1

            nucs_segm[t, :, :]  =  label(nucs_selected[t, :, :], connectivity=1)

        nucs_act_prof  =  np.zeros((idxs_in.size, nucs_trk.shape[0]))
        for i in range(idxs_in.size):
            pbar.update_progressbar(pbar_idx)
            pbar_idx  +=  1

            profile              =  np.sign((spots_trk == idxs_in[i]).sum(2).sum(1))
            nucs_act_prof[i, :]  =  SpotsFilter.SpotsFilter(profile, filter_set).prof_f

        nucs_act_cum  =  np.zeros(nucs_trk.shape[0])
        for k in range(nucs_act_prof.shape[0]):
            nucs_act_cum  +=  np.sign(np.cumsum(nucs_act_prof[k, :]))

        book      =  xlsxwriter.Workbook(foldername + '/ComprehensiveActivationData.xlsx')
        sheet1    =  book.add_worksheet("Sheet 1")

        sheet1.write(0, 0, 'FOLDER NAME')
        sheet1.write(0, 1, foldername)

        sheet1.write(1, 0, 'Tot Nucs Numb')
        sheet1.write(1, 1, numb_nucs_area)

        sheet1.write(2, 0, 'Region')
        sheet1.write(3, 0, 'X1')
        sheet1.write(4, 0, 'X2')
        sheet1.write(5, 0, 'Y1')
        sheet1.write(6, 0, 'Y2')

        sheet1.write(3, 1, coords2write[0])
        sheet1.write(4, 1, coords2write[1])
        sheet1.write(5, 1, coords2write[2])
        sheet1.write(6, 1, coords2write[3])

        sheet1.write(8, 0, "Filter Parameters")
        sheet1.write(9, 0, "Zeros")
        sheet1.write(10, 0, "Ones")
        sheet1.write(9, 1, float(filter_set[0]))
        sheet1.write(10, 1, float(filter_set[1]))
        sheet1.write(11, 0, "Pix Size")
        sheet1.write(11, 1, pix_size)

        sheet1.write(0, 6, "Time")
        sheet1.write(0, 7, "Frame")
        sheet1.write(0, 8, "Active Nucs")
        sheet1.write(0, 9, "Cumulative Active Nucs")

        sheet1.write(12, 0, "Date")
        sheet1.write(12, 1, datetime.datetime.now().strftime("%d-%b-%Y"))

        for t in range(nucs_trk.shape[0]):
            sheet1.write(t + 1, 6, (time_zero + t) * time_step_value)
            sheet1.write(t + 1, 7, t)
            sheet1.write(t + 1, 8, nucs_act_prof[:, t].sum())
            sheet1.write(t + 1, 9, nucs_act_cum[t])

        book.close()
        pbar.close()


class ProgressBar(QtWidgets.QWidget):
    """Simple Progressbar widget"""
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

    def update_progressbar(self, val1):
        """Progressbar updater"""
        self.progressbar1.setValue(val1)
        QtWidgets.qApp.processEvents()
