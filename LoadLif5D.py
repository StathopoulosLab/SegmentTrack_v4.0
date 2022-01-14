"""This function loads .lif files.

Given the filename of a .lsm files, this function gives as output the matrices
of the red and green channels maximum intensity projected plus the green channel
as it is. Inputs are the file-name and the channel number for nuclei and spots.
"""


import numpy as np
import read_lif
# from PyQt5 import QtGui, QtWidgets



class LoadLif5D:
    """Only class, does all the job"""
    def __init__(self, fname, nucs_spts_ch, num_bit):


        reader            =  read_lif.Reader(fname)
        series            =  reader.getSeries()
        chosen            =  series[0]                                                        # choose first image in the lif file
        steps             =  int(chosen.getTotalDuration() / chosen.getTimeLapse())
        zlen, xlen, ylen  =  chosen.getFrame(T=0, dtype=num_bit, channel=0).shape

        red_mtx    =  np.zeros((steps, xlen, ylen), np.uint32)
        green_mtx  =  np.zeros((steps, xlen, ylen), np.uint32)
        green4D    =  np.zeros((steps, zlen, xlen, ylen), np.uint32)
        for t in range(steps):
            red_mtx[t]    =  chosen.getFrame(T=t, dtype=num_bit, channel=nucs_spts_ch[0]).max(0)
            green_mtx[t]  =  chosen.getFrame(T=t, dtype=num_bit, channel=nucs_spts_ch[1]).max(0)
            green4D[t]    =  chosen.getFrame(T=t, dtype=num_bit, channel=nucs_spts_ch[1])

        self.red_mtx     =  red_mtx
        self.green_mtx   =  green_mtx
        self.green4D     =  green4D
        self.pix_sizeX   =  series[0].getMetadata()['voxel_size_x']
        self.pix_sizeZ   =  series[0].getMetadata()['voxel_size_z']
        self.time_lapse  =  chosen.getTimeLapse()


