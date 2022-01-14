"""This function loads and concatenates .lsm filedata as they come from microscope.

Taking .lsm filenames as input, the output are the concatenated matrices of the
maximum intensity projection of red and green channels plus the green channel in
4D (because of 3D detection purposes). Matrices are also flipped and rotate to
have a visualization conform to ImageJ standards.
"""


import numpy as np
from tifffile import TiffFile

import LoadLsm5D


class MultiLoadLsmOrTif5D:
    def __init__(self, fnames, nucs_spts_ch):

        time_steps     =  np.array([])
        mt_buff        =  LoadLsm5D.LoadLsm5D(str(fnames[0]), nucs_spts_ch)
        imarray_red    =  mt_buff.red_mtx
        imarray_green  =  mt_buff.green_mtx
        green4D        =  mt_buff.green4D
        time_steps     =  np.append(time_steps, imarray_red[:, 0, 0].size)

        try:
            time_step_value  =  TiffFile(str(fnames[0])).lsm_metadata["TimeIntervall"]
        except TypeError:
            time_step_value  =  19.95

        if len(fnames) > 1:
            for s in range(1, len(fnames)):
                mt_buff        =  LoadLsm5D.LoadLsm5D(str(fnames[s]), nucs_spts_ch)
                imarray_red    =  np.concatenate((imarray_red, mt_buff.red_mtx), axis=0)
                imarray_green  =  np.concatenate((imarray_green, mt_buff.green_mtx), axis=0)
                green4D        =  np.concatenate((green4D, mt_buff.green4D), axis=0)
                time_steps     =  np.append(time_steps, imarray_red[:, 0, 0].size)

        imarray_red    =  np.rot90(imarray_red, axes=(1, 2))[:, ::-1, :]
        imarray_green  =  np.rot90(imarray_green, axes=(1, 2))[:, ::-1, :]
        green4D        =  np.rot90(green4D, axes=(2, 3))[:, :, ::-1, :]

        self.imarray_red      =  imarray_red
        self.imarray_green    =  imarray_green
        self.green4D          =  green4D
        self.time_steps       =  time_steps
        self.time_step_value  =  np.round(time_step_value, decimals=3)
        self.pix_size         =  np.round(TiffFile(str(fnames[0])).lsm_metadata["VoxelSizeX"] * 1000000, decimals=4)
