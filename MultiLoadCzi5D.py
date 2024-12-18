"""This function loads and concatenates .czi filedata as they come from microscope.

Taking .czi filenames as input, the output are the concatenated matrices of the
maximum intensity projection of red and green channels plus the green channel in
4D (because of 3D detection purpouses). Matrices are also flipped and rotate to
have a visualization conform to ImageJ standards. In order to avoid to use 3D
and 4D matrices for concatenation (cumbersome to handle) the matrices are
always reshaped in a 1D vector, concatenated and reshaped at the end into
a matrix shape.
"""


# import multiprocessing
import numpy as np
from czifile import CziFile
from natsort import natsorted

import LoadCzi5D

from xml.etree import ElementTree as ET


class MultiProcLoadCzi5D:
    """Multiprocesses the load multi czi function"""
    def __init__(self, fnames, nucs_spts_ch):

        # fnames        =  fnames_chs[0]
        # nucs_spts_ch  =  fnames_chs[1]

        fnames  =  natsorted(fnames, key=lambda y: y.lower())                           # natural order for file names

        if len(fnames) > 0:                                                             # it can be zero when used in multiprocessing
            t_steps_done  =  False                                                      # flag for time steps reading
            mt_buff       =  LoadCzi5D.LoadCzi5D(str(fnames[0]), nucs_spts_ch)          # read first .czi file

            imarray_red    =  mt_buff.red_mtx                                           # separate its different channels
            imarray_green  =  mt_buff.green_mtx
            green4D        =  mt_buff.green4D

            if len(mt_buff.red_mtx.shape) == 2:                                         # store info about size: if a file has just one time frame, it will have one dimension less
                time_steps           =  1
                z_steps, xlen, ylen  =  green4D.shape
            else:
                time_steps, z_steps, xlen, ylen  =  green4D.shape
                with CziFile(str(fnames[0])) as czi:
                    for attachment in czi.attachments():
                        if attachment.attachment_entry.name == 'TimeStamps':
                            timestamps  =  attachment.data()
                            break
                    else:
                        raise ValueError('TimeStamps not found')

                time_step_value  =  np.round(timestamps[1] - timestamps[0], 2)    # time step value
                t_steps_done     =  True                                          # prevent to read it again from other files (useless)

            imarray_red    =  imarray_red.reshape(imarray_red.size)                     # reshape all the matrix we declare into a 1D vector
            imarray_green  =  imarray_green.reshape(imarray_green.size)
            green4D        =  green4D.reshape(green4D.size)

            if len(fnames) > 1:
                for s in range(1, len(fnames)):                                         # reading further files (if any)

                    mt_buff  =  LoadCzi5D.LoadCzi5D(str(fnames[s]), nucs_spts_ch)
                    if len(mt_buff.red_mtx.shape) == 2:                                 # store info about the matrix size
                        t_steps_bff  =  1
                    else:
                        t_steps_bff  =  mt_buff.green4D.shape[0]

                        if t_steps_done is False:                                       # read the time step value on the first file that has more than 1 time frame
                            with CziFile(str(fnames[s])) as czi:
                                for attachment in czi.attachments():
                                    if attachment.attachment_entry.name == 'TimeStamps':
                                        timestamps = attachment.data()
                                        break
                                else:
                                    raise ValueError('TimeStamps not found')

                            time_step_value  =  np.round(timestamps[1] - timestamps[0], 2)    # time step value
                            t_steps_done     =  True                                          # prevent to read it again from other files (useless)

                    imarray_red    =  np.append(imarray_red, mt_buff.red_mtx.reshape(mt_buff.red_mtx.size))                      # append new data to previous
                    imarray_green  =  np.append(imarray_green, mt_buff.green_mtx.reshape(mt_buff.green_mtx.size))
                    green4D        =  np.append(green4D, mt_buff.green4D.reshape(mt_buff.green4D.size))

                    time_steps  +=  t_steps_bff

            imarray_red    =  imarray_red.reshape((time_steps, xlen, ylen))                                                     # final reshape of the matrioces
            imarray_green  =  imarray_green.reshape((time_steps, xlen, ylen))
            green4D        =  green4D.reshape((time_steps, z_steps, xlen, ylen))

            imarray_red    =  np.rot90(imarray_red, axes=(1, 2))[:, ::-1, :]                                                    # rotation to adapt to the imageJ format
            imarray_green  =  np.rot90(imarray_green, axes=(1, 2))[:, ::-1, :]
            green4D        =  np.rot90(green4D, axes=(2, 3))[:, :, ::-1, :]

            a      =  CziFile(str(fnames[0]))                                                                                   # read info about pixel size
            b      =  a.metadata()

            # in place of the original code, extract the pixel scaling from the Metadata's Scaling section
            # In our case, the Metadata is expressed as an string of XML, which we must parse
            pix_size = 0.
            pix_size_Z = 0.
            xmlRoot = ET.fromstring(b)
            for scaling in xmlRoot.iter("Scaling"):
                for axis in scaling.iter("Distance"):
                    if axis.attrib["Id"] == "X":
                        pix_size = np.round(float(axis.find('Value').text) * 1000000., decimals=4)
                    elif axis.attrib["Id"] == 'Z':
                        pix_size_Z = np.round(float(axis.find('Value').text) * 1000000., decimals=4)

            # crash here if the metadata did't have what we need in the form we expect
            assert isinstance(pix_size, float) and pix_size > 0.
            assert isinstance(pix_size_Z, float) and pix_size_Z > 0.

            # start     =  b.find("ScalingX")
            # end       =  b[start + 9:].find("ScalingX")
            # pix_size  =  np.round(float(b[start + 9:start + 7 + end]) * 1000000, decimals=4)

            # start_Z     =  b.find("ScalingZ")
            # end_Z       =  b[start_Z + 9:].find("ScalingZ")
            # pix_size_Z  =  np.round(float(b[start_Z + 9:start_Z + 7 + end_Z]) * 1000000, decimals=4)

            self.time_steps       =  time_steps
            self.pix_size         =  pix_size
            self.pix_size_Z       =  pix_size_Z
            self.time_step_value  =  time_step_value
            self.imarray_red      =  imarray_red
            self.imarray_green    =  imarray_green
            self.green4D          =  green4D

        # cpu_ow      =  multiprocessing.cpu_count()  # number of cpu
        # job_args    =  list()  # initialize the list of input arguments
        # fnames      =  natsorted(fnames, key=lambda y: y.lower())  # natural order for file names
        # idxs_chops  =  np.array_split(fnames, cpu_ow)  # split the number of filenames in nearly equal lenght sub-lists

        # for idxs_chop in idxs_chops:
        #     job_args.append([list(idxs_chop), nucs_spts_ch])  # organize input arguments

        # pool     =  multiprocessing.Pool()
        # results  =  pool.map(MultiLoadCzi5D, job_args)
        # pool.close()

        # imarray_red    =  results[0].imarray_red  # organize results: initilize the finale matrix: THIS MAY BUG IF YOU A FILE WITH A SINGLE TIME FRAME
        # imarray_green  =  results[0].imarray_green
        # green4D        =  results[0].green4D

        # for k in results[1:]:  # concatenate results
        #     if hasattr(k, "imarray_red"):  # if you have less files than cpu, some entries can be empty and the software crushes
        #         imarray_red    =  np.concatenate([imarray_red, k.imarray_red])
        #         imarray_green  =  np.concatenate([imarray_green, k.imarray_green])
        #         green4D        =  np.concatenate([green4D, k.green4D])
        #     else:
        #         break

        # self.time_steps       =  imarray_red.shape[0]
        # self.pix_size         =  results[0].pix_size
        # self.time_step_value  =  results[0].time_step_value
        # self.imarray_red      =  imarray_red
        # self.imarray_green    =  imarray_green
        # self.green4D          =  green4D


class MultiLoadCzi5D:
    """Core of multi loading function"""
    def __init__(self, fnames_chs):

        fnames        =  fnames_chs[0]
        nucs_spts_ch  =  fnames_chs[1]

        if len(fnames) > 0:                                                             # it can be zero when used in multiprocessing
            t_steps_done  =  False                                                      # flag for time steps reading
            mt_buff       =  LoadCzi5D.LoadCzi5D(str(fnames[0]), nucs_spts_ch)          # read first .czi file

            imarray_red    =  mt_buff.red_mtx                                           # separate its different channels
            imarray_green  =  mt_buff.green_mtx
            green4D        =  mt_buff.green4D

            if len(mt_buff.red_mtx.shape) == 2:                                         # store info about size: if a file has just one time frame, it will have one dimension less
                time_steps           =  1
                z_steps, xlen, ylen  =  green4D.shape
            else:
                time_steps, z_steps, xlen, ylen  =  green4D.shape
                with CziFile(str(fnames[0])) as czi:
                    for attachment in czi.attachments():
                        if attachment.attachment_entry.name == 'TimeStamps':
                            timestamps  =  attachment.data()
                            break
                    else:
                        raise ValueError('TimeStamps not found')

                time_step_value  =  np.round(timestamps[1] - timestamps[0], 2)    # time step value
                t_steps_done     =  True                                          # prevent to read it again from other files (useless)

            imarray_red    =  imarray_red.reshape(imarray_red.size)                     # reshape all the matrix we declare into a 1D vector
            imarray_green  =  imarray_green.reshape(imarray_green.size)
            green4D        =  green4D.reshape(green4D.size)

            if len(fnames) > 1:
                for s in range(1, len(fnames)):                                         # reading further files (if any)

                    mt_buff  =  LoadCzi5D.LoadCzi5D(str(fnames[s]), nucs_spts_ch)
                    if len(mt_buff.red_mtx.shape) == 2:                                 # store info about the matrix size
                        t_steps_bff  =  1
                    else:
                        t_steps_bff  =  mt_buff.green4D.shape[0]

                        if t_steps_done is False:                                       # read the time step value on the first file that has more than 1 time frame
                            with CziFile(str(fnames[s])) as czi:
                                for attachment in czi.attachments():
                                    if attachment.attachment_entry.name == 'TimeStamps':
                                        timestamps = attachment.data()
                                        break
                                else:
                                    raise ValueError('TimeStamps not found')

                            time_step_value  =  np.round(timestamps[1] - timestamps[0], 2)    # time step value
                            t_steps_done     =  True                                          # prevent to read it again from other files (useless)

                    imarray_red    =  np.append(imarray_red, mt_buff.red_mtx.reshape(mt_buff.red_mtx.size))                      # append new data to previous
                    imarray_green  =  np.append(imarray_green, mt_buff.green_mtx.reshape(mt_buff.green_mtx.size))
                    green4D        =  np.append(green4D, mt_buff.green4D.reshape(mt_buff.green4D.size))

                    time_steps  +=  t_steps_bff

            imarray_red    =  imarray_red.reshape((time_steps, xlen, ylen))                                                     # final reshape of the matrioces
            imarray_green  =  imarray_green.reshape((time_steps, xlen, ylen))
            green4D        =  green4D.reshape((time_steps, z_steps, xlen, ylen))

            imarray_red    =  np.rot90(imarray_red, axes=(1, 2))[:, ::-1, :]                                                    # rotation to adapt to the imageJ format
            imarray_green  =  np.rot90(imarray_green, axes=(1, 2))[:, ::-1, :]
            green4D        =  np.rot90(green4D, axes=(2, 3))[:, :, ::-1, :]

            a      =  CziFile(str(fnames[0]))                                                                                   # read info about pixel size
            b      =  a.metadata()

            start     =  b.find("ScalingX")
            end       =  b[start + 9:].find("ScalingX")
            pix_size  =  np.round(float(b[start + 9:start + 7 + end]) * 1000000, decimals=4)

            start_Z     =  b.find("ScalingZ")
            end_Z       =  b[start_Z + 9:].find("ScalingZ")
            pix_size_Z  =  np.round(float(b[start_Z + 9:start_Z + 7 + end_Z]) * 1000000, decimals=4)

            self.time_steps       =  time_steps
            self.pix_size         =  pix_size
            self.pix_size_Z       =  pix_size_Z
            self.time_step_value  =  time_step_value
            self.imarray_red      =  imarray_red
            self.imarray_green    =  imarray_green
            self.green4D          =  green4D
