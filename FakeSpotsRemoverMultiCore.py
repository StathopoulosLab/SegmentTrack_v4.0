import numpy as np
import multiprocessing

import FakeSpotsRemover


class FakeSpotsRemoverMultiCore:
    def __init__(self, spts_tracked):
        self.spts_tracked  =  spts_tracked

        idxs  =  np.unique(self.spts_tracked)[1:]

        cpu_ow      =  multiprocessing.cpu_count()   # - 1  one core left free. Does it takes sense?
        idxs_chops  =  1 + idxs.size / cpu_ow

        a  =  []
        for t in range(cpu_ow - 1):
            a.append(idxs[t * idxs_chops:(t + 1) * idxs_chops])

        a.append(idxs[(t + 1) * idxs_chops:])
        # b         =  self.spots3D_thr * np.ones(len(a))
        job_args  =  []                                                                                                 # creates a list in which any element is a couple
        for k in renge(len(a)):
            job_args  =  np.append(job_args, [self.spts_tracked, a[k]])

        pool     =  multiprocessing.Pool()
        results  =  pool.map(FakeSpotsRemover.FakeSpotsRemover, job_args)

        pool.close()

