# -*- coding: utf-8 -*-

""" Module summary description.

More detailed description.
"""
from fototex.foto import Foto
from pyrasta.raster import Raster


# foto = Foto("/home/benjamin/Documents/DATA/SENTINEL-2/S2A_MSIL1C_20210718T084601_N0301_R107_T37VEF_20210718T100625"
#             ".SAFE/GRANULE/L1C_T37VEF_A031707_20210718T085326/IMG_DATA/T37VEF_20210718T084601_B03.jp2",
#             in_memory=True, method="block")


image = "/home/benjamin/Documents/DATA/SENTINEL-2" \
        "/S2A_MSIL1C_20210718T084601_N0301_R107_T37VEF_20210718T100625.SAFE/GRANULE" \
        "/L1C_T37VEF_A031707_20210718T085326/IMG_DATA/T37VEF_20210718T084601_B03.jp2"

# raster = Raster(image)

# raster._gdal_dataset.GetProjection()

# log_to_linear = 10 ** (raster / 10)

# raster = 10 ** (Raster(image) / 10)

foto = Foto(image,
            in_memory=True, method="moving")

# root = tkinter.Tk()
# plot(root, foto.dataset, foto.band, reduced_r_spectra, 0.6, 16, "max", 3, [2, 98])
# tkinter.mainloop()

# foto = Foto("/home/benjamin/Documents/PRO/FOTO/Images_entrées_fototex"
#             "/PAN_Mosaic_alizees_SEULEMENT.tif",
#             in_memory=False, data_chunk_size=2000000, method="moving")

foto.run(13, keep_dc_component=False, nb_processes=24)
# foto.out_dir = "/home/benjamin/Documents/PRO/PRODUITS/FOTO_RGB/SENTINEL"
foto.out_dir = "/home/benjamin/Documents/PRO/PRODUITS/FOTO_RADAR/"
# foto.plot(nb_quadrants=8)
# foto.plot("/home/benjamin/Documents/PRO/PRODUITS/FOTO_RGB/SENTINEL"
#           "/T23LKC_20201006T132241_B04_method=block_wsize=19_dc=True_foto_data.h5",
#           nb_quadrants=10, norm_method="max")
foto.save_rgb()
# foto.save_data()
