import os
from osgeo import gdal, osr

# Image source
src_img = r'C:\Users\malic\.gemini\antigravity\brain\9e1f2eab-f832-4eb3-b774-7501bf20b9e2\.user_uploaded\media_1793872084792_fb040432.jpg'
out_tif = os.path.join('donnees', 'carte_quartiers_georef.tif')

# Points de contrôle (GCPs) calculés précisément à partir de la grille UTM
# (pixel_x, pixel_y) -> (UTM_East, UTM_North)
# x=138 -> 245000, x=305 -> 246000, x=472 -> 247000, x=639 -> 248000, x=806 -> 249000, x=973 -> 250000
# y=62 -> 1637000, y=179 -> 1636300, y=296 -> 1635600, y=413 -> 1634900, y=530 -> 1634200
gcps = [
    gdal.GCP(245000, 1637000, 0, 138, 62),
    gdal.GCP(250000, 1637000, 0, 973, 62),
    gdal.GCP(245000, 1634200, 0, 138, 530),
    gdal.GCP(250000, 1634200, 0, 973, 530),
    gdal.GCP(247000, 1635600, 0, 472, 296),
    gdal.GCP(249000, 1634900, 0, 806, 413),
]

srs = osr.SpatialReference()
srs.ImportFromEPSG(32628) # WGS 84 / UTM Zone 28N

# Ouvrir l'image source
src_ds = gdal.Open(src_img)

# Créer un fichier VRT intermédiaire avec GCPs
temp_vrt = os.path.join('donnees', 'temp_georef.vrt')
vrt_ds = gdal.Translate(temp_vrt, src_ds, outputSRS=srs.ExportToWkt(), GCPs=gcps)
vrt_ds = None

# Reprojeter / Warper pour créer le GeoTIFF géoréférencé parfait
warp_opts = gdal.WarpOptions(dstSRS=srs.ExportToWkt(), resampleAlg='bilinear', format='GTiff')
out_ds = gdal.Warp(out_tif, temp_vrt, options=warp_opts)
out_ds = None

if os.path.exists(temp_vrt):
    os.remove(temp_vrt)

print(f"GeoTIFF géoréférencé créé avec succès : {out_tif}")

