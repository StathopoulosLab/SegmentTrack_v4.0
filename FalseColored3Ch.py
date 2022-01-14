"""This function generates false multicolored movie.

There are 3 colors that are assigned to nuclei depending on the time of the first activation.
Input are tracked nuclei, tracked spots and the two reference times.
"""


import numpy as np
import xlsxwriter
from skimage.morphology import label
from PyQt5 import QtWidgets


class FalseColored3Ch:
    """This class generates false multicoloured movies"""
    def __init__(self, nuc_tracked, spts_tracked, sld1_val, sld2_val):

        sp_idxs  =  np.unique(spts_tracked)[1:]

        false3ch  =  np.zeros(np.append(nuc_tracked.shape, 3))

        pbar      =  ProgressBar(total1=sp_idxs.size)
        pbar_idx  =  0
        pbar.show()

        for k in sp_idxs:
            pbar.update_progressbar(pbar_idx)
            pbar_idx   +=  1
            prof       =   np.sign((spts_tracked == k).sum(2).sum(1))
            first_act  =   np.where(prof == 1)[0][0]

            if first_act <= sld1_val:
                false3ch[first_act:, :, :, 1]  +=  255 * (nuc_tracked[first_act:, :, :] == k).astype(np.int)

            if sld1_val < first_act <= sld2_val:
                false3ch[first_act:, :, :, 0]  +=  255 * (nuc_tracked[first_act:, :, :] == k).astype(np.int)
                false3ch[first_act:, :, :, 1]  +=  255 * (nuc_tracked[first_act:, :, :] == k).astype(np.int)

            if first_act > sld2_val:
                false3ch[first_act:, :, :, 0]  +=  255 * (nuc_tracked[first_act:, :, :] == k).astype(np.int)

        false3ch[:, :, :, 2]  =  255 * np.sign(nuc_tracked) * (1 - np.sign(false3ch.sum(3)))

        self.false3ch  =  false3ch


class FalseColoredTimeWrite:
    """Class to write results and data oof the false multicoloured movie"""
    def __init__(self, fwritename, nuc_tracked, false3ch, sld1_val, sld2_val, time_step_var, fnames):

        last_fr   =  false3ch[-1, :, :, :] / 255
        num_red   =  label(nuc_tracked[-1, :, :] * (last_fr[:, :, 0] - (last_fr.sum(2) == 2)), connectivity=1).max()
        num_gre   =  label(nuc_tracked[-1, :, :] * (last_fr[:, :, 1] - (last_fr.sum(2) == 2)), connectivity=1).max()
        num_blue  =  label(nuc_tracked[-1, :, :] * (last_fr[:, :, 2]), connectivity=1).max()
        num_yell  =  label(nuc_tracked[-1, :, :] * (last_fr.sum(2) == 2), connectivity=1).max()

        num_tot  =  num_red + num_gre + num_blue + num_yell

        book    =  xlsxwriter.Workbook(fwritename + '/MultiFalseColored.xlsx')
        sheet1  =  book.add_worksheet("Sheet 1")

        sheet1.write(0, 1, "Number")
        sheet1.write(0, 2, "Percentage")

        sheet1.write(1, 0, "Nucs Green")
        sheet1.write(2, 0, "Nucs Yellow")
        sheet1.write(3, 0, "Nucs Red")
        sheet1.write(4, 0, "Nucs Blue")
        sheet1.write(5, 0, "Nucs Tot")

        sheet1.write(1, 1, float(num_gre))
        sheet1.write(2, 1, float(num_yell))
        sheet1.write(3, 1, float(num_red))
        sheet1.write(4, 1, float(num_blue))
        sheet1.write(5, 1, float(num_tot))

        sheet1.write(1, 2, 100 * num_gre  / num_tot.astype(np.float))
        sheet1.write(2, 2, 100 * num_yell / num_tot.astype(np.float))
        sheet1.write(3, 2, 100 * num_red  / num_tot.astype(np.float))
        sheet1.write(4, 2, 100 * num_blue / num_tot.astype(np.float))
        sheet1.write(5, 2, 100 * num_tot  / num_tot.astype(np.float))

        sheet1.write(0, 4, "First Time Ref")
        sheet1.write(0, 5, "Second Time Ref")
        sheet1.write(1, 4, sld1_val)
        sheet1.write(1, 5, sld2_val)

        sheet1.write(0, 7, "Seconds per Frame")
        sheet1.write(1, 7, time_step_var)

        sheet1.write(7, 0, "File Name")
        sheet1.write(8, 0, str(fnames))

        book.close()


class ProgressBar(QtWidgets.QWidget):
    """Simple progress bar"""
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
        """Progress bar updater"""
        self.progressbar1.setValue(val1)
        QtWidgets.qApp.processEvents()
