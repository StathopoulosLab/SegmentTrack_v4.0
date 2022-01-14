"""This function merges selected .xls file from WriteSteadySpotsBursting and writes a global one."""


import xlrd
import xlwt
import datetime


class MergeXlsFiles:
    """Only class, does all the job"""
    def __init__(self, fname2write, xls2merge):

        book    =  xlwt.Workbook(encoding='utf-8')
        sheet1  =  book.add_sheet("Sheet 1")

        def coord_finder(sheet1_opn):
            k  =  0
            while str(sheet1_opn.col(0)[k].value[:4]) != "Nuc_":
                k  +=  1
            k_in  =  k
            while str(sheet1_opn.col(0)[k].value[:4]) == "Nuc_":
                k  +=  1
            return [k_in, k]

        for j in range(len(xls2merge)):
            sheet1.write(j, 0, xls2merge[j])
        fnames_row  =  j + 2

        sheet1.write(fnames_row, 0, 'Nuclei ID')
        sheet1.write(fnames_row, 1, 'Integral Amplitude')
        sheet1.write(fnames_row, 2, 'Average Amplitude')
        sheet1.write(fnames_row, 3, 'Duration')
        sheet1.write(fnames_row, 4, 'X coord')
        sheet1.write(fnames_row, 5, 'Y coord')

        fnames_row  +=  2

        for j in range(len(xls2merge)):
            book_opn    =  xlrd.open_workbook(xls2merge[j])
            sheet1_opn  =  book_opn.sheet_by_index(0)
            pos_ref     =  coord_finder(sheet1_opn)

            for k in range(pos_ref[1] - pos_ref[0]):
                sheet1.write(fnames_row + k, 0, sheet1_opn.col(0)[pos_ref[0] + k].value)
                sheet1.write(fnames_row + k, 1, sheet1_opn.col(1)[pos_ref[0] + k].value)
                sheet1.write(fnames_row + k, 2, sheet1_opn.col(2)[pos_ref[0] + k].value)
                sheet1.write(fnames_row + k, 3, sheet1_opn.col(3)[pos_ref[0] + k].value)
                sheet1.write(fnames_row + k, 4, sheet1_opn.col(4)[pos_ref[0] + k].value)
                sheet1.write(fnames_row + k, 5, sheet1_opn.col(5)[pos_ref[0] + k].value)

            fnames_row  +=  k + 2


        date_format = xlwt.XFStyle()
        date_format.num_format_str = 'dd/mm/yyyy'
        sheet1.write(fnames_row + 2, 0, 'date')
        sheet1.write(fnames_row + 2, 1, datetime.datetime.now(), date_format)


        if fname2write[-3:] == 'xls':
            book.save(fname2write)
        else:
            book.save(fname2write + '.xls')
