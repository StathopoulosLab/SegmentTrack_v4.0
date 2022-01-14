"""This function serves to organize data with respect to X or Y constrain.

It finds the boundaries and than it feeds some other functions to generate the
excel files according to the statistics.
"""

import numpy as np
import pyqtgraph as pg
import tifffile
# from xlrd import open_workbook
# from xlwt import Workbook
# from xlutils.copy import copy
#from moviepy.editor import VideoClip

import SpatialBurstAnalysis


class SpatialBurstAnalysisSaverX:
    def __init__(self, foldername, raw_spts, spts, nuc_active3c, act_reg, x_coord, num_nucs):
        self.foldername    =  foldername
        self.raw_spts      =  raw_spts
        self.spts          =  spts
        self.nuc_active3c  =  nuc_active3c
        self.act_reg       =  act_reg
        self.x_coord       =  x_coord
        self.num_nucs      =  num_nucs
        reload(SpatialBurstAnalysis)

        x_min_int   =  self.act_reg.best_vals[0] - self.act_reg.best_vals[1] / 2
        x_max_int   =  self.act_reg.best_vals[0] + self.act_reg.best_vals[1] / 2
        x_min_ext1  =  self.act_reg.best_vals[0] - self.act_reg.best_vals[1] * (3 / 2.0)
        x_max_ext1  =  self.act_reg.best_vals[0] - self.act_reg.best_vals[1]
        x_min_ext2  =  self.act_reg.best_vals[0] + self.act_reg.best_vals[1]
        x_max_ext2  =  self.act_reg.best_vals[0] + self.act_reg.best_vals[1] * (3 / 2.0)

        y_min     =  0
        y_max     =  self.spts.shape[2]

        w1        =  pg.plot(self.x_coord, (self.raw_spts * np.sign(self.spts)).sum(2).mean(0), title='Spots Intensity averaged in time and Y axis', pen='r')
        exporter  =  pg.exporters.ImageExporter(w1.plotItem)
        exporter.export(self.foldername + '/' + 'SpotsIntensity.tif')

        # w2        =  pg.plot(np.arange(self.act_reg.ftng.size), self.act_reg.profs, title='Nuclei Activation Averaged in Time and in Y')
        w2        =  pg.plot(self.x_coord, self.act_reg.profs, title='Nuclei Activation Averaged in Time and in Y')
        w2.plot(self.x_coord, self.act_reg.ftng, pen='r')
        exporter  =  pg.exporters.ImageExporter(w2.plotItem)
        exporter.export(self.foldername + '/' + 'AverageActivation.tif')

        SpatialBurstAnalysis.SpatialBurstAnalysisX(self.foldername + '/journal.xls', self.foldername + '/Bursts_Statistics.xls', x_min_int, x_max_int, x_min_ext1, x_max_ext1, x_min_ext2, x_max_ext2, y_min, y_max)

        tifffile.imwrite(str(self.foldername) + "/false_colors_Xboundaries.tif", self.nuc_active3c.astype("uint8"))

        # rb  =  open_workbook(self.foldername + "/journal.xls")
        # wb  =  copy(rb)
        # s   =  wb.get_sheet(0)
        #
        # s.write(0, 3, "Numb Nuclei")
        # for t in range(self.num_nucs.size):
        #     s.write(t + 1, 3, self.num_nucs[t])
        #
        # wb.save(self.foldername + '/journal.xls')


class SpatialBurstAnalysisSaverY:
    def __init__(self, foldername, nuc_active3c, g_coord, study_len):
        self.foldername    =  foldername
        self.nuc_active3c  =  nuc_active3c
        self.g_coord       =  g_coord
        self.study_len     =  study_len

        x_min       =  0
        x_max       =  self.nuc_active3c.shape[1]
        y_min_int   =  self.g_coord - self.study_len
        y_max_int   =  self.g_coord + self.study_len
        y_min_ext1  =  self.g_coord - self.study_len * (5 / 2.0)
        y_max_ext1  =  self.g_coord - self.study_len * (3 / 2.0)
        y_min_ext2  =  self.g_coord + self.study_len * (3 / 2.0)
        y_max_ext2  =  self.g_coord + self.study_len * (5 / 2.0) 


        SpatialBurstAnalysis.SpatialBurstAnalysisY(self.foldername + '/journal.xls', self.foldername + '/Bursts_Statistics.xls', y_min_int, y_max_int, y_min_ext1, y_max_ext1, y_min_ext2, y_max_ext2, x_min, x_max)

        tifffile.imwrite(str(self.foldername) + "/false_colors_Yboundaries.tif", self.nuc_active3c.astype("uint8"))

#        def make_frame(t):
#            frame_for_time_t  =  np.rot90(self.nuc_active3c[np.int(t), :, ::-1, :])
#            return frame_for_time_t
#
#        animation  =  VideoClip(make_frame, duration=self.nuc_active3c.shape[0])
#        animation.write_videofile(str(self.foldername) + "/false_colors_Yboundaries.avi", fps=100, codec='png')  # export as video
