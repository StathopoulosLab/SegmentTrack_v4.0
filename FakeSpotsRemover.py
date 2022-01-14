import numpy as np


class FakeSpotsRemover:
    def __init__(self, spts_tracked):
        self.spts_tracked  =  spts_tracked    # input[0]

        idxs        =  np.unique(self.spts_tracked)[1:]
        delete_msk  =  np.zeros(self.spts_tracked.shape)

        for k in idxs:
            profile  =  np.sign((self.spts_tracked == k).sum(2).sum(1))
            prof_d2  =  np.diff(profile, 2)
            zero_jj  =  np.where(prof_d2 == -2)[0] + 1

            for l in zero_jj:
                delete_msk[l, :, :]  +=  (self.spts_tracked[l, :, :] == k)

            if profile[0] == 1 and profile[1] == 0:
                delete_msk[0, :, :]  +=  (self.spts_tracked[0, :, :] == k)
            if profile[-1] == 1 and profile[-2] == 0:
                delete_msk[-1, :, :]  +=  (self.spts_tracked[-1, :, :] == k)


        spts_tracked_filtered  =  self.spts_tracked * (1 - delete_msk)

        self.spts_tracked_filtered  =  spts_tracked_filtered
        # self.delete_msk             =  delete_msk



