"""This function generates false multicolored movies.

Active nuclei are in red and the intensity of red is related to the intensity of the spots.
Input are a list of folder names with analysis data and a range. The function
determins the highest and the lowest intensity value for all the spots in the
analysis folders and consequently identifies all the intensity limits. Than it
generates false colored movies (ine for each folder of course) in which the
color of the nuclei is as intense as the corresponding spot.
"""


import numpy as np
import pyqtgraph as pg
from xlrd import open_workbook
from skimage.color import label2rgb
from PyQt5 import QtCore, QtWidgets


class MultiColorIntensityGenerator:
    """Main class, does all the job"""
    def __init__(self, all_folders):

        num_clrs  =  3

        # """How to generate colormap"""
        # cmap            =  np.zeros((99, 3))
        # cmap[:33, 0]    =  np.round(np.linspace(0, 194, 33)).astype(np.int)
        # cmap[:33, 2]    =  11
        # cmap[33:66, 0]  =  np.round(np.linspace(194, 255, 33)).astype(np.int)
        # cmap[33:66, 1]  =  np.round(np.linspace(0, 128, 33)).astype(np.int)
        # cmap[33:66, 2]  =  0
        # cmap[66:, 0]    =  255
        # cmap[66:, 1]    =  np.round(np.linspace(128, 230, 33)).astype(np.int)
        # cmap[66:, 0]    =  255

        # lut  =  np.zeros((100, 10), dtype=np.int32)
        # for k in range(10):
        #     lut[:, k]  =  np.arange(0, 100)

        # pg.image(label2rgb(lut, bg_color=[0,0,0], bg_label=0, colors=cmap), title="LUT")

        cmap        =  np.zeros((3, 3))
        cmap[0, :]  =  np.array([194, 0, 11])
        cmap[1, :]  =  np.array([255, 128, 0])
        cmap[2, :]  =  np.array([255, 230, 16])

        pbar  =  QtWidgets.QProgressBar()
        pbar.setRange(0, 0)
        pbar.show()

        max_spts    =  0                                                              # initialise the maximum (we put zeros to be sure the final maximum is going to be from data and not from initialization)        
        for k in range(len(all_folders)):                                           # spots information are taken from the journal file in the analysis folder
            wb      =  open_workbook(all_folders[k] + '/SpotsIntensityDividedByBackground.xls')
            sheet1  =  wb.sheet_by_index(0)

            # spts  =  []                                                       # inizializing list of spots
            t_max  =  1
            while t_max + 1 < sheet1.nrows and str(sheet1.col(3)[t_max + 1].value) != '':                          # finds the number of rows containing the spot intensity 
                t_max  +=  1

            n_max  =  sheet1.ncols - 1
            while str(sheet1.col(n_max)[0].value)[:6] != 'SptId_':              # check against user modification of the file
                n_max  -=  1

            spts  =  np.zeros((t_max + 1, n_max - 2))                           # initializing spots matrix
            for i in range(3, n_max + 1):
                spts[0, i - 3]  =  int(str(sheet1.col(i)[0].value)[6:])         # spot tag in and first time component

            for i in range(3, n_max + 1):                                       # fill the matrix with the value of intensity divided by bkg that each spot takes 
                # print(i)
                QtCore.QCoreApplication.processEvents()                         # update waiting bar
                for j in range(1, t_max + 1):
                    spts[j, i - 3]  =  sheet1.col(i)[j].value

            max_spts  =  np.max([max_spts, spts.max()])                         # extract the maximum of the file and compare with the maximum of the files

            exec("spts_" + str(k) + "= spts")                                   # a new recursive name is given to spts matrix in order to avoid to recalculate it again

        nucs_multiclrs_list  =  []
        for r in range(len(all_folders)):                      # for each folder we load spots tracked, spots intensity and nucslei tracked matrix: from this matrices plus the interval info we will generate false multi colored video    

            nucs_trck  =  np.fromfile(all_folders[r] + '/nuclei_tracked.bin', 'uint16')
            nucs_trck  =  nucs_trck[3:].reshape((nucs_trck[2], nucs_trck[1], nucs_trck[0]))

            nucs_multiclrs  =  np.zeros(nucs_trck.shape)
            spts_idxs       =  eval("spts_" + str(r) + "[0, :].astype(np.int)")     # array with the list of tags and the matrix previously defined
            spts_ints       =  eval("spts_" + str(r))                               # array of all the intensities divided by bkg
            steps           =  nucs_trck.shape[0]


            for h in range(spts_idxs.size):
                QtCore.QCoreApplication.processEvents()
                for t in range(steps):
                    if spts_ints[t + 1, h] != 0:
                        nucs_multiclrs[t, :, :]  +=  int(np.round(255 * spts_ints[t + 1, h] / max_spts)) * (nucs_trck[t, :, :] == spts_idxs[h])    # at each nucleus in each time step is associated a value depending on the spot intensity (divided by bkg)

            nucs_multiclrs                      =   label2rgb(nucs_multiclrs, bg_color=[0, 0, 0], bg_label=0, colors=cmap)         # from intensity matrix to 3 channel matrix (visual purpouse)
            # nucs_multiclrs[:, :, :, 2]  +=  255 * (np.sign(nucs_trck) - np.sign(nucs_multiclrs[:, :, :, 0]))             # add inactive nuclei in blue
            nucs_multiclrs[0, 0, :num_clrs, :]  =   0
            nucs_inactive                       =   (np.sign(nucs_trck) - np.sign(nucs_multiclrs.sum(3)))
            nucs_multiclrs[:, :, :, 2]          +=  77 * nucs_inactive
            nucs_multiclrs[:, :, :, 0]          +=  77 * nucs_inactive
            nucs_multiclrs[:, :, :, 1]          +=  77 * nucs_inactive


            tit_idx  =  all_folders[r][::-1].find('/')
            pg.image(nucs_multiclrs, title=all_folders[r][-tit_idx:])                     # pop-up the 3 channels matrix with proper title

            nucs_multiclrs_list.append(nucs_multiclrs)                                    # storing all 3 channels video in a list to have the output for writing them 

        pbar.close()
        self.nucs_multiclrs_list  =  nucs_multiclrs_list


