import numpy as np
cimport numpy as np

DTYPE = np.int
ctypedef np.int_t DTYPE_t


cpdef Distance3D(list pt_start, np.ndarray[DTYPE_t, ndim=2] spots_ctrs_t, int dist_thr):

    cdef np.ndarray[DTYPE_t, ndim=1] dists = np.zeros([spots_ctrs_t.shape[0]], dtype=np.int)
    cdef int k, idx
    cdef int dis_size = spots_ctrs_t.shape[0]

    for k in range(dis_size):
        dists[k] = np.sum((pt_start[0] - spots_ctrs_t[k, 1]) ** 2 + (pt_start[1] - spots_ctrs_t[k, 2]) ** 2 + (pt_start[2] - spots_ctrs_t[k, 3]) ** 2)

    if dists.min() < dist_thr:
        idx  =  np.argmin(dists)
    else:
        idx  =  -1

    return idx

