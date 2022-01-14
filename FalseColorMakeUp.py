"""This function generates a video with different colors for mother active and mother inactive nuclei.

Input data is the folder path with analysis results.
"""



# from os import listdir
import numpy as np
# from xlrd import open_workbook
import tifffile
# from scipy.ndimage import binary_dilation

import AnalysisLoader
import SpotsConnection
import NucleiSpotsConnection


class FalseColoredMakeUp:
    """Only class, does all the job"""
    def __init__(self, folder_name):

        imarray_red_whole                             =  AnalysisLoader.RawData(folder_name).imarray_red
        imarray_red_whole[imarray_red_whole >= 2000]  =  2000
        spots_3D                                      =  AnalysisLoader.SpotsIntsVol(folder_name)
        nuclei_tracked                                =  np.fromfile(folder_name + '/nuclei_tracked.bin', "uint16")
        nuclei_tracked                                =  nuclei_tracked[3:].reshape((nuclei_tracked[2], nuclei_tracked[1], nuclei_tracked[0]))
        spots_tracked_3D                              =  SpotsConnection.SpotsConnection(nuclei_tracked, np.sign(spots_3D.spots_vol), 5).spots_tracked

        nucs_act    =  NucleiSpotsConnection.NucleiSpotsConnection(spots_tracked_3D, nuclei_tracked).nuclei_active
        nucs_act    =  nucs_act == 2
        nucs_inact  =  (np.sign(nuclei_tracked) * (1 - nucs_act)).astype(bool)
        mtx_fin     =  np.zeros(nucs_act.shape + (3,), np.uint16)

        mtx_fin[:, :, :, 0]   =  nucs_act  *  imarray_red_whole
        mtx_fin[:, :, :, 1]   =  nucs_act  *  imarray_red_whole
        mtx_fin[:, :, :, 2]   =  nucs_act  *  imarray_red_whole
        mtx_fin[:, :, :, 2]  +=  nucs_inact  *  imarray_red_whole

        con_spts              =  np.sign(spots_tracked_3D).astype(np.uint16)
        mtx_fin[:, :, :, 0]  *=  (1 - con_spts)
        mtx_fin[:, :, :, 1]  *=  (1 - con_spts)
        mtx_fin[:, :, :, 2]  *=  (1 - con_spts)
        mtx_fin[:, :, :, 0]  +=  con_spts * imarray_red_whole.max()

        tifffile.imwrite(folder_name + '/active_inactive_makeup_nc14.tif', np.rot90(mtx_fin[:, :, ::-1], axes=(1, 2)))
        # tifffile.imwrite('/home/atrullo/Desktop/active_inactive_makeup.tif', np.rot90(mtx_fin[:, :, :-1], axes=(1, 2)))

        self.mtx_fin  =  mtx_fin




class FalseColoredMakeUpRY:
    """Only class, does all the job"""
    def __init__(self, folder_name):

        imarray_red_whole                             =  AnalysisLoader.RawData(folder_name).imarray_red
        imarray_red_whole[imarray_red_whole >= 2000]  =  2000
        spots_3D                                      =  AnalysisLoader.SpotsIntsVol(folder_name)
        nuclei_tracked                                =  np.fromfile(folder_name + '/nuclei_tracked.bin', "uint16")
        nuclei_tracked                                =  nuclei_tracked[3:].reshape((nuclei_tracked[2], nuclei_tracked[1], nuclei_tracked[0]))
        spots_tracked_3D                              =  SpotsConnection.SpotsConnection(nuclei_tracked, np.sign(spots_3D.spots_vol), 5).spots_tracked

        nucs_act    =  NucleiSpotsConnection.NucleiSpotsConnection(spots_tracked_3D, nuclei_tracked).nuclei_active
        nucs_act    =  nucs_act == 2
        nucs_inact  =  (np.sign(nuclei_tracked) * (1 - nucs_act)).astype(bool)
        mtx_fin     =  np.zeros(nucs_act.shape + (3,), np.uint16)

        mtx_fin[:, :, :, 0]  =  imarray_red_whole
        mtx_fin[:, :, :, 1]  =  nucs_act  *  imarray_red_whole

        # mtx_fin[:, :, :, 0]   =  nucs_act  *  imarray_red_whole
        # mtx_fin[:, :, :, 1]   =  nucs_act  *  imarray_red_whole
        # mtx_fin[:, :, :, 2]   =  nucs_act  *  imarray_red_whole
        # mtx_fin[:, :, :, 2]  +=  nucs_inact  *  imarray_red_whole
        #
        # con_spts              =  np.sign(spots_tracked_3D).astype(np.uint16)
        # mtx_fin[:, :, :, 0]  *=  (1 - con_spts)
        # mtx_fin[:, :, :, 1]  *=  (1 - con_spts)
        # mtx_fin[:, :, :, 2]  *=  (1 - con_spts)
        # mtx_fin[:, :, :, 0]  +=  con_spts * imarray_red_whole.max()

        tifffile.imwrite(folder_name + '/active_inactive_makeup_nc14_ry.tif', np.rot90(mtx_fin[:, :, ::-1], axes=(1, 2)))
        # tifffile.imwrite('/home/atrullo/Desktop/active_inactive_makeup.tif', np.rot90(mtx_fin[:, :, :-1], axes=(1, 2)))

        self.mtx_fin  =  mtx_fin


#         files  =  listdir(folder_name)                         # search in the analysis folder the xls files to read the background values
#         for file in files:
#             if file[:24] == "MemoryStudyWithDistances":        # select the .xls file with spot analysis results, green
#                 xls_name  =  file
#                 break
#
#         imarray_red_whole  =  np.load(folder_name + '/imarray_red_whole.npy')
#         evol_conc_ok       =  LoadMergedResults.LoadMergedResultsEvolCheck(folder_name).conc_nuc_ok
#
#
#         book       =  open_workbook(folder_name + "/" + xls_name)
#         sheet      =  book.sheet_by_index(0)
#         tags_list  =  sheet.col_values(0)[1:]
#         mthr_list  =  sheet.col_values(1)[1:]
#
#         kk  =  1
#         while tags_list[kk] != '':
#             kk += 1
#
#         tags_list        =  tags_list[:kk]
#         mthr_list        =  mthr_list[:kk]
#         tags_list        =  [int(tag[3:])for tag in tags_list]
#         mthr_list        =  np.asarray(mthr_list)
#         mthr_act_tags    =  [tags_list[idx] for idx in np.where(mthr_list != 0)[0]]
#         mthr_inact_tags  =  [tags_list[idx] for idx in np.where(mthr_list == 0)[0]]
#
#         mthr_act_inact_mtx  =  np.zeros(evol_conc_ok.shape + (3,))
#         msk                 =  np.zeros(imarray_red_whole.shape)
#         for k in mthr_act_tags:
#             bff                              =  (evol_conc_ok == k)
#             msk                             +=  bff
#             mthr_act_inact_mtx[:, :, :, 1]  +=  imarray_red_whole * bff
#
#         for j in mthr_inact_tags:
#             bff                              =  (evol_conc_ok == j)
#             msk                             +=  bff
#             mthr_act_inact_mtx[:, :, :, 0]  +=  imarray_red_whole * bff
#
#         for t in range(msk.shape[0]):
#             msk[t]  =  binary_dilation(msk[t], iterations=2)
#
#         mthr_act_inact_mtx[:, :, :, 0]  *=  1 - con_spts     # + con_spts * imarray_red_whole.max()
#         mthr_act_inact_mtx[:, :, :, 1]  *=  1 - con_spts     # + con_spts * imarray_red_whole.max()
#         mthr_act_inact_mtx[:, :, :, 2]  *=  1 - con_spts     # + con_spts * imarray_red_whole.max()
#
#         mthr_act_inact_mtx[:, :, :, 0]  +=  con_spts * msk * imarray_red_whole.max()
#         mthr_act_inact_mtx[:, :, :, 1]  +=  con_spts * msk * imarray_red_whole.max()
#         mthr_act_inact_mtx[:, :, :, 2]  +=  con_spts * msk * imarray_red_whole.max()

        # self.tab3_flag        =  1
        # self.spots_segm_flag  =  0
        # self.spots_trk_flag   =  1
        # self.frame4.setImage(np.sign(self.spots_tracked_3D[self.sld1.value(), :, :]))


        # ipp_3D            =  self.spots_3D.spots_ints.reshape(self.spots_3D.spots_ints.size)
        # i                 =  np.where(ipp_3D == 0)[0]
        # ipp_3D            =  np.delete(ipp_3D, i, axis=0)
        # self.ipp_3D_av    =  ipp_3D.sum() / np.float(self.spots_3D.spots_vol.sum())                                                               # ipp is defined just to calculate the average intensity value of the spots, ipp_av
        # self.features_3D  =  ParametersExtraction.ParametersExtraction(self.spots_3D.spots_ints, self.spots_tracked_3D, self.spots_3D.spots_vol)   # spots_3D.spots_vol * np.sign(self.spots_tracked_3D))





