# Guide Utilisateur

## Prérequis

Avant de commencer, assurez-vous d'avoir :

- **Python** : Installez la version la plus récente de Python depuis [le site officiel Python](https://www.python.org/downloads/).
- **IDE Python** (Optionnel) : Un environnement de développement comme PyCharm ou Visual Studio Code.

## Cloner le Dépôt GitHub

1. **Cloner le dépôt** : Ouvrez votre terminal et exécutez la commande suivante :

   ```bash
   git clone https://github.com/eliott-esiee/projet_dumont_vigier_dsia4101a_e4_natural_disaster
   ```

2. **Naviguer dans le dossier du projet** :

   ```
   cd projet_dumont_vigier_dsia4101a_e4_natural_disaster-master
   ```


## Installation des Dépendances

1. **Installer les packages Python nécessaires** :

   pip install -r requirements.txt

## Téléchargement et Configuration des Données

Assurez-vous que les fichiers de données comme `countries.geojson`, `Global Temperature.csv`, `natural_disaster.csv`, `new_dataframe.csv` sont placés dans le bon dossier.

## Lancement de l'Application

1. **Exécuter l'application** :

   python main.py

# Rapport d’Analyse

## Jeux de données

### Premier jeu de données (Fichier `Natural_disaster.csv`)

Le fichier `Natural_disaster.csv` est un ensemble de données complet qui documente diverses catastrophes naturelles survenues à travers le monde. Ces données, provenant de l'EOSDIS (Earth Observing System Data and Information System), fournissent des informations détaillées sur les événements, leur type, leur localisation, ainsi que leur impact humain et économique. Voici une vue d'ensemble des colonnes clés et de ce qu'elles représentent :

1. **Year, Seq, Glide** : Identifiants et références uniques pour chaque événement.
2. **Disaster Group & Subgroup** : Catégorisation générale des catastrophes (par exemple, naturelles, géophysiques).
3. **Disaster Type & Subtype** : Type spécifique de catastrophe (par exemple, inondation, séisme).
4. **Event Name, Country, ISO** : Nom de l'événement, pays et code ISO où il s'est produit.
5. **Region, Continent, Location** : Informations géographiques plus détaillées.
6. **Origin, Associated Dis(1&2), OFDA Response** : Origine de la catastrophe, catastrophes associées et réponses d'urgence.
7. **Appeal, Declaration** : Appels à l'aide et déclarations officielles.
8. **Aid Contribution, Dis Mag(Value & Scale)** : Contributions d'aide et magnitude de la catastrophe.
9. **Latitude, Longitude** : Coordonnées géographiques de l'événement.
10. **Start/End Year, Month, Day** : Dates de début et de fin de l'événement.
11. **Total Deaths, No Injured, No Affected, No Homeless, Total Affected** : Impact humain (décès, blessés, affectés, sans-abris).
12. **Insured Damages, Total Damages, CPI** : Dégâts matériels assurés et totaux, indice des prix à la consommation pour contextualiser économiquement.
13. **Adm Level, Admin1/2 Code, Geo Locations** : Niveaux administratifs concernés et localisations géographiques plus précises.

### Deuxième jeu de données (Fichier `Global Temperature.csv`)

Le fichier `Global Temperature.csv` contient des données détaillées sur les températures mondiales, fournies par Berkeley Earth (https://berkeleyearth.org/data/). Ces données sont essentielles pour analyser les tendances climatiques et comprendre les variations de température sur une longue période. Voici un aperçu des principales colonnes et de leur signification :

1. **Year, Month** : L'année et le mois de l'enregistrement des données.
2. **Monthly Anomaly** : L'écart mensuel de la température par rapport à une moyenne de référence.
3. **Monthly Unc.** : L'incertitude associée à l'anomalie mensuelle.
4. **Annual Anomaly** : L'anomalie annuelle de la température.
5. **Annual Unc** : L'incertitude associée à l'anomalie annuelle.
6. **Five-Year Anomaly, Ten-Year Anomaly, Twenty-Year Anomaly** : Anomalies calculées sur des périodes de cinq, dix et vingt ans pour observer les tendances à long terme.
7. **Uncertainties** : Les incertitudes correspondantes pour les anomalies calculées sur différentes périodes.

### Troisième jeu de données (Fichier `new_dataframe.csv`)

Le fichier `new_dataframe.csv` a été généré en utilisant un processus de géocodage via l'API Google, à partir des données de catastrophes naturelles. Ce fichier contient des informations géolocalisées enrichies pour chaque événement de catastrophe. Voici une brève description du processus utilisé pour créer ce fichier :

#### Processus de Géocodage

Voici le code :
```
import pandas as pd
import concurrent.futures
from geopy.geocoders import GoogleV3
from geopy.extra.rate_limiter import RateLimiter

# Charger le fichier CSV
df = pd.read_csv("1900_2021_DISASTERS.xlsx - emdat data.csv")

# Imprimer le nombre de valeurs manquantes dans la colonne 'Latitude'
print(df['Latitude'].isna().sum())

# Initialiser le géolocalisateur
geolocator = GoogleV3(api_key="Votre_API_Key_Ici")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1/50)

# Créer un dictionnaire de cache
cache = {}

def get_coordinates(address):
    # Si l'adresse est dans le cache, retourner le résultat en cache
    if address in cache:
        return cache[address]

    # Sinon, obtenir les coordonnées de l'API
    location = geocode(address)
    if location is not None:
        coordinates = (location.latitude, location.longitude)
    else:
        coordinates = (None, None)

    # Stocker le résultat dans le cache
    cache[address] = coordinates

    return coordinates

# Appliquer la fonction à chaque ligne du dataframe en parallèle
with concurrent.futures.ThreadPoolExecutor() as executor:
    df['Latitude'], df['Longitude'] = zip(*executor.map(get_coordinates, df['Location']))

# Imprimer le nombre de valeurs manquantes dans la colonne 'Latitude' après géocodage
print(df['Latitude'].isna().sum())

# Conserver uniquement les colonnes 'Location', 'Latitude' et 'Longitude'
df = df[['Location', 'Latitude', 'Longitude']]

# Sauvegarder le nouveau dataframe dans un fichier CSV
df.to_csv("new_dataframe.csv", index=False)
```

1. **Chargement des Données Initiales** : Les données de catastrophes naturelles ont été chargées à partir d'un fichier CSV source.
2. **Géocodage avec l'API Google** : Utilisant l'API GoogleV3 via la bibliothèque `geopy`, chaque emplacement a été géocodé pour obtenir des coordonnées précises.
3. **Utilisation de Rate Limiter** : Pour éviter de dépasser les limites de requêtes de l'API, un `RateLimiter` a été employé.
4. **Caching des Résultats** : Les résultats de géocodage ont été mis en cache pour optimiser les performances et réduire les requêtes inutiles.
5. **Parallélisation du Processus** : Le processus de géocodage a été exécuté en parallèle pour accélérer le traitement.
6. **Nettoyage des Données** : Les colonnes finales sélectionnées étaient 'Location', 'Latitude' et 'Longitude'.
7. **Sauvegarde du Nouveau Fichier CSV** : Les données enrichies ont été sauvegardées dans `new_dataframe.csv`.

## Principales Conclusions

### Partie Histogramme

- **Fréquence des Décès** : La grande majorité des catastrophes provoquent peu de décès. Cette observation suggère que, bien que fréquentes, toutes les catastrophes naturelles ne sont pas nécessairement mortelles à grande échelle.

### Partie Carte des Catastrophes

- **Localisation des Catastrophes** : Les inondations se produisent principalement autour des fleuves, et de nombreuses tornades (orages supercellulaires) sont observées dans la Tornado Valley aux États-Unis. Cette répartition géographique montre clairement les zones les plus susceptibles d'être affectées par certaines catastrophes.

### Partie Évolution des Catastrophes

- **Augmentation du Nombre de Catastrophes** : Depuis 1900, le nombre de catastrophes naturelles semble augmenter parallèlement à l'augmentation de la température globale. 
- **Croissance de Certaines Catastrophes** : Une augmentation notable est observée pour les inondations et les tempêtes, suggérant un changement dans les modèles météorologiques et climatiques.

### Partie Catastrophes les Plus Coûteuses

- **Augmentation des Dégâts Matériels** : Les dommages causés par les catastrophes augmentent également au fil des années. 
- **Coûts Élevés de Certaines Catastrophes** : Les cyclones, les séismes et les inondations sont particulièrement coûteux en termes de dégâts, reflétant leur impact dévastateur sur les infrastructures.

### Partie Catastrophes les Plus Meurtrières

- **Catastrophes avec le Plus Grand Nombre de Décès** : Les sécheresses et les épidémies sont identifiées comme les catastrophes les plus meurtrières. Ces types d'événements ont un impact direct et significatif sur la santé humaine et la sécurité alimentaire.

### Partie Évolution des Morts

- **Impact Variable selon les Pays** : Certains pays, tels que l'Allemagne et la Finlande, semblent être moins touchés par les catastrophes en termes de mortalité. Cette observation peut refléter des capacités de gestion des catastrophes plus efficaces ou des conditions géographiques et climatiques moins propices aux événements catastrophiques majeurs.
En revanche certain petit pays comme Haiti on pourtant un nombre de mort très élevé lié au catastrophe.

# Guide Développeur

## Prérequis

- **Python** : Installez la version la plus récente de Python depuis [le site officiel Python](https://www.python.org/downloads/).
- **Bibliothèques Python** : Assurez-vous que les bibliothèques nécessaires (celles présentes dans requirement.txt) comme Dash, Pandas, Plotly, et Dash Bootstrap Components sont installées.

## Installation des Dépendances

- Exécutez `pip install -r requirements.txt` dans votre terminal pour installer toutes les dépendances requises.

## Configuration des Données

- Les données sont chargées à partir de fichiers CSV et GeoJSON. Assurez-vous que les fichiers `countries.geojson`, `Global Temperature.csv`, `natural_disaster.csv`, `new_dataframe.csv` sont présents dans le dossier approprié.

## Architecture du Code

L'application est structurée comme suit :

- **main.py** : C'est le point d'entrée de l'application. Il initialise l'application Dash et définit les styles externes.
- **layout.py** : Contient la définition de la mise en page de l'application. Modifiez ce fichier pour changer l'agencement des composants de l'interface utilisateur.
- **callbacks.py** : Gère la logique des interactions utilisateur. Les fonctions callback de Dash y sont définies pour rendre l'application dynamique.
- **config.py** : Contient les configurations comme les chemins des fichiers de données et les paramètres globaux. Modifiez-le pour changer les configurations de base.
- **style.css** : Fichier de style pour personnaliser l'apparence de l'application. Ajoutez ou modifiez les styles CSS ici.

## Modification et Extension du Code

1. **Ajouter de Nouvelles Fonctionnalités** :
   - Pour ajouter de nouvelles fonctionnalités, commencez par définir de nouveaux composants dans `layout.py`.
   - Ensuite, créez les callbacks nécessaires dans `callbacks.py` pour gérer les interactions avec ces composants.

2. **Modification des Données** :
   - Les données sont chargées et gérées dans `config.py`. Pour utiliser de nouvelles sources de données, modifiez les chemins de fichiers ou les fonctions de chargement de données ici.

3. **Personnalisation de l'Interface** :
   - Modifiez `layout.py` pour changer l'agencement des composants.
   - Utilisez `style.css` pour modifier l'apparence des composants de l'interface utilisateur.

4. **Debugging et Tests** :
   - Utilisez des outils de debugging Python standard pour tester et déboguer l'application.
   - Dash offre également des fonctionnalités de logging pour suivre les interactions et les callbacks.

## Bonnes Pratiques

- **Versionnage du Code** : Utilisez Git pour le contrôle de version et GitHub pour le partage et la collaboration.
- **Documentation** : Documentez tout changement important dans le code pour faciliter la compréhension et la maintenance.
- **Tests** : Écrivez des tests unitaires pour les nouvelles fonctionnalités pour garantir la stabilité de l'application.
## Lancement de l'Application

1. Ouvrez un terminal et naviguez vers le dossier de l'application.
2. Exécutez `python main.py` pour démarrer l'application.
3. Ouvrez un navigateur web et accédez à l'URL indiquée dans le terminal (généralement `http://127.0.0.1:8050/`).

## Utilisation de l'Application

- **Navigation** : Utilisez la barre latérale pour naviguer entre les différentes pages de l'application.
- **Interactivité** : Interagissez avec les graphiques et les cartes pour des visualisations dynamiques.
- **Filtres et Sélections** : Utilisez les filtres disponibles pour affiner les visualisations selon vos critères.
