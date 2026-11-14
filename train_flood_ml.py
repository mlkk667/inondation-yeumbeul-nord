# -*- coding: utf-8 -*-
"""
Pipeline Scientifique de Machine Learning pour la Prédiction des Inondations
Commune de Yeumbeul Nord - Comparaison AHP vs Machine Learning (Random Forest)
Auteur : M. Ndiaye (L3 Géomatique - UAM)
"""

import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import rasterio
from rasterio.warp import reproject, Resampling

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_curve, auc, confusion_matrix, ConfusionMatrixDisplay
)

os.environ['MPLCONFIGDIR'] = os.path.abspath('.matplotlib_cache')
os.makedirs('assets/images', exist_ok=True)
os.makedirs('donnees', exist_ok=True)

# 1. Chargement et Préparation des Données
csv_path = r"donnees_ehant/ehantillons_final.csv"
df = pd.read_csv(csv_path)

# Variables explicatives (Features X) et Cible (Target y)
feature_cols = ['altitude1', 'pente1', 'dd1', 'pedo1', 'ocsol1']
feature_names_fr = ['Altitude (MNT)', 'Pente (%)', 'Densité de Drainage', 'Pédologie (Sols)', 'Occupation du Sol']

X = df[feature_cols].copy()
y = df['label'].copy()

# Séparation Train (80%) / Test (20%) stratifiée
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)

print(f"Échantillons totaux : {len(df)} (Train: {len(X_train)}, Test: {len(X_test)})")

# 2. Entraînement des Modèles
rf_model = RandomForestClassifier(
    n_estimators=150,
    max_depth=8,
    min_samples_split=4,
    random_state=42,
    n_jobs=-1
)
rf_model.fit(X_train, y_train)

gb_model = GradientBoostingClassifier(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=4,
    random_state=42
)
gb_model.fit(X_train, y_train)

# 3. Évaluation sur le jeu de Test
models = {
    'Random Forest': rf_model,
    'Gradient Boosting': gb_model
}

results = {}
for name, model in models.items():
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]
    
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    roc_auc = auc(fpr, tpr)
    
    cv_scores = cross_val_score(model, X, y, cv=5, scoring='roc_auc')
    
    results[name] = {
        'acc': acc, 'prec': prec, 'rec': rec, 'f1': f1, 'auc': roc_auc,
        'cv_auc_mean': cv_scores.mean(), 'cv_auc_std': cv_scores.std(),
        'fpr': fpr, 'tpr': tpr, 'y_pred': y_pred, 'y_prob': y_prob
    }
    
    print(f"\n=== Performances de {name} ===")
    print(f"Accuracy (Justesse)   : {acc*100:.2f} %")
    print(f"Précision             : {prec*100:.2f} %")
    print(f"Rappel (Recall)       : {rec*100:.2f} %")
    print(f"F1-Score              : {f1*100:.2f} %")
    print(f"Score AUC-ROC         : {roc_auc:.4f}")
    print(f"Validation Croisée 5x : {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")

# 4. Graphique 1 : Courbe ROC Comparée
plt.figure(figsize=(8, 6), dpi=300)
for name, res in results.items():
    plt.plot(res['fpr'], res['tpr'], lw=2.5, label=f"{name} (AUC = {res['auc']:.3f})")

plt.plot([0, 1], [0, 1], color='gray', lw=1.5, linestyle='--', label='Hasard pur (AUC = 0.50)')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('Taux de Faux Positifs (1 - Spécificité)', fontsize=12, fontweight='bold')
plt.ylabel('Taux de Vrais Positifs (Sensibilité / Rappel)', fontsize=12, fontweight='bold')
plt.title('Courbe ROC - Modèles de Susceptibilité aux Inondations\nCommune de Yeumbeul Nord', fontsize=13, fontweight='bold', pad=15)
plt.legend(loc="lower right", fontsize=11, frameon=True, shadow=True)
plt.grid(True, linestyle=':', alpha=0.6)
plt.tight_layout()
plt.savefig('assets/images/ml_courbe_roc.png')
plt.close()
print("Graphique ROC sauvegardé : assets/images/ml_courbe_roc.png")

# 5. Graphique 2 : Matrice de Confusion (Random Forest)
cm = confusion_matrix(y_test, results['Random Forest']['y_pred'])
fig, ax = plt.subplots(figsize=(7, 6), dpi=300)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Non inondé (0)', 'Inondé (1)'])
disp.plot(cmap='Blues', ax=ax, values_format='d')
ax.set_title('Matrice de Confusion (Random Forest - Test N=100)\nCommune de Yeumbeul Nord', fontsize=12, fontweight='bold', pad=15)
ax.set_xlabel('Classe Prédite par le Modèle IA', fontsize=11, fontweight='bold')
ax.set_ylabel('Vérité Terrain (Échantillons Validés)', fontsize=11, fontweight='bold')
plt.tight_layout()
plt.savefig('assets/images/ml_matrice_confusion.png')
plt.close()
print("Matrice de confusion sauvegardée : assets/images/ml_matrice_confusion.png")

# 6. Graphique 3 : Importance des Variables (Feature Importance Gini)
importances = rf_model.feature_importances_
indices = np.argsort(importances)[::-1]

plt.figure(figsize=(9, 5.5), dpi=300)
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
bars = plt.bar(range(len(importances)), importances[indices], color=colors, edgecolor='black', alpha=0.85)

for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.01, f"{yval*100:.1f} %", ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.xticks(range(len(importances)), [feature_names_fr[i] for i in indices], rotation=15, ha='right', fontsize=10, fontweight='bold')
plt.ylabel('Importance Relative (Gini / MDI)', fontsize=11, fontweight='bold')
plt.title("Hiérarchie des Facteurs d'Inondation selon l'IA (Random Forest)\nCommune de Yeumbeul Nord", fontsize=12, fontweight='bold', pad=15)
plt.ylim(0, max(importances) + 0.08)
plt.grid(axis='y', linestyle=':', alpha=0.6)
plt.tight_layout()
plt.savefig('assets/images/ml_feature_importance.png')
plt.close()
print("Graphique d'importance sauvegardé : assets/images/ml_feature_importance.png")

# 7. Prédiction Spatiale sur toute la Commune (Génération du Raster ML)
print("\n=== Début de la Prédiction Spatiale sur toute la commune ===")

raster_files = {
    'altitude1': r"donnees_ehant/altitude.tif",
    'pente1': r"donnees_ehant/pente.tif",
    'dd1': r"donnees_ehant/densite_d.tif",
    'pedo1': r"donnees_ehant/pedologie.tif",
    'ocsol1': r"donnees_ehant/ocsol.tif"
}

with rasterio.open(raster_files['altitude1']) as ref_src:
    meta = ref_src.meta.copy()
    ref_shape = ref_src.shape
    ref_transform = ref_src.transform
    ref_crs = ref_src.crs

print(f"Dimensions de référence : {ref_shape[0]} lignes x {ref_shape[1]} colonnes (Résolution 5m)")

raster_arrays = {}
valid_mask = np.ones(ref_shape, dtype=bool)

for feat in feature_cols:
    with rasterio.open(raster_files[feat]) as src:
        if src.shape == ref_shape:
            arr = src.read(1)
        else:
            print(f"Rééchantillonnage de {feat} (shape {src.shape} -> {ref_shape})...")
            arr = np.empty(ref_shape, dtype=np.float32)
            reproject(
                source=rasterio.band(src, 1),
                destination=arr,
                src_transform=src.transform,
                src_crs=src.crs,
                dst_transform=ref_transform,
                dst_crs=ref_crs,
                resampling=Resampling.bilinear
            )
        
        if src.nodata is not None:
            valid_mask &= (arr != src.nodata)
        valid_mask &= ~np.isnan(arr)
        raster_arrays[feat] = arr

N_pixels = ref_shape[0] * ref_shape[1]
pixel_matrix = np.column_stack([raster_arrays[feat].flatten() for feat in feature_cols])
flat_mask = valid_mask.flatten()

valid_pixels = pixel_matrix[flat_mask]
print(f"Pixels valides à prédire : {len(valid_pixels):,} pixels")

print("Calcul des probabilités par Random Forest...")
prob_predictions = rf_model.predict_proba(valid_pixels)[:, 1]

prob_map = np.full(N_pixels, np.nan, dtype=np.float32)
prob_map[flat_mask] = prob_predictions
prob_map_2d = prob_map.reshape(ref_shape)

meta.update({
    'dtype': 'float32',
    'count': 1,
    'nodata': -9999.0
})
prob_map_2d_save = np.nan_to_num(prob_map_2d, nan=-9999.0)

output_tif = r"donnees/carte_susceptibilite_ml.tif"
with rasterio.open(output_tif, 'w', **meta) as dst:
    dst.write(prob_map_2d_save.astype(np.float32), 1)

print(f"Raster de probabilité exporté : {output_tif}")

# 8. Carte Graphique Finale
plt.figure(figsize=(9, 8), dpi=300)
cmap = matplotlib.colormaps['RdYlBu_r']

masked_prob = np.ma.masked_invalid(prob_map_2d)
im = plt.imshow(masked_prob, cmap=cmap, vmin=0, vmax=1)
cbar = plt.colorbar(im, fraction=0.038, pad=0.04)
cbar.set_label("Probabilité d'Inondation Prédite (0.0 = Sûr ➔ 1.0 = Risque Maximal)", fontsize=10, fontweight='bold')

plt.title("Cartographie Prédictive de la Susceptibilité aux Inondations\nModélisation par Machine Learning (Random Forest) - Yeumbeul Nord", fontsize=11, fontweight='bold', pad=15)
plt.axis('off')
plt.tight_layout()
plt.savefig('assets/images/carte_susceptibilite_ml.png', bbox_inches='tight')
plt.close()
print("Carte finale de susceptibilité ML sauvegardée : assets/images/carte_susceptibilite_ml.png")
print("\n=== PIPELINE MACHINE LEARNING TERMINÉ AVEC SUCCÈS TOTAL ! ===")
