"""This function loads and concatenates .czi filedata as they come from microscope.

Taking .czi filenames as input, the output are the concatenated matrices of the
maximum intensity projection of red and green channels plus the green channel in
4D (because of 3D detection purpouses). Matrices are also flipped and rotate to
have a visualization conform to ImageJ standards. In order to avoid to use 3D
and 4D matrices for concatenation (cumbersome to handle) the matrices are
always reshaped in a 1D vector, concatenated and reshaped at the end into
a matrix shape.
"""


import numpy as np
from PyQt5 import QtWidgets

import LoadLif5D


class MultiLoadLif5D:
    """Only class, does all the job"""
    def __init__(self, fnames, nucs_spts_ch):

        num_bit  =  NumBit.getNumBit()

        t_steps_done  =  False                                                               # flag for time steps reading
        mt_buff       =  LoadLif5D.LoadLif5D(str(fnames[0]), nucs_spts_ch, num_bit)          # read first .lif file

        imarray_red    =  mt_buff.red_mtx                                                    # separate its different channels 
        imarray_green  =  mt_buff.green_mtx
        green4D        =  mt_buff.green4D

        if len(mt_buff.red_mtx.shape) == 2:                                         # store info about size: if a file has just one time frame, it will have one dimension less
            time_steps           =  1
            z_steps, xlen, ylen  =  green4D.shape

        else:
            time_steps, z_steps, xlen, ylen  =  green4D.shape
            time_step_value                  =  np.round(mt_buff.time_lapse, 2)    # time step value
            t_steps_done                     =  True                               # prevent to read it again from other files (useless)

        imarray_red    =  imarray_red.reshape(imarray_red.size)                     # reshape all the matrix we declare into a 1D vector
        imarray_green  =  imarray_green.reshape(imarray_green.size)
        green4D        =  green4D.reshape(green4D.size)


        if len(fnames) > 1:
            for s in range(1, len(fnames)):                                         # reading further files (if any) 

                mt_buff  =  LoadLif5D.LoadLif5D(str(fnames[s]), nucs_spts_ch, num_bit)
                if len(mt_buff.red_mtx.shape) == 2:                                 # store info about the matrix size                                                            
                    t_steps_bff  =  1
                else:
                    t_steps_bff  =  mt_buff.green4D.shape[0]

                    if t_steps_done is False:                                       # read the time step value on the first file that has more than 1 time frame
                        time_step_value  =  np.round(mt_buff.time_lapse, decimals=2)    # time step value
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

        self.time_steps       =  time_steps
        self.pix_size         =  mt_buff.pix_sizeX
        self.time_step_value  =  time_step_value
        self.imarray_red      =  imarray_red
        self.imarray_green    =  imarray_green
        self.green4D          =  green4D




class NumBit(QtWidgets.QDialog):
    """Dialog widget to set the number of bit"""
    def __init__(self, parent=None):
        super(NumBit, self).__init__(parent)

        title_lbl  =  QtWidgets.QLabel("Choose the number of bits", self)
        title_lbl.setFixedSize(200, 25)

        num_bit_combo = QtWidgets.QComboBox(self)
        num_bit_combo.addItem("8 bit")
        num_bit_combo.addItem("16 bit")
        num_bit_combo.activated[str].connect(self.num_bit_val)
        num_bit_combo.setFixedSize(200, 25)

        cierra_btn  =  QtWidgets.QPushButton("Ok", self)
        cierra_btn.clicked.connect(self.cierra)
        cierra_btn.setFixedSize(200, 25)

        self.num_bit_value  =  np.uint8

        layout  =  QtWidgets.QVBoxLayout()
        layout.addWidget(title_lbl)
        layout.addWidget(num_bit_combo)
        layout.addWidget(cierra_btn)

#         self.setWindowModality(Qt.ApplicationModal)
        self.setLayout(layout)
        self.setGeometry(300, 300, 200, 100)
        self.setWindowTitle("Choose Algorithm")


    def num_bit_val(self, text):
        """Set the values of the combo"""
        if text == "8 bit":
            self.num_bit_value  =  np.uint8
        if text == "16 bit":
            self.num_bit_value  =  np.uint16


    def cierra(self):
        """Close dialog"""
        self.close()


    def num_bit(self):
        """Prepare  value to send"""
        return self.num_bit_value

    @staticmethod
    def getNumBit(parent=None):
        """Send the value"""
        dialog  =  NumBit(parent)
        result  =  dialog.exec_()
#         flag    =  str(dialog.num_bit_value())
        flag    =  dialog.num_bit_value
        return flag

