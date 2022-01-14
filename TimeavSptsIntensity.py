"""This function prepares data for the 'SpotsTimeAverage' tool.EnginioClient

Starting from the analysis folder (excel files written) it generates the 
activation profile that is the input of the tool.
"""


import numpy as np
from xlrd import open_workbook
from PyQt5 import QtGui, QtWidgets


class TimeavSptsIntensity:
    "Main class, does all the job"
    def __init__(self, foldername):

        wb_bybkg    =  open_workbook(foldername + '/SpotsIntensityDividedByBackground.xls')
        s_wb_bybkg  =  wb_bybkg.sheets()[0]

        wb_spat    =  open_workbook(foldername + '/ComprehensiveBurstingData.xls')
        s_wb_spat  =  wb_spat.sheets()[0]

        wb_journal    =  open_workbook(foldername + '/journal.xls')
        s_wb_journal  =  wb_journal.sheets()[0]

        row_start  =  0
        while str(s_wb_spat.col(0)[row_start].value) != "Nuclei ID":
            row_start  +=  1
        
        spt_ids  =  []
        j        =  row_start + 1
        while str(s_wb_spat.col(0)[j].value)[:4] == "Nuc_":
            spt_ids.append(str(s_wb_spat.col(0)[j].value)[4:])
            j  +=  1

        col_coords  =  []
        for k in spt_ids:
            for l in range(s_wb_bybkg.ncols):
                if str(s_wb_bybkg.col(l)[0].value)[6:] == k:
                    col_coords.append(l)

        t_steps     =  s_wb_bybkg.nrows - 1
        spots_vals  =  np.zeros((t_steps, len(col_coords)))

        pbar  =  ProgressBar(total1=len(col_coords))
        pbar.show()

        for r in range(len(col_coords)):
            pbar.update_progressbar(r)
            for t in range(t_steps):
                spots_vals[t, r]  =  np.float(s_wb_bybkg.col(col_coords[r])[t + 1].value)

        pbar.close()

        self.spots_vals  =  spots_vals
        self.t_step      =  float(s_wb_journal.col(1)[11].value)
        self.time_zero   =  int(s_wb_journal.col(1)[14].value)




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
