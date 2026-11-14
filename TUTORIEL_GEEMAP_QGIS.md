# Tutoriel Pratique : Installer Geemap et Google Earth Engine dans QGIS sous Windows (100% Fonctionnel)

> **Auteur** : M. Ndiaye  
> **Contexte** : Intégration de Google Earth Engine (GEE), Python et Geemap dans QGIS sous environnement Windows.

---

## 1. Introduction et Objectif

L'intégration de **Google Earth Engine (GEE)** dans **QGIS** via l'extension **Geemap** (développée par le Pr. Qiusheng Wu / OpenGeos) permet d'accéder au catalogue mondial d'images satellites (Sentinel, Landsat, MODIS, MNT planétaires) et d'exécuter des scripts de télédétection directement au sein de l'interface graphique de QGIS.

Cependant, sous **Windows**, l'installation rencontre fréquemment des blocages techniques :
- Les méthodes basées sur Conda / Pixi pour lancer un second QGIS virtuel échouent souvent à cause de conflits de bibliothèques système (`Could not load qgis_app.dll`).
- Le bouton automatique « *Install Dependencies* » de l'extension QGIS peut se fermer prématurément avant la fin du téléchargement des 110 bibliothèques Python requises.

Ce tutoriel fournit le **protocole pas-à-pas infaillible** pour installer et faire fonctionner Geemap dans votre **QGIS habituel**.

---

## 2. Étape 1 : Installer l'extension Geemap dans QGIS

1. Ouvrez votre **QGIS classique** (ex: version 3.34, 3.44 LTR).
2. Dans le menu supérieur, ouvrez : **Extensions** ➔ **Installer/Gérer les extensions**.
3. Dans l'onglet **Paramètres** à gauche :
   - Cochez la case **« Afficher également les extensions expérimentales »**.
   - Dans la section *Dépôts d'extensions officieux*, cliquez sur le bouton **Ajouter...** :
     - **Nom** : `OpenGeos`
     - **URL** : `https://qgis.gishub.org/plugins.xml`
   - Cliquez sur **OK**.
4. Allez ensuite dans l'onglet **Toutes**, tapez **`Geemap`** dans la barre de recherche.
5. Sélectionnez le plugin et cliquez sur le bouton en bas à droite : **Installer l'extension**.

> Une nouvelle barre d'outils Geemap apparaît dans QGIS, avec notamment l'icône de la Terre flanquée d'un « G » et une icône d'**engrenage (Geemap Settings)**.

---

## 3. Étape 2 : Initialiser le dossier de l'environnement virtuel

1. Cliquez sur l'icône de l'engrenage **Geemap Settings** dans QGIS.
2. Dans l'onglet **Dependencies**, cliquez une première fois sur le bouton :
   👉 **`Install Dependencies`**
3. **Ce que fait QGIS en arrière-plan** :
   - Il crée un répertoire dédié dans votre dossier utilisateur : `C:\Users\<VotreNom>\.qgis_geemap`.
   - Il y installe un exécutable de gestion de paquets ultra-rapide (`uv.exe`) et prépare un environnement virtuel Python (`venv`).

---

## 4. Étape 3 : L'astuce technique (Forcer l'installation des 110 dépendances)

Sous Windows, le bouton graphique de QGIS peut afficher *« Installed successfully »* alors que le téléchargement réseau a été interrompu en tâche de fond, laissant les statuts en rouge (*Not installed*).

Pour garantir que les 110 paquets (`geemap`, `earthengine-api`, `google-auth-oauthlib`, etc.) soient réellement installés :

1. Ouvrez une fenêtre **PowerShell** sur votre ordinateur (Touche Windows ➔ tapez `PowerShell` ➔ Entrée).
2. Copiez-collez cette **commande unique** (universelle pour tout utilisateur Windows) :
   ```powershell
   & "$HOME\.qgis_geemap\uv\uv.exe" pip install --python "$HOME\.qgis_geemap\venv\Scripts\python.exe" earthengine-api geemap google-auth-oauthlib
   ```
3. Laissez tourner pendant 10 à 15 secondes.
4. Le terminal doit afficher :
   ```text
   Resolved 110 packages ...
   Installed 110 packages ...
    + earthengine-api==...
    + geemap==...
    + google-auth-oauthlib==...
   ```

---

## 5. Étape 4 : Validation et Enregistrement dans QGIS

1. Retournez dans QGIS, dans la fenêtre **Geemap Settings**.
2. Cliquez sur le bouton **`Refresh Status`** :
   - Les 3 lignes rouges passent instantanément au **VERT** avec la mention **`Installed`**.
3. Cliquez sur le bouton tout en bas à gauche : **`Save Settings`** *(cette étape est essentielle pour que QGIS retienne les chemins)*.
4. **Fermez complètement QGIS et rouvrez-le**.

---

## 6. Étape 5 : Authentification Google Earth Engine

Pour que Google vous autorise à charger des images satellites, vous devez lier votre compte :

1. Assurez-vous d'avoir créé un projet Google Cloud Earth Engine (gratuit pour la recherche/éducation sur [earthengine.google.com](https://earthengine.google.com)). Notez le nom de votre projet (ex: `ee-monnom` ou `nom-du-projet-123456`).
2. Dans votre terminal **PowerShell**, lancez l'authentification :
   ```powershell
   & "$HOME\.qgis_geemap\venv\Scripts\python.exe" -c "import ee; ee.Authenticate()"
   ```
3. Une page web Google s'ouvre :
   - Connectez-vous avec votre adresse Gmail.
   - Validez les autorisations et autorisez la génération du jeton.
   - Les identifiants sont sauvegardés automatiquement sur votre machine (`~/.config/earthengine/credentials`).
4. Dans QGIS, ouvrez **Geemap Settings** ➔ onglet **Earth Engine** :
   - Saisissez votre **Project ID** Google Cloud dans le champ prévu.
   - Cliquez sur **Save Settings**.

---

## 7. Étape 6 : Test et Démonstration en Direct

1. Dans QGIS, cliquez sur l'icône **Geemap** (icône Terre avec le « G »).
2. Le panneau **Geemap for QGIS** s'ouvre.
3. Allez dans l'onglet **Code**, tapez :
   ```python
   import ee
   import geemap

   # Tester la connexion
   print("Connexion réussie !")
   ```
4. Cliquez sur **Run Code**.
5. **Résultat attendu** : Aucun message d'erreur rouge ! Le système est pleinement fonctionnel.

### Exemple de script pour charger un MNT mondial (SRTM) dans QGIS :
```python
import ee

dem = ee.Image('USGS/SRTMGL1_003')
vis_params = {
    'min': 0,
    'max': 4000,
    'palette': ['006633', 'E5FFCC', '662A00', 'D8D8D8', 'F5F5F5']
}
m.add_layer(dem, vis_params, 'SRTM DEM')
```

---

## 8. Résumé des Erreurs Courantes et Diagnostics

| Message d'erreur | Cause | Solution |
| :--- | :--- | :--- |
| `Could not load qgis_app.dll` | Conflit entre deux versions de QGIS (ex: tentative de lancer un QGIS Pixi alors qu'un QGIS natif est déjà installé). | Ne pas utiliser QGIS via Pixi ; installer le plugin directement dans le QGIS existant. |
| `Error: No module named 'geemap'` ou `'ee'` | Les dépendances Python ne sont pas installées dans `.qgis_geemap\venv\Lib\site-packages` ou les réglages n'ont pas été sauvegardés. | Exécuter la commande `uv pip install` (Étape 3), faire *Refresh Status* puis *Save Settings*. |
| `Earth Engine API not found` | Absence du jeton d'authentification ou du Project ID. | Lancer `ee.Authenticate()` en PowerShell et renseigner le *Project ID* dans l'onglet Earth Engine. |

