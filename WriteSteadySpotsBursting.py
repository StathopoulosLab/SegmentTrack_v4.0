"""This function writes an .xls file with bursting statistics.

It uses the results of the Comprehensive tool, the ComprehensiveBurstingData.xls file
and takes into account the selection of the traces done with MultiPlotShowing tool.
"""

import numpy as np
import xlwt
import xlrd
import datetime
from PyQt5 import QtWidgets


class WriteSteadySpotsBursting:
    """Only class, does all the job"""
    def __init__(self, foldername, fname2write, multi_trace, good_tags, min_length_var):

        book_opn    =  xlrd.open_workbook(foldername + '/ComprehensiveBurstingData.xls')
        sheet1_opn  =  book_opn.sheet_by_index(0)

        def coord_finder(sheet1_opn, str_id):
            k  =  0
            while str(sheet1_opn.col(0)[k].value[4:]) != str_id:
                k  +=  1
            return k

        book    =  xlwt.Workbook(encoding='utf-8')
        sheet1  =  book.add_sheet("Sheet 1")
        sheet1.write(0, 0, 'FOLDER NAME')

        sheet1.write(0, 1, foldername)
        sheet1.write(2, 0, 'Region')
        sheet1.write(3, 0, 'X1')
        sheet1.write(4, 0, 'X2')
        sheet1.write(5, 0, 'Y1')
        sheet1.write(6, 0, 'Y2')
        sheet1.write(3, 1, int(sheet1_opn.col(1)[3].value))
        sheet1.write(4, 1, int(sheet1_opn.col(1)[4].value))
        sheet1.write(5, 1, int(sheet1_opn.col(1)[5].value))
        sheet1.write(6, 1, int(sheet1_opn.col(1)[6].value))

        sheet1.write(8, 0, 'Minimum Length')
        sheet1.write(8, 1, min_length_var)

        sheet1.write(10, 0, 'Nuclei ID')
        sheet1.write(10, 1, 'Integral Amplitude')
        sheet1.write(10, 2, 'Average Amplitude')
        sheet1.write(10, 3, 'Duration')
        sheet1.write(10, 4, 'X coord')
        sheet1.write(10, 5, 'Y coord')

        pbar  =  ProgressBar.ProgressBar(total1=good_tags.size)
        pbar.show()

        for j in range(good_tags.size):
            pbar.update_progressbar(j)
            sheet1.write(11 + j, 0, 'Nuc_' + str(good_tags[j]))
            int_ampl  =  ((multi_trace.spots_tracked_3d == good_tags[j]) * multi_trace.raw_sp).sum()
            duration  =  np.sign((multi_trace.spots_tracked_3d == good_tags[j]).sum(2).sum(1)).sum()
            av_ampl   =  int_ampl / float(duration)
            coord     =  coord_finder(sheet1_opn, str(good_tags[j]))

            sheet1.write(11 + j, 1, float(int_ampl))
            sheet1.write(11 + j, 2, float(av_ampl))
            sheet1.write(11 + j, 3, float(duration))
            sheet1.write(11 + j, 4, sheet1_opn.col(1)[coord].value)
            sheet1.write(11 + j, 5, sheet1_opn.col(2)[coord].value)

        date_format = xlwt.XFStyle()
        date_format.num_format_str = 'dd/mm/yyyy'
        sheet1.write(14 + j, 0, 'date')
        sheet1.write(14 + j, 1, datetime.datetime.now(), date_format)

        book.save(fname2write)
        pbar.close()



class ProgressBar(QtWidgets.QWidget):
    """Simple progress bar widget"""
    def __init__(self, parent=None, total1=20):
        super(ProgressBar, self).__init__(parent)
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
        """Progress bar updater"""
        self.progressbar1.setValue(val1)
        QtWidgets.qApp.processEvents()




