import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Configuration du dossier temporaire pour matplotlib
os.environ['MPLCONFIGDIR'] = os.path.join(os.getcwd(), '.matplotlib_cache')
os.makedirs(os.environ['MPLCONFIGDIR'], exist_ok=True)

# Charger les données
csv_path = os.path.join('donnees', 'ahp_diagramme.csv')
df = pd.read_csv(csv_path)

# Ordre logique des classes de susceptibilité
class_order = {
    1: ('Très faible', '#228B22'),    # Forest green
    2: ('Faible', '#90EE90'),         # Light green
    3: ('Moyen', '#FFFF00'),          # Yellow
    4: ('Élevé', '#FF7F0E'),          # Orange
    5: ('Très élevé', '#D62728')      # Red
}

# Mapper les noms et couleurs
df['ordre'] = df['DN']
df = df.sort_values('ordre')
labels = [class_order[dn][0] for dn in df['DN']]
colors = [class_order[dn][1] for dn in df['DN']]
values = df['surface_perc'].values

# Création du graphique en barres horizontales + annotations
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5), dpi=300)

# 1. Bar plot
bars = ax1.barh(labels, values, color=colors, edgecolor='#333333', linewidth=1.2, height=0.6)
ax1.set_xlabel('Proportion de la surface communale (%)', fontsize=11, fontweight='bold', labelpad=10)
ax1.set_title('Répartition des classes de susceptibilité\n(Commune de Yeumbeul Nord)', fontsize=12, fontweight='bold', pad=12)
ax1.set_xlim(0, max(values) + 10)
ax1.grid(axis='x', linestyle='--', alpha=0.5)

# Valeurs affichées au bout des barres
for bar in bars:
    w = bar.get_width()
    ax1.text(w + 1.0, bar.get_y() + bar.get_height()/2, f'{w:.2f} %',
             ha='left', va='center', fontsize=10, fontweight='bold', color='#222222')

ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

# 2. Donut plot (camembert moderne)
wedges, texts, autotexts = ax2.pie(
    values, 
    labels=labels, 
    colors=colors, 
    autopct='%1.1f%%', 
    pctdistance=0.8,
    startangle=140,
    wedgeprops=dict(width=0.42, edgecolor='#333333', linewidth=1),
    textprops=dict(fontsize=9, fontweight='bold')
)
for at in autotexts:
    at.set_fontsize(9)
    at.set_fontweight('bold')
ax2.set_title('Part relative des surfaces par classe', fontsize=12, fontweight='bold', pad=12)

plt.tight_layout()

# Sauvegarde
out_dir = os.path.join('donnees', 'figures')
os.makedirs(out_dir, exist_ok=True)
out_file = os.path.join(out_dir, 'repartition_susceptibilite.png')
plt.savefig(out_file, dpi=300, bbox_inches='tight')
print(f"Graphique sauvegardé avec succès dans: {out_file}")

