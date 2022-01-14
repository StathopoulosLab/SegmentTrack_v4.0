"""This function rescues the raw data of the analysis.

Given the nuclei raw data matrix saved as rescue during the analysis
and the the total raw data, it searches for the cutting 
points and properly cuts the filedata. 
"""


import numpy as np

class RescueRaw:
    def __init__(self, raw_red_rescued, filedata):
        
        sum_diff         =  -10                         # just a non-zero value to start
        start_cut_value  =  -1                          # -1 to start from 0 having the update at the first line
        while sum_diff != 0:
            start_cut_value  +=  1
            sum_diff  =  np.sum(filedata.imarray_red[start_cut_value] - raw_red_rescued[0])     # check if difference is non-zero with the first frame

        sum_diff       =  -10                                               # same things, but with the last frame
        end_cut_value  =  filedata.imarray_red.shape[0]
        while sum_diff != 0:
            end_cut_value  -=  1
            sum_diff  =  np.sum(filedata.imarray_red[end_cut_value] - raw_red_rescued[-1])

        filedata.imarray_red    =  filedata.imarray_red[start_cut_value:end_cut_value + 1]
        filedata.imarray_green  =  filedata.imarray_green[start_cut_value:end_cut_value + 1]
        filedata.green4D        =  filedata.green4D[start_cut_value:end_cut_value + 1]
        
        self.start_cut_value  =  start_cut_value                # output values useful to the save function
        self.end_cut_value    =  end_cut_value
        