import sys
from osgeo import gdal, ogr, osr

srs = osr.SpatialReference()
srs.ImportFromEPSG(32628)
tgt = osr.SpatialReference()
tgt.ImportFromEPSG(4326)
transform = osr.CoordinateTransformation(srs, tgt)

print("Extent in Lat/Lon:")
print("Bottom-Left:", transform.TransformPoint(227075, 1620465)[:2])
print("Top-Right:", transform.TransformPoint(252515, 1638950)[:2])

print("\n--- oscol classes ---")
ds = ogr.Open("donnees/vecteur/oscol.shp")
lyr = ds.GetLayer()
classes = set()
for f in lyr:
    classes.add(f.GetField("Class_name"))
print(classes)

print("\n--- pedologie classes ---")
ds2 = ogr.Open("donnees/vecteur/pedologie.shp")
lyr2 = ds2.GetLayer()
peds = set()
for f in lyr2:
    peds.add(f.GetField("MSDNOM"))
print(peds)
