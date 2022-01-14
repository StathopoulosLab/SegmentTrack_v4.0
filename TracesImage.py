"""This function generates traces image.

Given an anlysis folder as input, this class
organizes traces into a image with colormap
for intensity. It is possible to load more 
than one analysis folder, traces will be 
pooled togheter. Inout is a list. 
"""


import numpy as np
from xlrd import open_workbook
from skimage.color import label2rgb
from scipy.signal import medfilt
import pyqtgraph as pg
from PyQt5.QtWidgets import QGraphicsLineItem
from PyQt5 import QtCore, QtWidgets

import SpotsFilter



class TracesImage:
    """Only class, does all the job"""
    def __init__(self, folderpaths):

        mmap         =  np.zeros((11, 3))               # define colormap
        mmap[0, :]   =  [50, 25, 50]
        mmap[1, :]   =  [100, 50, 100]
        mmap[2, :]   =  [150, 100, 150]
        mmap[3, :]   =  [175, 125, 175]
        mmap[4, :]   =  [75, 0, 0]
        mmap[5, :]   =  [100, 0, 0]
        mmap[6, :]   =  [125, 0, 0]
        mmap[7, :]   =  [200, 200, 0]
        mmap[8, :]   =  [220, 220, 0]
        mmap[9, :]   =  [250, 250, 0]
        mmap[10, :]  =  [255, 255, 255]

        mmap_lut  =  np.zeros((11, 1, 3))                # popup a figure with the lut
        for gg in range(11):
            mmap_lut[gg]  =  mmap[gg]
        pg.image(mmap_lut, title="LookUpTable")

        traces_tot  =  []

        pbar  =  QtWidgets.QProgressBar()
        pbar.setRange(0, 0)
        pbar.show()


        for ff in range(len(folderpaths)):
            wb_cbd  =  open_workbook(folderpaths[ff] + '/ComprehensiveBurstingData.xls')
            s_cbd   =  wb_cbd.sheets()[0]

            col_tags   =  s_cbd.col_values(0)
            tags_list  =  []
            for tag in col_tags:
                if tag[:4] == "Nuc_":
                    tags_list.append(int(tag[4:]))                              # reads all the nuclei tags from the xls file
            
            wb_j  =  open_workbook(folderpaths[ff] + '/journal.xls')
            s_j   =  wb_j.sheets()[0]

            s_j_start  =  0
            while s_j.col(s_j_start)[0].value[:4] != "Spot":
                s_j_start  +=  1

            s_j_steps  =  1
            while s_j.col(s_j_start)[s_j_steps].value != "":
                s_j_steps  +=  1

            traces_sing  =  []
            for tag in tags_list:
                QtCore.QCoreApplication.processEvents()
                # print(tag)
                s_j_tag  =  0
                while s_j.col(s_j_tag)[0].value[5:] != str(tag):
                    s_j_tag  +=  1
                trace  =  []
                for k in range(1, s_j_steps):
                    trace.append(int(s_j.col(s_j_tag)[k].value))
                traces_sing.append(trace)

                
            traces_sing  =  np.transpose(np.asarray(traces_sing))
            traces_tot.append(traces_sing)

        trace_length  =  1000000
        for nn in range(len(folderpaths)):
            QtCore.QCoreApplication.processEvents()
            trace_length  =  np.min((trace_length, traces_tot[nn].shape[0]))

        for pp in range(len(folderpaths)):
            traces_tot[pp]  =  traces_tot[pp][:trace_length, :]

        traces  =  traces_tot[0]
        for yy in range(1, len(folderpaths)):
            traces  =  np.concatenate((traces, traces_tot[yy]), axis=1)


        for j in range(traces.shape[1]):
            prof           =  np.sign(traces[:, j])
            prof_f         =  SpotsFilter.SpotsFilter(prof, np.array([int(s_cbd.col(1)[9].value), int(s_cbd.col(1)[10].value)])).prof_f              # filtering appends here, on the binary series
            traces[:, j]  *=  prof_f

        traces_flt  =  np.zeros(traces.shape)
        for kk in range(traces.shape[1]):
            traces_flt[:, kk]  =  medfilt(traces[:, kk], 3)

        traces_ord  =  np.zeros(traces.shape, dtype=np.int)
        j           =  0
        j_ord       =  0
        while traces_flt.sum() != 0:
            while len(np.where(traces_flt[j, :] != 0)[0]) == 0:
                j  +=  1

            idx                    =  np.where(traces_flt[j, :] != 0)[0][0]
            traces_ord[:, j_ord]   =  traces_flt[:, idx]
            traces_flt[:, idx]     =  0
            j_ord                 +=  1

        traces2plot   =  11 * traces_ord / traces_ord.max()
        traces2plot2  =  np.zeros((traces2plot.shape[0], 2 * traces2plot.shape[1]))
        for k in range(traces2plot.shape[1]):
            traces2plot2[:, 2 * k]      =  traces2plot[:, k]
            traces2plot2[:, 2 * k + 1]  =  traces2plot[:, k]


        traces2plot2_3c  =  label2rgb(traces2plot2, bg_label=0, bg_color=[0, 0, 0], colors=mmap)

        coords  =  []
        for cc in range(traces2plot.shape[1] - 1):
            try:
                coords.append([np.where(traces2plot2[:, 2 * cc] != 0)[0][0], 1 + 2 * cc])
            except IndexError:
                pass
                
        coords  =  np.asarray(coords)
        coefs   =  np.polyfit(coords[:, 0], coords[:, 1], 5)
        p       =  np.poly1d(coefs)
        vec     =  []
        for x in coords[:, 0]:
            vec.append(p(x))

        if vec[0] < 0:
            vec  +=  np.abs(vec[0])

        w  =  pg.image(traces2plot2_3c)
        for k in range(len(vec) - 2):
            bff  =  QGraphicsLineItem(coords[k, 0] + 2, vec[k], coords[k + 1, 0] + 2, vec[k + 1])
            bff.setPen(pg.mkPen('w', width=2, style=QtCore.Qt.DashLine))
            w.addItem(bff)
            bff  =  QGraphicsLineItem(coords[k + 1, 0] + 2, vec[k + 1], coords[k + 2, 0] + 2, vec[k + 2])
            bff.setPen(pg.mkPen('w', width=2, style=QtCore.Qt.DashLine))
            w.addItem(bff)

        w2  =  pg.image(traces2plot2_3c)
        pbar.close()

        self.traces2plot2_3c  =  traces2plot2_3c
        self.traces2plot2     =  traces2plot2
        self.mmap             =  mmap
        self.mmap_lut         =  mmap_lut




# class ProgressBar(QtGui.QWidget):
#     """Simple progressbar widget"""
#     def __init__(self, parent=None, total1=20):
#         super(ProgressBar, self).__init__(parent)
#         self.name_line1  =  QtGui.QLineEdit()

#         self.progressbar1  =  QtWidgets.QProgressBar()
#         self.progressbar1.setMinimum(1)
#         self.progressbar1.setMaximum(total1)

#         main_layout  =  QtGui.QGridLayout()
#         main_layout.addWidget(self.progressbar1, 0, 0)

#         self.setLayout(main_layout)
#         self.setWindowTitle("Progress")
#         self.setGeometry(500, 300, 300, 50)

#     def update_progressbar(self, val1):
#         self.progressbar1.setValue(val1)
#         QtWidgets.qApp.processEvents()
