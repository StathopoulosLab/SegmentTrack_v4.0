import numpy as np
import pyqtgraph as pg
import tifffile
import czifile
from scipy import ndimage
from skimage.filters import threshold_otsu


class FromTile2GlobCoordinate:
    def __init__(self, tile_img):

        # tile_img    =  np.rot90(tile_img)[::-1, :]
        tile_img_f  =  ndimage.filters.gaussian_filter(tile_img, 10)
        val         =  threshold_otsu(tile_img_f)
        mask        =  (tile_img_f > val)

        pts_x         =  np.where(mask.sum(1) != 0)[0]
        start_pts_x   =  pts_x[0]
        lenght_pts_x  =  pts_x[-1] - pts_x[0]

        px_central_img_x  =  int(tile_img.shape[0] / 5)

        perc_first_pts    =  (2 * px_central_img_x - start_pts_x) * 100 / lenght_pts_x
        perc_last_pts     =  (3 * px_central_img_x - start_pts_x) * 100 / lenght_pts_x
        x_coord_cntr_img  =  np.linspace(perc_first_pts, perc_last_pts, px_central_img_x)

        pts_y         =  np.where(mask.sum(0) != 0)[0]
        start_pts_y   =  pts_y[0]
        lenght_pts_y  =  pts_y[-1] - pts_y[0]

        px_central_img_y  =  int(tile_img.shape[1] / 3)

        perc_first_pts    =  (px_central_img_y - start_pts_y) * 100 / lenght_pts_y
        perc_last_pts     =  (2 * px_central_img_y - start_pts_y) * 100 / lenght_pts_y
        y_coord_cntr_img  =  np.linspace(perc_first_pts, perc_last_pts, px_central_img_y)


        pg.image(tile_img)

        self.x_coord_cntr_img  =  x_coord_cntr_img
        self.y_coord_cntr_img  =  y_coord_cntr_img



class FromTile2GlobCoordinateLoader:
    def __init__(self, tile_fname):

        if tile_fname[-3:] == "tif" or tile_fname[-3:] == "lsm":
            tile_img  =  tifffile.imread(str(tile_fname))[0, 0, 1, :, :]

        if tile_fname[-3:] == "czi":
            tile_img  =  np.squeeze(czifile.imread(tile_fname))[1]

        if len(tile_img.shape) > 2:
            tile_mip  =  np.zeros(tile_img.shape[1:])
            for x in range(tile_img.shape[1]):
                tile_mip[x, :]  =  tile_img[:, x, :].max(0)

            tile_img  =  tile_mip

        tile_img  =  np.rot90(tile_img)[::-1, :]

        self.tile_img  =  tile_img
