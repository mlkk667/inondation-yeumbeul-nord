"""
Script d'échantillonnage stratifié pour le Machine Learning
Projet : Susceptibilité aux inondations - Yeumbeul Nord

Principe :
- Classe 1 (Inondable) : prélèvement aléatoire dans les polygones 'tres eleve' et 'eleve' (DN 4 et 5)
- Classe 0 (Non Inondable) : prélèvement aléatoire dans les polygones 'tres faible' et 'faible' (DN 1 et 2)
- Classe 'moyen' (DN 3) : EXCLUE de l'échantillonnage pour éviter le bruit d'étiquetage (label noise).
- Extraction des covariables depuis les rasters : MNT, Pente, TWI, Densité de drainage
"""

import os
import random
import numpy as np
import pandas as pd
from osgeo import ogr, gdal, osr

gdal.UseExceptions()
ogr.UseExceptions()

# Chemins des fichiers
SHP_PATH = os.path.join('donnees', 'vecteur', 'ahp_final.shp')
RASTERS = {
    'dem': os.path.join('donnees', 'raster', 'raster_re', 're_dem_ynord.tif'),
    'pente': os.path.join('donnees', 'raster', 'raster_re', 're_Pente.tif'),
    'twi': os.path.join('donnees', 'raster', 'raster_re', 're_twi.tif'),
    'dd': os.path.join('donnees', 'raster', 'raster_re', 're_dd.tif')
}
OUTPUT_CSV = os.path.join('donnees', 'echantillons_ml.csv')

def get_raster_value(ds, x, y):
    """Extrait la valeur d'un raster aux coordonnées (x, y)."""
    gt = ds.GetGeoTransform()
    px = int((x - gt[0]) / gt[1])
    py = int((y - gt[3]) / gt[5])
    band = ds.GetRasterBand(1)
    nodata = band.GetNoDataValue()
    if 0 <= px < ds.RasterXSize and 0 <= py < ds.RasterYSize:
        val = band.ReadAsArray(px, py, 1, 1)[0, 0]
        if val != nodata and not np.isnan(val):
            return float(val)
    return None

def sample_points_from_geometry(geom, num_points):
    """Génère des points aléatoires uniformes à l'intérieur d'une géométrie."""
    minx, maxx, miny, maxy = geom.GetEnvelope()
    points = []
    attempts = 0
    max_attempts = num_points * 50
    while len(points) < num_points and attempts < max_attempts:
        attempts += 1
        rx = random.uniform(minx, maxx)
        ry = random.uniform(miny, maxy)
        pt = ogr.Geometry(ogr.wkbPoint)
        pt.AddPoint(rx, ry)
        if geom.Contains(pt):
            points.append((rx, ry))
    return points

def run_sampling(n_samples_per_class=300):
    print("--- Démarrage de l'échantillonnage pour Machine Learning ---")
    ds = ogr.Open(SHP_PATH)
    lyr = ds.GetLayer()

    geom_inondable = ogr.Geometry(ogr.wkbMultiPolygon)
    geom_non_inondable = ogr.Geometry(ogr.wkbMultiPolygon)

    for feat in lyr:
        dn = feat.GetField('DN')
        geom = feat.GetGeometryRef()
        if geom is None:
            continue
        # Cloner et extraire les polygones individuels si MULTIPOLYGON
        subgeoms = []
        if geom.GetGeometryName() == 'MULTIPOLYGON':
            for i in range(geom.GetGeometryCount()):
                subgeoms.append(geom.GetGeometryRef(i).Clone())
        else:
            subgeoms.append(geom.Clone())

        # DN 4 et 5 -> Inondable (Label 1)
        if dn in [4, 5]:
            for g in subgeoms:
                geom_inondable.AddGeometry(g)
        # DN 1 et 2 -> Non Inondable (Label 0)
        elif dn in [1, 2]:
            for g in subgeoms:
                geom_non_inondable.AddGeometry(g)

    geom_inondable = geom_inondable.UnionCascaded()
    geom_non_inondable = geom_non_inondable.UnionCascaded()

    print(f"Génération de {n_samples_per_class} points pour chaque classe (Inondable vs Non Inondable)...")
    pts_1 = sample_points_from_geometry(geom_inondable, n_samples_per_class)
    pts_0 = sample_points_from_geometry(geom_non_inondable, n_samples_per_class)

    print(f"Points générés : {len(pts_1)} (Inondables = 1) | {len(pts_0)} (Non Inondables = 0)")

    # Ouverture des rasters
    raster_ds = {name: gdal.Open(path) for name, path in RASTERS.items() if os.path.exists(path)}

    records = []
    for label, pts in [(1, pts_1), (0, pts_0)]:
        for pid, (x, y) in enumerate(pts):
            row = {'id': len(records) + 1, 'x': x, 'y': y, 'label': label}
            valid = True
            for rname, rds in raster_ds.items():
                val = get_raster_value(rds, x, y)
                if val is None:
                    valid = False
                    break
                row[rname] = val
            if valid:
                records.append(row)

    df = pd.DataFrame(records)
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"Échantillonnage terminé avec succès !")
    print(f"Fichier exporté : {OUTPUT_CSV} ({len(df)} échantillons valides)")
    print("\nAperçu des 5 premières lignes :")
    print(df.head())

if __name__ == '__main__':
    run_sampling(n_samples_per_class=250)
