"""This function loads the previously done analysis."""


# import os
import numpy as np
# from xlrd import open_workbook
from PyQt5 import QtWidgets

import MultiLoadCzi5D


# class RawData:
#     """Load raw data file"""
#     def __init__(self, foldername):

#         if os.path.isfile(foldername + '/raw_data_nuclei.bin'):
#             imarray_red    =  np.fromfile(foldername + '/raw_data_nuclei.bin', 'uint16')
#             imarray_red    =  imarray_red[3:].reshape((imarray_red[2], imarray_red[1], imarray_red[0]))

#             imarray_green  =  np.fromfile(foldername + '/raw_data_spots.bin', 'uint16')
#             imarray_green  =  imarray_green[3:].reshape((imarray_green[2], imarray_green[1], imarray_green[0]))

#             green4D  =  np.fromfile(foldername + '/raw_data_green4D.bin', 'uint16')
#             green4D  =  green4D[4:].reshape((green4D[3], green4D[0], green4D[2], green4D[1]))

#             wb          =  open_workbook(foldername + '/journal.xls')
#             s_wb        =  wb.sheets()[0]
#             pix_size    =  s_wb.col(1)[15].value
#             pix_size_Z  =  s_wb.col(1)[16].value

#             self.imarray_green  =  imarray_green
#             self.imarray_red    =  imarray_red
#             self.green4D        =  green4D
#             self.pix_size       =  pix_size
#             self.pix_size_Z     =  pix_size_Z

#         elif os.path.isfile(foldername + '/im_red_smpl.npy'):
#             fnames       =  QtWidgets.QFileDialog.getOpenFileNames(None, "Select czi (or lsm) data files to concatenate...", filter="*.lsm *.czi *.tif *.lif")[0]
#             raw_data     =  MultiLoadCzi5D.MultiProcLoadCzi5D(fnames, np.fromfile(foldername + '/nucs_spts_ch.bin', 'uint16'))
#             im_red_smpl  =  np.load(foldername + '/im_red_smpl.npy')
#             jj_start     =  np.where(np.sum(raw_data.imarray_red - im_red_smpl[0], axis=(1, 2)) == 0)[0][0]
#             jj_end       =  np.where(np.sum(raw_data.imarray_red - im_red_smpl[1], axis=(1, 2)) == 0)[0][0]

#             self.imarray_green  =  raw_data.imarray_green[jj_start:jj_end + 1]
#             self.imarray_red    =  raw_data.imarray_red[jj_start:jj_end + 1]
#             self.green4D        =  raw_data.green4D[jj_start:jj_end + 1]
#             self.pix_size       =  raw_data.pix_size


class RawData:
    """Load raw data file"""
    def __init__(self, foldername):

        fnames       =  QtWidgets.QFileDialog.getOpenFileNames(None, "Select czi (or lsm) data files to concatenate...", filter="*.lsm *.czi *.tif *.lif")[0]
        # fnames  =  ['/home/atrullo/Desktop/Louise2Spots/Kr_E3_09242021/Kr_E3_09242021_i_Out.czi']
        raw_data     =  MultiLoadCzi5D.MultiProcLoadCzi5D(fnames, np.fromfile(foldername + '/nucs_spts_ch.bin', 'uint16'))
        im_red_smpl  =  np.load(foldername + '/im_red_smpl.npy')
        jj_start     =  np.where(np.sum(raw_data.imarray_red - im_red_smpl[0], axis=(1, 2)) == 0)[0][0]
        jj_end       =  np.where(np.sum(raw_data.imarray_red - im_red_smpl[1], axis=(1, 2)) == 0)[0][0]

        self.imarray_green  =  raw_data.imarray_green[jj_start:jj_end + 1]
        self.imarray_red    =  raw_data.imarray_red[jj_start:jj_end + 1]
        self.green4D        =  raw_data.green4D[jj_start:jj_end + 1]
        self.pix_size       =  raw_data.pix_size
        self.pix_size_Z     =  raw_data.pix_size_Z


class SpotsIntsVol:
    """Loads intensity and volume of detected spots"""
    def __init__(self, foldername):

        self.spots_ints     =  np.load(foldername + '/spots_3D_ints.npy')
        self.spots_vol      =  np.load(foldername + '/spots_3D_vol.npy')
        self.spots_tzxy     =  np.load(foldername + '/spots_3D_tzxy.npy')
        self.spots_coords   =  np.load(foldername + '/spots_3D_coords.npy')


class Features:
    """Load spots features"""
    def __init__(self, foldername):

        self.statistics_info  =  np.load(foldername + '/spots_features3D.npy')


class SpotsIntsVolRescue:
    """Load intensity and volume for analysis rescue"""
    def __init__(self):

        self.spots_ints  =  np.load('rescue_spts_ints.npy')
        self.spots_vol   =  np.load('rescue_spts_vol.npy')
        self.spots_tzxy  =  np.load('rescue_spts_tzxy.npy')
