import numpy as np
from xlrd import open_workbook
from scipy.stats import chi2
from scipy.stats import mannwhitneyu

import ChiSquareCalculate


class InternalExternalComparison:
    def __init__(self, xls_filename):
        self.xls_filename  =  xls_filename

        wb            =  open_workbook(self.xls_filename)
        s_wb_int      =  wb.sheets()[0]


        rows_num_int  =  s_wb_int.nrows - 1
        flag          =  0
        idx           =  0
        while flag == 0:
            if str(s_wb_int.col(0)[rows_num_int - idx].value)[:3] != 'Nuc':
                idx  +=  1
            else:
                flag  =  1

        rows_range_int  =  rows_num_int - idx

        num_burst_int   =  np.zeros(rows_range_int)
        for j in range(1, rows_range_int + 1):
            num_burst_int[j - 1]  =  s_wb_int.col(1)[j].value


        flag  =  0
        idx   =  3
        while flag == 0:
            if str(s_wb_int.col(idx)[0].value) != 'Bursts integ ampl':
                idx  +=  1
            else:
                flag  =  1

        bavampl_range  =  np.arange(2, idx)
        avampl_int     =  np.array([])
        for k in bavampl_range:
            for t in range(1, rows_range_int + 1):
                if s_wb_int.col(k)[t].value != '':
                    avampl_int  =  np.append(avampl_int, s_wb_int.col(k)[t].value)


        flag  =  0
        idx   =  bavampl_range.max()
        while flag == 0:
            if str(s_wb_int.col(idx)[0].value) != 'Bursts durations':
                idx  +=  1
            else:
                flag  =  1

        bintegampl_range  =  np.arange(bavampl_range.max() + 1, idx)
        integampl_int     =  np.array([])
        for k in bintegampl_range:
            for t in range(1, rows_range_int + 1):
                if s_wb_int.col(k)[t].value != '':
                    integampl_int  =  np.append(integampl_int, s_wb_int.col(k)[t].value)



        duration_range_int  =  np.arange(bintegampl_range.max() + 1, s_wb_int.ncols)
        duration_int        =  np.array([])
        for k in duration_range_int:
            for t in range(1, rows_range_int + 1):
                if s_wb_int.col(k)[t].value != '':
                    duration_int  =  np.append(duration_int, s_wb_int.col(k)[t].value)



        s_wb_ext      =  wb.sheets()[1]
        rows_num_ext  =  s_wb_ext.nrows - 1
        flag          =  0
        idx           =  0
        while flag == 0:
            if str(s_wb_ext.col(0)[rows_num_ext - idx].value)[:3] != 'Nuc':
                idx  +=  1
            else:
                flag  =  1

        rows_range_ext  =  rows_num_ext - idx

        num_burst_ext   =  np.zeros(rows_range_ext)
        for j in range(1, rows_range_ext + 1):
            num_burst_ext[j - 1]  =  s_wb_ext.col(1)[j].value


        avampl_ext        =  np.array([])
        for k in bavampl_range:
            for t in range(1, rows_range_ext + 1):
                if s_wb_ext.col(k)[t].value != '':
                    avampl_ext  =  np.append(avampl_ext, s_wb_ext.col(k)[t].value)


        integampl_ext  =  np.array([])
        for k in bintegampl_range:
            for t in range(1, rows_range_ext + 1):
                if s_wb_ext.col(k)[t].value != '':
                    integampl_ext  =  np.append(integampl_ext, s_wb_ext.col(k)[t].value)



        duration_range_ext  =  np.arange(bintegampl_range.max() + 1, s_wb_ext.ncols)
        duration_ext        =  np.array([])
        for k in duration_range_ext:
            for t in range(1, rows_range_ext + 1):
                if s_wb_ext.col(k)[t].value != '':
                    duration_ext  =  np.append(duration_ext, s_wb_ext.col(k)[t].value)


        x_chi  =  np.linspace(0, 1, 201)

        bbinn_num         =  np.arange(np.min([num_burst_int.min(), num_burst_ext.min()]), np.max([num_burst_int.max(), num_burst_ext.max()]) + 1)
        csdf_numb_burst   =  ChiSquareCalculate.ChiSquareCalculate(num_burst_int, num_burst_ext, bbinn_num)
        chisq_proof       =  chi2.ppf(x_chi, csdf_numb_burst.df)
        j                 =  np.where(chisq_proof > csdf_numb_burst.chisq)[0][0]
        alpha_numb_burst  =  1 - x_chi[j - 1]

        # bbinn_avampl  =  np.linspace(np.min([avampl_int.min(), avampl_ext.min()]), np.max([avampl_int.max(), avampl_ext.max()]), 100)
        # csdf_avampl   =  ChiSquareCalculate.ChiSquareCalculate(avampl_int, avampl_ext, bbinn_avampl)
        # chisq_proof   =  chi2.ppf(x_chi, csdf_avampl.df)
        # j             =  np.where(chisq_proof > csdf_avampl.chisq)[0][0]
        # alpha_avampl  =  1 - x_chi[j - 1]

        # bbinn_integ      =  np.linspace(np.min([integampl_int.min(), integampl_ext.min()]), np.max([integampl_int.max(), integampl_ext.max()]), 100)
        # csdf_integampl   =  ChiSquareCalculate.ChiSquareCalculate(integampl_int, integampl_ext, bbinn_integ)
        # chisq_proof      =  chi2.ppf(x_chi, csdf_integampl.df)
        # j                =  np.where(chisq_proof > csdf_integampl.chisq)[0][0]
        # alpha_integampl  =  1 - x_chi[j - 1]
        mww              =  mannwhitneyu(integampl_int, integampl_ext)
        alpha_integampl  =  mww.pvalue

        bbinn_dur        =  np.arange(np.min([duration_int.min(), duration_ext.min()]), np.max([duration_int.max(), duration_ext.max()]) + 1)
        csdf_duration    =  ChiSquareCalculate.ChiSquareCalculate(duration_int, duration_ext, bbinn_dur)
        chisq_proof      =  chi2.ppf(x_chi, csdf_duration.df)
        j                =  np.where(chisq_proof > csdf_duration.chisq)[0][0]
        alpha_duration   =  1 - x_chi[j - 1]


        self.chisq_numb_burst  =  csdf_numb_burst.chisq
        self.df_numb_burst     =  csdf_numb_burst.df
        self.alpha_numb_burst  =  alpha_numb_burst
        # self.chisq_avampl      =  csdf_avampl.chisq
        # self.df_avampl         =  csdf_avampl.df
        # self.alpha_avampl      =  alpha_avampl
        # self.chisq_integampl   =  csdf_integampl.chisq
        # self.df_integampl      =  csdf_integampl.df
        self.alpha_integampl   =  alpha_integampl
        self.chisq_duration    =  csdf_duration.chisq
        self.df_duration       =  csdf_duration.df
        self.alpha_duration    =  alpha_duration
