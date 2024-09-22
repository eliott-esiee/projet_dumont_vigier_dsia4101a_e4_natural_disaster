import pandas as pd  # Importer la bibliothèque pandas pour la manipulation de données.
import seaborn as sns  # Importer seaborn pour la visualisation de données.
import random  # Importer la bibliothèque random pour la génération de nombres aléatoires.

# Charger des données sur les catastrophes naturelles à partir de fichiers CSV.
natural_disaster_df = pd.read_csv('natural_disaster.csv')
df_geoloc = pd.read_csv("new_dataframe.csv")
global_temp_data = pd.read_csv('Global Temperature.csv')

# Associer les colonnes de latitude et de longitude de df_geoloc à natural_disaster_df.
natural_disaster_df['Latitude'],natural_disaster_df['Longitude'] = df_geoloc['Latitude'],df_geoloc['Longitude']

# Supprimer les lignes sans données de latitude et de longitude.
df_catastrophe_location = natural_disaster_df.dropna(subset=['Latitude', 'Longitude'])

# Extraire les années uniques des données de catastrophes pour une utilisation ultérieure.
annees = df_catastrophe_location['Year'].unique()

# Créer un dictionnaire pour mapper les types de catastrophes à des couleurs et des icônes spécifiques.
marqueur_type_de_catastrophe = {
    'Drought': {'color': 'beige', 'icon': 'tint'},
    'Drouuake': {'color': 'beige', 'icon': 'tint'},
    'Volcanic activity': {'color': 'orange', 'icon': 'fire'},
    'Mass movement (dry)': {'color': 'gray', 'icon': 'warning-sign'},
    'Storm': {'color': 'darkblue', 'icon': 'cloud'},
    'Earthquake': {'color': 'purple', 'icon': 'exclamation-sign'},
    'Earthquakeght': {'color': 'darkpurple', 'icon': 'exclamation-sign'},
    'Earthq':{'color': 'darkpurple', 'icon': 'exclamation-sign'},
    'Flood': {'color': 'blue', 'icon': 'tint'},
    'Epidemic': {'color': 'pink', 'icon': 'plus-sign'},
    'Landslide': {'color': 'darkgreen', 'icon': 'arrow-down'},
    'Wildfire': {'color': 'red', 'icon': 'fire'},
    'Extreme temperature ': {'color': 'darkred', 'icon': 'warning-sign'},
    'Fog': {'color': 'lightgray', 'icon': 'cloud'},
    'Insect infestation': {'color': 'green', 'icon': 'leaf'},
    'Impact': {'color': 'gray', 'icon': 'asterisk'},
    'Animal accident': {'color': 'green', 'icon': 'leaf'},
    'Glacial lake outburst': {'color': 'lightblue', 'icon': 'tint'}
}

# Nettoyer les données et grouper par année et code de pays (ISO) pour compter les catastrophes.
df_castrophe_country = natural_disaster_df.dropna(subset=['ISO','Year'])
disaster_counts = df_castrophe_country.groupby(['Year', 'ISO']).size().reset_index(name='Disaster Count')

# Grouper les données pour obtenir le nombre total de décès par année et par pays.
disaster_death_counts = df_castrophe_country.groupby(['Year', 'ISO'])['Total Deaths'].sum().reset_index(name='Death Count')

# Chemin vers le fichier GeoJSON qui contient les frontières des pays.
country_geojson = 'countries.geojson'  

# Sélectionner uniquement certaines colonnes pour l'analyse.
selected_columns = ['Disaster Group', 'Disaster Subgroup', 'Disaster Type', 'Disaster Subtype', 'Disaster Subsubtype']
df_selected = natural_disaster_df[selected_columns]

# Créer la liste des labels uniques à partir des colonnes sélectionnées.
labels = pd.concat([df_selected[col] for col in selected_columns]).unique().tolist()

# Créer un mapping pour les labels (chaque label est associé à un index unique).
label_mapping = {label: idx for idx, label in enumerate(labels)}

# Initialiser les listes pour stocker les informations des liens entre les labels.
source = []
target = []
value = []

def fill_lists(df, col1, col2):
    # Fonction pour remplir les listes source, target et value à partir des données groupées.
    grouped_df = df.groupby([col1, col2]).size().reset_index(name='count')
    for index, row in grouped_df.iterrows():
        source_idx = label_mapping[row[col1]]
        target_idx = label_mapping[row[col2]]
        source.append(source_idx)
        target.append(target_idx)
        value.append(row['count'])

# Remplir les listes pour chaque paire de colonnes adjacentes.
for i in range(len(selected_columns) - 1):
    fill_lists(df_selected, selected_columns[i], selected_columns[i + 1])

# Générer une palette de couleurs avec autant de couleurs qu'il y a de labels.
palette = sns.color_palette("husl", len(labels)).as_hex()

# Assigner une couleur à chaque nœud.
node_colors = [palette[i] for i in range(len(labels))]

# Générer des couleurs aléatoires pour les liens entre les nœuds.
link_colors = [f'rgba({random.randint(0,255)}, {random.randint(0,255)}, {random.randint(0,255)}, 0.5)' for _ in range(len(source))]

# Créer des textes Markdown pour décrire les différentes parties du tableau de bord.
texte_markdown = """

**Cartes des catastrophes :** Cette section présente une carte interactive qui illustre la répartition géographique des catastrophes. En sélectionnant différentes plages d'années, vous pouvez observer comment certaines régions du monde sont plus affectées que d'autres et comment cela a évolué au fil du temps.

**Histogrammes des morts :** Ici, nous analysons la fréquence et la sévérité des catastrophes naturelles au fil des ans. Les histogrammes permettent de visualiser les tendances et les modèles dans les données historiques, soulignant les périodes de haute activité et les types de catastrophes les plus communs.

**Evolution des catastrophes :** Ici, nous explorons les tendances dans l'occurrence des catastrophes naturelles au fil du temps. Cette analyse aide à comprendre si les catastrophes naturelles deviennent plus fréquentes et plus sévères avec le changement climatique et d'autres facteurs environnementaux.

**Evolution des morts :** Cette partie du dashboard se concentre sur l'impact humain des catastrophes naturelles. À travers des visualisations dynamiques, nous examinons l'évolution du nombre de décès dus aux catastrophes, offrant une perspective sombre mais nécessaire sur leur coût humain.

**Catastrophes les plus meurtrières :** Cet onglet met en lumière les catastrophes les plus dévastatrices en termes de pertes humaines. En examinant les catastrophes les plus meurtrières, nous pouvons apprendre de ces événements tragiques pour mieux nous préparer à l'avenir.

**Catastrophes les plus coûteuses :** Finalement, cette section aborde l'aspect financier des catastrophes naturelles. En analysant les coûts économiques, nous pouvons mieux comprendre l'impact financier global des catastrophes et les besoins en matière de ressources pour la reconstruction et la prévention.
"""
texte_markdown_2 = """

**Interactivité et Exploration :**

"""

texte_markdown_3 = """

Un élément clé de ce tableau de bord est son interactivité. Nous vous encourageons vivement à explorer les différents graphiques et visualisations interactives disponibles. Cliquez, faites glisser, et zoomez pour découvrir de nouveaux aperçus et perspectives sur les données. Votre interaction peut révéler des tendances cachées, des insights uniques et des informations détaillées qui ne sont pas immédiatement évidentes. N'hésitez pas à expérimenter et à explorer pour obtenir une compréhension plus profonde des catastrophes naturelles et de leur impact.

"""