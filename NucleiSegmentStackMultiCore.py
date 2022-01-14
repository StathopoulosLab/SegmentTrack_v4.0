"""This function segments nuclei.

It takes as input the matrix of the detected nuclei (black&white) and segments them
with circularity and the watershad algorithm. Other inputs are circularity
threshold and lpm. The function that really performs the segmentation is
NucleiSegment, this function serves just to set the multiprocessing.
"""


import multiprocessing
import numpy as np

import NucleiSegment


class NucleiSegmentStackMultiCore:
    """Main class, coordinates the action in a multiprocessing pool"""
    def __init__(self, labbs, circ_thr, lmp):

        cpu_ow   =  multiprocessing.cpu_count()
        t_chops  =  1 + labbs.shape[0] // cpu_ow

        a  =  []
        for t in range(cpu_ow - 1):
            a.append(labbs[t * t_chops:(t + 1) * t_chops, :, :])                # in the multiprocessing pool each core will work on a certain number of frames: here we chop the frames

        a.append(labbs[(t + 1) * t_chops:, :, :])
        job_args  =  []
        for k in range(cpu_ow):
            job_args.append([a[k], circ_thr, lmp])                              # creates a list in which any element is a triple

        pool     =  multiprocessing.Pool()
        results  =  pool.map(NucleiSegmentStackCoordinator, job_args)
        pool.close()

        nuclei_labels  =  results[0].nuclei_labels                              # concatenates the results of the pool
        for k in range(1, len(results)):
            if results[k].nuclei_labels.shape[0] != 0:
                nuclei_labels  =  np.concatenate((nuclei_labels, results[k].nuclei_labels), axis=0)

        self.nuclei_labels  =  nuclei_labels.astype(np.uint32)


class NucleiSegmentStackCoordinator:
    """Class that actually segments the nuclei"""
    def __init__(self, input_data):
        frames    =  input_data[0]
        circ_thr  =  input_data[1]
        lmp       =  np.int(input_data[2])

        nuclei_labels  =  np.zeros(frames.shape, dtype=np.uint32)

        for j in range(frames.shape[0]):
            nuclei_labels[j, :, :]  =  NucleiSegment.NucleiSegment(frames[j, :, :], circ_thr, lmp).lbl_fin

        self.nuclei_labels  =  nuclei_labels





