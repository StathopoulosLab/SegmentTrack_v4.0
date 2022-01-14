"""This function writes an .xls file with all statistical info on bursts."""


import numpy as np
# import xlwt
import xlsxwriter


class BurstStatisticWriter:
    """Main class, does all the job"""
    def __init__(self, fwritename, features_3D):

        id         =  features_3D.statistics_info[:, 0].size
        step_info  =  int((features_3D.statistics_info.shape[1] - 3) / 5.0)

        # book      =  xlwt.Workbook(encoding='utf-8')
        # sheet1    =  book.add_sheet("Sheet 1")
        # sheet2    =  book.add_sheet("Sheet 
        book    =  xlsxwriter.Workbook(str(fwritename) + '/Bursts_Statistics.xlsx')                                                                  # write results
        sheet1  =  book.add_worksheet("Sheet1")
        sheet2  =  book.add_worksheet("Sheet2")

        sheet1.write(0, 0, "Nuclei ID")
        sheet1.write(0, 1, "Numb of Bursts")
        sheet1.write(0, 2, "Busts av ampl")
        sheet1.write(0, 2 + step_info, "Bursts integ ampl")
        if 2 + step_info < 256:
            sheet1.write(0, 2 + step_info * 2, "Bursts durations")
        else:
            sheet2.write(0, 2 + step_info * 2 - 256, "Bursts durations")
        if 2 + step_info * 3 < 256:
            sheet1.write(0, 2 + step_info * 3, "Number of Off")
        else:
            sheet2.write(0, 2 + step_info * 3 - 256, "Number of Off")
        if 3 + step_info * 3 < 256:
            sheet1.write(0, 3 + step_info * 3, "Off durations")
        else:
            sheet2.write(0, 3 + step_info * 3 - 256, "Off durations")    

        for k in range(id):
            sheet1.write(k + 1, 0, "Nuc_" + str(np.int(features_3D.statistics_info[k, 0])))
            sheet1.write(k + 1, 1, np.int(features_3D.statistics_info[k, 1]))
            if 2 + step_info * 3 < 256:
                sheet1.write(k + 1, 2 + step_info * 3, features_3D.statistics_info[k, 2 + 4 * step_info])
            else:
                sheet2.write(k + 1, 2 + step_info * 3 - 256, features_3D.statistics_info[k, 2 + 4 * step_info])
            for j in range(step_info):

                if features_3D.statistics_info[k, 2 + 3 * step_info + j] != 0:
                    if 2 + j < 256:
                        sheet1.write(k + 1, 2 + j, features_3D.statistics_info[k, 2 + 3 * step_info + j])
                    else: 
                        sheet2.write(k + 1, 2 + j - 256, features_3D.statistics_info[k, 2 + 3 * step_info + j])

                if features_3D.statistics_info[k, 2 + 2 * step_info + j] != 0:
                    if 2 + step_info + j < 256:
                        sheet1.write(k + 1, 2 + step_info + j, features_3D.statistics_info[k, 2 + 2 * step_info + j])
                    else:
                        sheet2.write(k + 1, 2 + step_info + j - 256, features_3D.statistics_info[k, 2 + 2 * step_info + j])

                if features_3D.statistics_info[k, 2 + j] != 0:
                    if 2 + 2 * step_info + j < 256:
                        sheet1.write(k + 1, 2 + 2 * step_info + j, features_3D.statistics_info[k, 2 + j])
                    else:
                        sheet2.write(k + 1, 2 + 2 * step_info + j - 256, features_3D.statistics_info[k, 2 + j])

                if features_3D.statistics_info[k, 3 + 4 * step_info + j] != 0:
                    if 3 + 3 * step_info + j < 256:
                        sheet1.write(k + 1, 3 + 3 * step_info + j, features_3D.statistics_info[k, 3 + 4 * step_info + j])
                    else:
                        sheet2.write(k + 1, 3 + 3 * step_info + j - 256, features_3D.statistics_info[k, 3 + 4 * step_info + j])    

        # book.save(str(fwritename) + '/Bursts_Statistics.xls')
        book.close()
        

# class BurstStatisticWriter:
#     def __init__(self, fwritename, features_3D):

#         id         =  features_3D.statistics_info[:, 0].size
#         step_info  =  int((features_3D.statistics_info.shape[1] - 3) / 5.0)
#         book      =  xlwt.Workbook(encoding='utf-8')

#         sheet1    =  book.add_sheet("Sheet 1")

#         sheet1.write(0, 0, "Nuclei ID")
#         sheet1.write(0, 1, "Numb of Bursts")
#         sheet1.write(0, 2, "Busts av ampl")
#         sheet1.write(0, 2 + step_info, "Bursts integ ampl")
#         sheet1.write(0, 2 + step_info * 2, "Bursts durations")
#         sheet1.write(0, 2 + step_info * 3, "Number of Off")
#         sheet1.write(0, 3 + step_info * 3, "Off durations")

#         for k in range(id):
#             sheet1.write(k + 1, 0, "Nuc_" + str(np.int(features_3D.statistics_info[k, 0])))
#             sheet1.write(k + 1, 1, np.int(features_3D.statistics_info[k, 1]))
#             sheet1.write(k + 1, 2 + step_info * 3, features_3D.statistics_info[k, 2 + 4 * step_info])
#             for j in range(step_info):
#                 if features_3D.statistics_info[k, 2 + 3 * step_info + j] != 0:
#                     sheet1.write(k + 1, 2 + j, features_3D.statistics_info[k, 2 + 3 * step_info + j])
#                 if features_3D.statistics_info[k, 2 + 2 * step_info + j] != 0:
#                     sheet1.write(k + 1, 2 + step_info + j, features_3D.statistics_info[k, 2 + 2 * step_info + j])
#                 if features_3D.statistics_info[k, 2 + j] != 0:
#                     sheet1.write(k + 1, 2 + 2 * step_info + j, features_3D.statistics_info[k, 2 + j])
#                 if features_3D.statistics_info[k, 3 + 4 * step_info + j] != 0:
#                     sheet1.write(k + 1, 3 + 3 * step_info + j, features_3D.statistics_info[k,  3 + 4 * step_info + j])


#         book.save(str(fwritename) + '/Bursts_Statistics.xls')
