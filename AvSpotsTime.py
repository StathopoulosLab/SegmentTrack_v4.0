"""This function copies the values of intensity spots divided by background
into another excel file.

The starting xls files contains all the intensity value divided by background
that a spot takes during the whole evolution. This function copies these values
for all the spots for a certain range of time, specified by t1 and t2. t1 and t2
are expressed in frames, not in seconds.
"""

import os
import numpy as np
import xlwt
from xlrd import open_workbook
from xlutils.copy import copy


class AvSpotsTime:
    def __init__(self, filename, foldername, spots_vals, t1, t2, t1_text, t2_text):

        t1_text  =  t1_text.replace(",", ":")                                   # replace the comma with colon for time writing
        t2_text  =  t2_text.replace(",", ":")

        foldername_sub  =  foldername[:-1]
        ref_name        =  foldername_sub[::-1].find('/')

        if os.path.isfile(filename) is False:                                   # check if there is a file to modify or a new file to write
            book    =  xlwt.Workbook(encoding='utf-8')
            sheet1  =  book.add_sheet("Sheet 1")
            sheet2  =  book.add_sheet("Averages")
            rf_wrt  =  0

        else:
            wb_file2write  =  open_workbook(filename, formatting_info=True, on_demand=True)
            rf_wrt         =  wb_file2write.get_sheet(0).ncols + 1
            book           =  copy(wb_file2write)
            sheet1         =  book.get_sheet(0)
            sheet2         =  book.get_sheet(1)
            os.remove(filename)

        sheet1.write(0, rf_wrt, foldername[len(foldername) - ref_name - 1:])
        sheet1.write(1, rf_wrt, "Time " + str(t1_text) + " to " + str(t2_text))

        sheet2.write(0, rf_wrt, foldername[len(foldername) - ref_name - 1:])
        sheet2.write(1, rf_wrt, "Time " + str(t1_text) + " to " + str(t2_text))

        nn  =  3
        for s in range(spots_vals.shape[1]):
            for t in range(t1, t2):
                sheet1.write(nn, rf_wrt, spots_vals[t, s])
                nn  +=  1
            nn  +=  1

        time_avgs  =  np.zeros((t2 - t1))
        for tt in range(t1, t2):                                                # average of all the spots per single time frame 
            bffr_calc           =  spots_vals[tt, :]
            time_avgs[tt - t1]  =  bffr_calc[bffr_calc != 0].mean()

        time_avgs  =  np.nan_to_num(time_avgs)    
        numb_spts  =  np.sign(spots_vals[t1:t2, :].sum(0)).sum()                              # number of spots considered for the average

        sheet1.write(nn + 7, rf_wrt, np.nan_to_num(time_avgs[time_avgs != 0].mean()))         # average of all the spots in each of the selected time frames and than total average
        sheet1.write(nn + 8, rf_wrt, numb_spts)                                               # number of spots used for the average

        sheet2.write(7, rf_wrt, np.nan_to_num(time_avgs[time_avgs != 0].mean()))              # average of all the spots in each of the selected time frames and than total average
        sheet2.write(8, rf_wrt, numb_spts)                                                    # number of spots used for the average
        
        if filename[-4:] == '.xls':
            book.save(filename)    
        else:
            book.save(filename + '.xls')
