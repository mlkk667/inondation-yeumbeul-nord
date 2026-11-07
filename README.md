# Évaluation de la Susceptibilité aux Inondations par Analyse Spatiale Multicritère (AHP)
### Application à la Commune de Yeumbeul Nord (Dakar, Sénégal)

> **Projet académique** : Licence 3 Géomatique – Département Géosciences Appliquées et Environnement  
> **Auteur** : M. Ndiaye  
> **Cadre technique** : SIG, Télédétection & Analyse Multicritère Hiérarchique (AHP)  
> **Système de Coordonnées de Référence (SCR)** : WGS 84 / UTM Zone 28N (EPSG: 32628)  
> **Sources des données spatiales** : ANAT, GEOSENEGAL, CSE, SRTM / MNT local

---

## Résumé Exécutif

Ce projet a pour objectif d'évaluer et de cartographier la susceptibilité aux inondations dans la **commune de Yeumbeul Nord** par une méthode d'**Analyse Multicritère Hiérarchique (AHP - Analytic Hierarchy Process)** développée par Saaty. Face aux inondations récurrentes qui paralysent régulièrement cette zone de la banlieue dakaroise, cinq facteurs géo-environnementaux conditionnants majeurs ont été extraits, standardisés et combinés : l'**altitude**, la **pente**, la **densité de drainage**, la **pédologie (types de sol)** et l'**occupation du sol**. Les résultats mettent en évidence une répartition spatiale contrastée, dominée par une classe de susceptibilité moyenne (65.98 %), mais avec plus de 28.6 % du territoire communal classé en susceptibilité élevée à très élevée. Ce document constitue la base cartographique présentée en classe, et pose les fondements méthodologiques pour de futurs travaux d'automatisation prédictive par **Machine Learning**.

> ⚠️ *Note sur les limites administratives* : Les découpages communaux utilisés dans cette version préliminaire sont en cours de révision en concertation avec les services techniques municipaux.

---

## 1. Introduction

Les inondations font partie des risques naturels les plus destructeurs au monde **(Li, 2026)**. Elles sont caractérisées par la submersion temporaire d'une zone par l'eau. La complexité de lutter contre ce risque réside dans le fait qu'il existe différents types d'inondations : urbaines, torrentielles, fluviales, côtières, pluviales ainsi que les inondations par remontée de nappe phréatique. Il est impératif de trouver des moyens d'anticiper cet aléa car il constitue une menace directe pour les enjeux humains, la salubrité publique, les biens matériels, les infrastructures et les activités économiques.

L'épisode de la sécheresse des années 1970 marque un tournant majeur dans l'urbanisation de la presqu'île de Dakar. Pour fuir les famines occasionnées par ce déficit pluviométrique prolongé au Sahel, les populations des milieux ruraux ont afflué massivement vers la capitale. La périphérie dakaroise a ainsi été occupée de manière informelle et spontanée. Cependant, ces installations n'ont pas toujours respecté les règles de planification urbaine : les nouveaux arrivants se sont majoritairement installés dans des bas-fonds et d'anciens plans d'eau temporairement asséchés (les Niayes). Avec le retour progressif de cycles pluviométriques normaux à humides depuis les années 2000, ces zones se sont révélées extrêmement vulnérables aux inondations à la moindre averse. 

C'est particulièrement le cas de la **commune de Yeumbeul Nord**, une zone d'expansion urbaine dense qui fait face régulièrement à des crises hydrologiques majeures, dont les épisodes historiques les plus marquants restent ceux de 2005, 2009 et 2012 **(Sy, 2019)**. Plusieurs études de référence ont déjà été réalisées sur cette commune, notamment les travaux fondateurs de **M. Diongue (2014)** et du **Dr Bocar Sy (2019)**. 
Le présent travail s'inscrit dans cette lignée en mobilisant les outils modernes de la géomatique. Il vise à répondre à la question suivante : **Comment l'Analyse Multicritère Hiérarchique (AHP) permet-elle de discriminer et de quantifier objectivement les zones de susceptibilité aux inondations à Yeumbeul Nord, et comment cette modélisation peut-elle servir de socle pour de futures approches prédictives par apprentissage automatique ?**

---

## 2. Présentation de la Zone d'Étude

La commune de Yeumbeul Nord est située dans la région de Dakar, au cœur du département de Keur Massar (anciennement rattaché à Pikine). Elle s'étend entre les coordonnées UTM Zone 28N : X compris entre 245 000 m et 250 000 m, et Y compris entre 1 634 000 m et 1 637 500 m.

| Paramètre | Caractéristique |
| :--- | :--- |
| **Entité administrative** | Commune de Yeumbeul Nord, Région de Dakar, Sénégal |
| **Cadre géomorphologique** | Système des Niayes (alternance de dunes et de dépressions) |
| **Altitude minimale** | **1.61 m** (Cuvettes et abords du lac Warouwaye) |
| **Altitude maximale** | **11.53 m** (Crêtes des cordons dunaires) |
| **Régime hydrologique** | Bassin endoréique sans exutoire naturel direct vers la mer |
| **Facteurs aggravants** | Nappe phréatique sub-affleurante, forte imperméabilisation du bâti |

![Carte de Localisation et Topographie](assets/images/carte_localisation.jpg)
*Figure 1 : Carte de situation régionale et modèle altimétrique de Yeumbeul Nord.*

La morphologie de Yeumbeul Nord est dominée par des dunes de sable ogoliennes orientées NNE-SSW séparées par des dépressions interdunaires fermées. Le **lac Warouwaye**, situé au nord-ouest de la commune, constitue le point bas de convergence des eaux de ruissellement et de résurgence de la nappe superficielle.

---

## 3. Données d'Entrée et Facteurs Conditionnants

Conformément aux standards de la littérature scientifique en modélisation des inondations, cinq facteurs conditionnants géo-environnementaux ont été sélectionnés, préparés sous QGIS et standardisés selon une échelle commune de **1 à 5** (où 1 correspond à une susceptibilité très faible et 5 à une susceptibilité très élevée).




### 3.1 Facteur 1 : L'Altitude (Modèle Numérique de Terrain)
L'altitude est le facteur physique directeur. L'eau s'accumule sous l'effet de la gravité dans les points bas topographiques. Les zones situées entre **0 et 3 mètres** (en rouge) représentent le cœur des dépressions et reçoivent la note maximale (**5**). Les altitudes supérieures à **12 mètres** (en vert foncé) représentent les crêtes dunaires à l'abri des submersions (note **1**).

| Tranche d'altitude (m) | Note de susceptibilité | Niveau de risque |
| :---: | :---: | :--- |
| **0 – 3 m** | **5** | Très élevé |
| **3 – 6 m** | **4** | Élevé |
| **6 – 9 m** | **3** | Moyen |
| **9 – 12 m** | **2** | Faible |
| **12 – 15 m** | **1** | Très faible |

![Altitude Reclassifiée](assets/images/critere_altitude_reclassifiee.jpg)
*Figure 2 : Carte de l'altitude reclassifiée (MNT).*

---

### 3.2 Facteur 2 : La Pente du Terrain (Slope)
La pente contrôle directement la vitesse d'écoulement de l'eau. Sur les surfaces planes (inférieures à 2 %), le ruissellement est quasi nul, favorisant une stagnation prolongée des eaux pluviales. Les pentes plus fortes favorisent une évacuation gravitaire rapide vers les bas-fonds.

| Tranche de pente (%) | Note de susceptibilité | Niveau de risque |
| :---: | :---: | :--- |
| **≤ 2 %** | **5** | Très élevé (Stagnation maximale) |
| **2 – 4 %** | **4** | Élevé |
| **4 – 6 %** | **3** | Moyen |
| **6 – 7.5 %** | **2** | Faible |
| **> 7.5 %** | **1** | Très faible (Écoulement rapide) |

![Pente Reclassifiée](assets/images/critere_pente_reclassifiee.jpg)
*Figure 3 : Carte des pentes reclassifiées.*

---

### 3.3 Facteur 3 : La Densité de Drainage
La densité de drainage (km/km²) mesure la concentration linéaire des axes d'écoulement et des ravines par unité de surface. Une forte densité indique une forte convergence des flux d'eaux pluviales vers un secteur réduit.

| Densité (km/km²) | Note de susceptibilité | Niveau de risque |
| :---: | :---: | :--- |
| **9 – 13** | **5** | Très élevé (Convergence intense) |
| **7 – 9** | **4** | Élevé |
| **5 – 7** | **3** | Moyen |
| **3 – 5** | **2** | Faible |
| **1 – 3** | **1** | Très faible |

![Densité de Drainage](assets/images/critere_densite_drainage.png)
*Figure 4 : Carte de la densité de drainage reclassifiée.*

---

### 3.4 Facteur 4 : La Pédologie (Types de Sols)
La perméabilité et la capacité d'infiltration dépendent directement de la nature lithologique des sols :
- **Sols hydromorphes (Note 5 - Rouge)** : Présents dans l'axe central des dépressions, ces sols sont constamment saturés d'eau, argileux et quasiment imperméables.
- **Sols ferrugineux tropicaux (Note 2 - Vert clair)** : Sols sableux-limoneux de pente à infiltration modérée.
- **Dunes littorales (Note 1 - Vert foncé)** : Sables marins grossiers très filtrants à forte capacité d'absorption.

| Type de sol | Note de susceptibilité | Degré de perméabilité |
| :--- | :---: | :--- |
| **Hydromorphes** | **5** | Imperméable / Nappe saturée |
| **Ferrugineux tropicaux** | **2** | Perméabilité moyenne |
| **Dunes littorales** | **1** | Très perméable / Filtrant |

![Pédologie](assets/images/critere_pedologie.jpg)
*Figure 5 : Carte pédologique reclassifiée.*

---

### 3.5 Facteur 5 : L'Occupation du Sol (LULC)
L'état de surface influe sur le coefficient de ruissellement et le taux d'imperméabilisation :
- **Mares et plans d'eau (Note 5 - Rouge)** : Surfaces constamment submergées (Lac Warouwaye et cuvettes pérennes).
- **Savane arbustive (Note 4 - Orange)** : Sols nus ou semi-végétalisés sujets au ruissellement.
- **Steppe arbustive (Note 3 - Jaune)** : Végétation clairsemée.
- **Localité / Tissu bâti (Note 2 - Vert clair)** : Zones d'habitat consolidées sur cordons sableux.
- **Cultures maraîchères (Note 1 - Vert foncé)** : Espaces agraires sableux ouverts des Niayes.

| Classe d'occupation | Note de susceptibilité | Impact hydrologique |
| :--- | :---: | :--- |
| **Mare, lac** | **5** | Submersion permanente |
| **Savane arbustive** | **4** | Ruissellement important |
| **Steppe arbustive** | **3** | Infiltration modérée |
| **Localité (bâti)** | **2** | Tissu habité |
| **Culture maraîchère** | **1** | Espace ouvert perméable |

![Occupation du Sol](assets/images/critere_occupation_sol.jpg)
*Figure 6 : Carte de l'occupation du sol reclassifiée.*

---

## 4. Méthodologie : L'Analyse Multicritère Hiérarchique (AHP)

La méthode AHP développée par Thomas Saaty (1980) repose sur la comparaison par paires des critères afin d'établir une hiérarchie de pondération rationnelle et mathématiquement vérifiée.

### 4.1 Matrice de Comparaison par Paires (MCPP)
L'importance relative des critères a été évaluée selon l'échelle standard de Saaty (de 1 = importance égale à 9 = importance absolue) :

| Critères | Altitude | Pente | Densité Drainage | Pédologie | Occupation Sol |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Altitude** | 1.000 | 2.000 | 3.000 | 4.000 | 5.000 |
| **Pente** | 0.500 | 1.000 | 2.000 | 3.000 | 4.000 |
| **Densité Drainage** | 0.333 | 0.500 | 1.000 | 2.000 | 3.000 |
| **Pédologie** | 0.250 | 0.333 | 0.500 | 1.000 | 2.000 |
| **Occupation Sol** | 0.200 | 0.250 | 0.333 | 0.500 | 1.000 |

### 4.2 Vecteur des Poids  et Validation de Cohérence
Après normalisation par colonne et calcul de la moyenne géométrique de chaque ligne, les poids relatifs obtenus sont :

| Facteur conditionnant | Poids relatif (%) | Poids décimal appliqué |
| :--- | :---: | :---: |
| **Altitude (MNT)** | **41.62 %** | 0.4162 |
| **Pente du terrain** | **26.18 %** | 0.2618 |
| **Densité de drainage** | **16.10 %** | 0.1610 |
| **Pédologie (Types de sol)** | **9.86 %** | 0.0986 |
| **Occupation du sol (LULC)** | **6.24 %** | 0.0624 |
| **TOTAL** | **100.00 %** | **1.0000** |

#### Test de cohérence mathématique de Saaty :
- **Nombre de critères (n)** = 5
- **Valeur propre maximale (λ max)** = **5.0678**
- **Indice de Cohérence (CI)** :  
  `CI = (λ max - n) / (n - 1) = (5.0678 - 5) / 4 = 0.0169`
- **Indice Aléatoire (RI)** pour 5 critères : **1.12**
- **Ratio de Cohérence (CR)** :  
  `CR = CI / RI = 0.0169 / 1.12 = 0.0151` (soit **1.51 %**)

> **Validation** : Le ratio de cohérence (**CR = 1.51 %**) est largement inférieur au seuil critique de **10 %** (CR < 0.10). Les jugements de la matrice de Saaty sont donc parfaitement cohérents et mathématiquement validés.

### 4.3 Combinaison Linéaire Pondérée (WLC)
L'intégration spatiale a été exécutée dans la calculatrice raster de QGIS selon l'équation de Combinaison Linéaire Pondérée (*Weighted Linear Combination*) :

```plaintext
Score AHP = (0.4162 × Altitude) + (0.2618 × Pente) + (0.1610 × Densité Drainage) + (0.0986 × Pédologie) + (0.0624 × Occupation)
```

---

## 5. Résultats et Analyse Spatiale

Le raster continu résultant de l'AHP a été discrétisé en **5 classes de susceptibilité** par la méthode des seuils naturels (Jenks) :

![Carte Finale de Susceptibilité AHP](assets/images/carte_susceptibilite.jpg)
*Figure 7 : Carte globale de susceptibilité aux inondations de Yeumbeul Nord.*

### 5.1 Répartition Surfacique des Classes
Le calcul zonal sur l'emprise communale révèle la distribution suivante :

| Classe DN | Degré de Susceptibilité | Proportion (%) | Interprétation territoriale |
| :---: | :--- | :---: | :--- |
| **1** | **Très faible** | **0.29 %** | Crêtes dunaires sommitales, relief très sécurisé |
| **2** | **Faible** | **5.09 %** | Versants dunaires bien drainés |
| **3** | **Moyen** | **65.98 %** | Zone tampon intermédiaire (majorité de la commune) |
| **4** | **Élevé** | **20.82 %** | Abords immédiats des bas-fonds et tissu urbain dense |
| **5** | **Très élevé** | **7.81 %** | Cœur des cuvettes, lac Warouwaye et bas-fonds inondables |

![Répartition des Classes de Susceptibilité](assets/images/repartition_susceptibilite.png)
*Figure 8 : Proportion surfacique des classes de susceptibilité aux inondations.*

### 5.2 Interprétation et Discussion des Résultats
1. **Convergence topographique et géologique** : Les zones de susceptibilité **Très élevée (7.81 %)** et **Élevée (20.82 %)** coïncident de manière remarquable avec le couloir de **sols hydromorphes** et les altitudes inférieures à 3 mètres. Le secteur ceinturant le **lac Warouwaye** apparaît comme la zone la plus critique de la commune.
2. **Le poids de la classe intermédiaire** : La classe **Moyenne (65.98 %)** couvre les deux tiers de la commune. Ce résultat met en lumière la fragilité générale de Yeumbeul Nord : ces secteurs ne sont pas immédiatement inondés lors d'une pluie ordinaire, mais basculent rapidement en situation de submersion lors d'événements pluvieux intenses en raison de la saturation progressive du sol et de la remontée de la nappe phréatique.

---

## 6. Perspectives de Recherche : Vers une Automatisation par Machine Learning

Bien que l'Analyse Multicritère AHP apporte une compréhension qualitative solide des processus physiques, elle demeure tributaire de la subjectivité de l'opérateur et produit des cartes statiques. La perspective majeure de ce travail consiste à coupler cette analyse à des algorithmes de **Machine Learning supervisé** (Random Forest, XGBoost) afin d'automatiser et d'objectiver la détection des zones inondables.

```
                      [ DONNÉES GÉO-SPATIALES ]
             (MNT, Pente, TWI, Drainage, Sol, Occupation)
                                  │
                                  ▼
                     [ 1. MODÉLISATION AHP ]
                   (Pondération Saaty validée CR=1.5%)
                                  │
                                  ▼
                [ 2. ÉCHANTILLONNAGE STRATIFIÉ ]
          ┌───────────────────────┴───────────────────────┐
          ▼                                               ▼
  [ Classe 1 : Inondable ]                     [ Classe 0 : Non Inondable ]
  (Prélevée dans Très Élevé / Élevé)           (Prélevée dans Très Faible / Faible)
          └───────────────────────┬───────────────────────┘
                     (Exclusion de la classe « Moyen »)
                                  │
                                  ▼
                [ 3. APPRENTISSAGE MACHINE LEARNING ]
                   (Random Forest / XGBoost / SVM)
                                  │
                                  ▼
             [ 4. PRÉDICTION AUTOMATISÉE DYNAMIQUE ]
```

### 6.1 Protocole d'Échantillonnage et Binarisation
Pour entraîner un modèle de Machine Learning robuste, la binarisation des labels doit être rigoureusement guidée par les résultats AHP :
- **Classe 1 (Inondable / Présence)** : Points d'entraînement extraits exclusivement des classes **Très élevé (DN 5)** et **Élevé (DN 4)**.
- **Classe 0 (Non Inondable / Absence)** : Points d'entraînement extraits des classes **Très faible (DN 1)** et **Faible (DN 2)**.
- **Exclusion de la classe « Moyen » (DN 3)** : Afin d'éviter le bruit d'étiquetage (*label noise*), la zone tampon intermédiaire est écartée des données d'apprentissage du modèle.

### 6.2 Données d'Entraînement Générées
Un premier jeu de données géoréférencé de **465 échantillons équilibrés** (234 points inondables / 231 points non inondables) a d'ores et déjà été extrait via un script Python automatisé ([`sample_generator.py`](file:///c:/formation_qgis_2026/exo_amc/sample_generator.py)), associant à chaque point ses covariables environnementales :

| id | Coord X (m) | Coord Y (m) | **Label (Cible)** | Altitude | Pente (%) | TWI | Densité Drainage |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | 246546.5 | 1634616.0 | **1** (Inondable) | 3.0 | 5.0 | 4.0 | 5.0 |
| 2 | 246151.8 | 1636758.0 | **1** (Inondable) | 5.0 | 5.0 | 3.0 | 5.0 |
| ... | ... | ... | ... | ... | ... | ... | ... |
| 240 | 247120.0 | 1635890.0 | **0** (Non inondable) | 10.3 | 5.2 | 3.8 | 0.6 |

---

## 7. Recommandations pour l'Aménagement et la Mairie

À la lumière des résultats cartographiques, plusieurs recommandations opérationnelles peuvent être formulées à l'attention des services techniques de la **Mairie de Yeumbeul Nord** et des organismes d'assainissement (ONAS, PROGEP) :
1. **Protection stricte des zones tampons des Niayes** : Stopper immédiatement l'urbanisation clandestine dans les dépressions situées à une altitude inférieure à 3 m et autour du lac Warouwaye.
2. **Dimensionnement des infrastructures de drainage** : Concentrer la réalisation des caniveaux primaires et des bassins d'écrêtement le long des couloirs de drainage naturel identifiés par la classe de susceptibilité très élevée.
3. **Planification opérationnelle à l'échelle des quartiers** : Utiliser le découpage des 82 quartiers pour prioriser le déploiement des motopompes et organiser les opérations de secours lors de la survenue d'événements pluvieux intenses.

---

## 8. Références Bibliographiques

- **Diongue, M.** (2014). *Périphérie urbaine et risques d'inondation à Dakar (Sénégal) : Le cas de Yeumbeul Nord*. ESO Travaux et Documents, (37), 23-34.
- **Li, et al.** (2026). *Coupled Multi-Criteria Decision-Making and Machine Learning Approaches for Spatial Flood Susceptibility Prediction*. ScienceDirect / Geoscience Frontiers. [DOI: 10.1016/j.gsf.2026.1001854](https://www.sciencedirect.com/science/article/pii/S1674987126001854)
- **Saaty, T. L.** (1980). *The Analytic Hierarchy Process: Planning, Priority Setting, Resource Allocation*. McGraw-Hill International, New York.
- **Sy, B.** (2019). *Approche multidisciplinaire de l'évaluation de l'aléa d'inondation à Yeumbeul Nord, Dakar, Sénégal : la contribution de la science citoyenne*. Thèse de doctorat en sciences de l'environnement, Université de Genève, n° 5340. [Archive ouverte UNIGE](https://archive-ouverte.unige.ch/unige:126388)
