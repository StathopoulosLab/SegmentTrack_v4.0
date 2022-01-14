import numpy as np
import xlrd
import xlwt
from xlutils.copy import copy

import InternalExternalComparison


class SpatialBurstAnalysisX:
    def __init__(self, journalfname, burstfilename, x_min_int, x_max_int, x_min_ext1, x_max_ext1, x_min_ext2, x_max_ext2, y_min, y_max):
        self.journalfname   =  journalfname
        self.burstfilename  =  burstfilename
        self.y_min          =  y_min
        self.y_max          =  y_max
        self.x_min_int   =  x_min_int
        self.x_max_int   =  x_max_int
        self.x_min_ext1  =  x_min_ext1
        self.x_max_ext1  =  x_max_ext1
        self.x_min_ext2  =  x_min_ext2
        self.x_max_ext2  =  x_max_ext2

        wb_b       =  xlrd.open_workbook(self.burstfilename)
        s_b        =  wb_b.sheets()[0]
        wb_j       =  xlrd.open_workbook(self.journalfname)
        b_row_len  =  len(s_b.row(0))
        steps      =  int(wb_j.sheets()[0].col(4)[-1].value + 1)                                                        # number of time frames (4 is the column index of 'TIME')

        book      =  xlwt.Workbook(encoding='utf-8')
        sheet1    =  book.add_sheet("Internal")
        sheet2    =  book.add_sheet("External")

        for o in range(b_row_len):
            sheet1.write(0, o, s_b.row(0)[o].value)
            sheet2.write(0, o, s_b.row(0)[o].value)

        if len(wb_j.sheets()) == 2 and len(wb_j.sheets()[1].col(0)) != 0:
            num_sheets  =  2

        if len(wb_j.sheets()) == 2 and len(wb_j.sheets()[1].col(0)) == 0:
            num_sheets  =  1

        row_idx_inter  =  0
        row_idx_exter  =  0

        id_b  =  0
        for j in range(num_sheets):
            s_j       =  wb_j.sheets()[j]                                                                                 # in case the journal has 2 sheets (a lot of nuclei)
            num_cols  =  s_j.ncols
            # n_spts  =  len(s_j.row(0)) - 6                                                                              # number of spots (the first 6 cells are empty)

            flag      =  0
            idx_spts  =  0
            while flag == 0 and idx_spts < num_cols - 6:
                # print s_j.col(6 + idx_spts)[0].value
                if s_j.col(6 + idx_spts)[0].value[:5] == 'Spot_':
                    idx_spts  +=  1
                else:
                    flag  =  1

            n_spts  =  idx_spts - 1

            for id_j in range(n_spts):

                flag  =  0
                while flag == 0:
                    if str(s_j.col(6 + id_j)[0].value[5:]) == str(s_b.col(0)[id_b].value)[4:]:
                        flag  =  1
                    else:
                        id_b  +=  1

                x_coord  =  np.zeros(steps)
                for t in range(steps):
                    x_coord[t]  =  s_j.col(6 + id_j)[steps + 3 + t].value
                x_coord_av  =  np.delete(x_coord, np.where(x_coord == 0), axis=0).mean()

                y_coord  =  np.zeros(x_coord.shape)
                for t in range(steps):
                    y_coord[t]  =  s_j.col(6 + id_j)[2 * steps + 5 + t].value
                y_coord_av  =  np.delete(y_coord, np.where(y_coord == 0), axis=0).mean()

                if self.x_min_int < x_coord_av < self.x_max_int and self.y_min < y_coord_av < self.y_max:
                    for k in range(b_row_len):
                        sheet1.write(1 + row_idx_inter, k, s_b.row(id_b)[k].value)
                    row_idx_inter  +=  1

                if self.x_min_ext1 < x_coord_av < self.x_max_ext1 or self.x_min_ext2 < x_coord_av < self.x_max_ext2:
                    for k in range(b_row_len):
                        sheet2.write(1 + row_idx_exter, k, s_b.row(id_b)[k].value)
                    row_idx_exter  +=  1


        burst_spatially_org  =  self.journalfname[:-self.journalfname[::-1].find('/')] + "Burst_Spatially_organized_X.xls"
        book.save(burst_spatially_org)


        comparison  =  InternalExternalComparison.InternalExternalComparison(burst_spatially_org)
        rb          =  xlrd.open_workbook(burst_spatially_org)
        wb          =  copy(rb)
        s           =  wb.get_sheet(0)

        s.write(row_idx_inter + 6, 0, "alpha burst numb")
        s.write(row_idx_inter + 6, 1, comparison.alpha_numb_burst)

        # s.write(row_idx_inter + 7, 0, "alpha av amplitude")
        # s.write(row_idx_inter + 7, 1, comparison.alpha_avampl)

        s.write(row_idx_inter + 8, 0, "alpha integ amplitude")
        s.write(row_idx_inter + 8, 1, comparison.alpha_integampl)

        s.write(row_idx_inter + 9, 0, "alpha duration")
        s.write(row_idx_inter + 9, 1, comparison.alpha_duration)

        wb.save(burst_spatially_org)



class SpatialBurstAnalysisY:
    # def __init__(self, journalfname, burstfilename, g_coord, study_len):
    def __init__(self, journalfname, burstfilename, y_min_int, y_max_int, y_min_ext1, y_max_ext1, y_min_ext2, y_max_ext2, x_min, x_max):
        self.journalfname   =  journalfname
        self.burstfilename  =  burstfilename
        self.y_min_int   =  y_min_int
        self.y_max_int   =  y_max_int
        self.y_min_ext1  =  y_min_ext1
        self.y_max_ext1  =  y_max_ext1
        self.y_min_ext2  =  y_min_ext2
        self.y_max_ext2  =  y_max_ext2
        self.x_min       =  x_min
        self.x_max       =  x_max


        wb_b       =  xlrd.open_workbook(self.burstfilename)
        s_b        =  wb_b.sheets()[0]
        wb_j       =  xlrd.open_workbook(self.journalfname)
        b_row_len  =  len(s_b.row(0))
        steps      =  int(wb_j.sheets()[0].col(4)[-1].value + 1)                                                        # number of time frames (4 is the column index of 'TIME')

        book      =  xlwt.Workbook(encoding='utf-8')
        sheet1    =  book.add_sheet("Internal")
        sheet2    =  book.add_sheet("External")

        for o in range(b_row_len):
            sheet1.write(0, o, s_b.row(0)[o].value)
            sheet2.write(0, o, s_b.row(0)[o].value)

        if len(wb_j.sheets()) == 2 and len(wb_j.sheets()[1].col(0)) != 0:
            num_sheets  =  2

        if len(wb_j.sheets()) == 2 and len(wb_j.sheets()[1].col(0)) == 0:
            num_sheets  =  1

        row_idx_inter  =  0
        row_idx_exter  =  0

        id_b  =  0
        for j in range(num_sheets):
            s_j     =  wb_j.sheets()[j]                                                                                 # in case the journal has 2 sheets (a lot of nuclei)
            idx_spts  =  6

            for idx_spts in range(s_j.ncols - 6):
                if s_j.col(6 + idx_spts)[0].value[:5] != 'Spot_':
                    break

            n_spts  =  np.min([s_j.ncols, idx_spts])

            for id_j in range(n_spts):

                flag  =  0
                while flag == 0:
                    if str(s_j.col(6 + id_j)[0].value[5:]) == str(s_b.col(0)[id_b].value)[4:]:
                        flag  =  1
                    else:
                        id_b  +=  1

                y_coord  =  np.zeros(steps)
                for t in range(steps):
                    y_coord[t]  =  s_j.col(6 + id_j)[2 * steps + 5 + t].value
                y_coord_av  =  np.delete(y_coord, np.where(y_coord == 0), axis=0).mean()

                if y_min_int < y_coord_av < self.y_max_int:
                    for k in range(b_row_len):
                        sheet1.write(1 + row_idx_inter, k, s_b.row(id_b)[k].value)
                    row_idx_inter += 1

                if self.y_min_ext1 < y_coord_av < self.y_max_ext1 or self.y_min_ext2 < y_coord_av < self.y_max_ext2:
                    for k in range(b_row_len):
                        sheet2.write(1 + row_idx_exter, k, s_b.row(id_b)[k].value)
                    row_idx_exter += 1

        burst_spatially_org  =  self.journalfname[:-self.journalfname[::-1].find('/')] + "Burst_Spatially_organized_Y.xls"
        book.save(burst_spatially_org)

        comparison  =  InternalExternalComparison.InternalExternalComparison(burst_spatially_org)
        rb          =  xlrd.open_workbook(burst_spatially_org)
        wb          =  copy(rb)
        s           =  wb.get_sheet(0)

        s.write(row_idx_inter + 6, 0, "alpha burst numb")
        s.write(row_idx_inter + 6, 1, comparison.alpha_numb_burst)

        # s.write(row_idx_inter + 7, 0, "alpha av amplitude")
        # s.write(row_idx_inter + 7, 1, comparison.alpha_avampl)

        s.write(row_idx_inter + 8, 0, "alpha integ amplitude")
        s.write(row_idx_inter + 8, 1, comparison.alpha_integampl)

        s.write(row_idx_inter + 9, 0, "alpha duration")
        s.write(row_idx_inter + 9, 1, comparison.alpha_duration)

        wb.save(burst_spatially_org)
