"""This function fits journal data.

Starting from the xls journal files, it performes a fitting on the activation curve
using a gamma function.
"""

import numpy as np
from xlrd import open_workbook
from scipy.optimize import curve_fit
from scipy.stats import gamma
import pyqtgraph as pg
import xlwt


class FromJournal2Fitting:
    def __init__(self, journal_names):

        nucs_active  =  np.zeros((1000, len(journal_names)))
        t_max        =  np.zeros(len(journal_names))

        for j in range(len(journal_names)):
            bfr   =  np.zeros(1000)
            wb    =  open_workbook(journal_names[j])
            s_wb  =  wb.sheets()[0]

            for i in range(1, len(s_wb.col(0))):
                if type(s_wb.row(i)[5].value) == float:
                    bfr[i]  =  s_wb.row(i)[5].value

            bfr                        =  np.trim_zeros(bfr)
            t_max[j]                   =  bfr.size
            nucs_active[:bfr.size, j]  =  bfr

        t_max        =  t_max.min().astype(np.int)
        nucs_active  =  nucs_active[:t_max, :]

        def func(x, ampl, alpha, theta):
            return ampl * gamma.cdf(x, alpha, theta)

        x_vv        =  np.arange(t_max)
        popt, pcov  =  curve_fit(func, x_vv, nucs_active.sum(1))
        # perr        =  np.sqrt(np.diag(pcov))
        y_vv        =  func(x_vv, popt[0], popt[1], popt[2])
        w           =  pg.plot(x_vv, nucs_active.sum(1))
        w.plot(x_vv, y_vv, pen='r')

        half_active  =  np.argmin(np.abs(y_vv - y_vv[-1] / 2))

        # self.nucs_active  =  nucs_active
        self.popt         =  popt
        self.y_vv         =  y_vv
        self.half_active  =  half_active



class WriteResults:
    def __init__(self, filename, journal_names, nucs_active, half_active, popt):

        book    =  xlwt.Workbook(encoding='utf-8')
        sheet1  =  book.add_sheet("Sheet 1")

        sheet1.write(0, 0, 'half active')
        sheet1.write(0, 1, half_active.astype(np.int))

        sheet1.write(2, 0, "Ampl")
        sheet1.write(2, 1, popt[0])
        sheet1.write(3, 0, "alpha")
        sheet1.write(3, 1, popt[1])
        sheet1.write(4, 0, "theta")
        sheet1.write(4, 1, popt[2])

        sheet1.write(6, 0, "File names")
        for j in range(len(journal_names)):
            sheet1.write(7 + j, 0, journal_names[j])
            sheet1.write(0, 3 + j, "Act file" + str(j + 1))

        for jj in range(nucs_active.shape[1]):
            for t in range(nucs_active.shape[0]):
                sheet1.write(1 + t, 3 + jj, nucs_active[t, jj])

        book.save(filename)
