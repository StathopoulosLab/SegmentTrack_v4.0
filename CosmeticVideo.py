"""This script generates nice false colored video.

"""

import tifffile
import numpy as np


analysis_folder  =  '/home/atrullo/VirginiaColour/snaTATAmut'
raw_data         =  np.fromfile(analysis_folder + '/raw_data_nuclei.bin', 'uint16')
raw_data         =  raw_data[3:].reshape((raw_data[2], raw_data[1], raw_data[0])).astype(np.float)
raw_data         =  (255 * raw_data / raw_data.max()).astype(np.uint32)
falsevideo       =  tifffile.imread(analysis_folder + '/false_2colors.tiff')

false_nice               =  np.zeros(falsevideo.shape, dtype=np.uint32)
false_nice[:, :, :, 2]  +=  (falsevideo[:, :, :, 2] == 255) * raw_data
false_nice[:, :, :, 0]  +=  (falsevideo[:, :, :, 0] == 255) * raw_data * (1 - (falsevideo.sum(3) == 510)).astype(np.uint32)
false_nice[:, :, :, 1]  +=  (falsevideo[:, :, :, 0] == 255) * raw_data * (1 - (falsevideo.sum(3) == 510)).astype(np.uint32)
false_nice[:, :, :, 2]  +=  (falsevideo[:, :, :, 0] == 255) * raw_data * (1 - (falsevideo.sum(3) == 510)).astype(np.uint32)
false_nice[:, :, :, 0]  +=  np.uint32(255) * (falsevideo.sum(3) == 510)

fname  =  analysis_folder[-analysis_folder[::-1].find("/"):]

tifffile.imwrite(analysis_folder + "/false_MultiColors_" + fname + ".tif", np.rot90(false_nice[:, :, ::-1, :], axes=(1, 2)).astype("uint8"))



