import folium  # Importation du module folium
import plotly_express as px  # Importation du module plotly_express
import dash  # Importation du module dash
import numpy as np  # Importation du module numpy
from plotly.subplots import make_subplots  # Importation du module plotly.subplots
import plotly.graph_objects as go  # Importation du module plotly.graph_objects
from dash import dcc, html  # Importation du module dash
from dash.dependencies import Input, Output  # Importation du module dash.dependencies

import geopandas as gpd  # Importation du module geopandas

from config import *  # Importation de tout depuis le module config

from main import app  # Importation de l'application depuis le module main

# Déclaration d'un callback pour mettre à jour le contenu en fonction des clics sur les liens
@app.callback(
    Output('content', 'children'),  # Spécifie l'élément à mettre à jour et sa propriété
    [Input("home-link", "n_clicks"),  # Inputs basés sur le nombre de clics sur les liens
     Input("map-link", "n_clicks"),
     Input("histogram-link", "n_clicks"),
     Input("graph3-link", "n_clicks"),
     Input("graph4-link", "n_clicks"),
     Input("graph5-link", "n_clicks"),
     Input("graph6-link", "n_clicks")]
)
# Fonction pour mettre à jour le contenu en fonction de l'élément cliqué
def update_content(home_link_clicks, map_link_clicks, histogram_link_clicks, graph3_link_clicks, graph4_link_clicks, graph5_link_clicks, graph6_link_clicks):
    ctx = dash.callback_context  # Obtenir le contexte du callback
    if not ctx.triggered:  # Si aucun élément n'a été cliqué
        return generate_home_content()  # Retourner le contenu de la page d'accueil
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]  # Identifier le bouton cliqué
        # Retourner le contenu approprié en fonction du bouton cliqué
        if button_id == "home-link":
            return generate_home_content()
        elif button_id == "map-link":
            return generate_map_content()
        elif button_id == "histogram-link":
            return generate_histogram_content()
        elif button_id == "graph3-link":
            return generate_graph3_content()
        elif button_id == "graph4-link":
            return generate_graph4_content()
        elif button_id == "graph5-link":
            return generate_graph5_content()
        elif button_id == "graph6-link":
            return generate_graph6_content()

# Fonction pour générer le contenu de la page d'accueil
def generate_home_content():
    return html.Div([
        # Ajout d'un titre H2
        html.H2("Bienvenue sur notre Dashboard d'étude des catastrophes naturelles",style={'textAlign': 'center'},
            className= 'subtitle_color'),
        # Utilisation de Markdown pour le texte
        dcc.Markdown(texte_markdown, style={'textAlign': 'justify'},
                 className='subtitle_color marge_top'),
        dcc.Markdown(texte_markdown_2, style={'textAlign': 'center'},
                 className='subtitle_color marge_top'),      
        dcc.Markdown(texte_markdown_3, style={'textAlign': 'justify'},
                 className='subtitle_color marge_top')
    ])

# Fonction pour générer le contenu de la carte des catastrophes
def generate_map_content():
    # Création d'un conteneur HTML pour la carte
    return html.Div(children=[
        # Ajout d'un titre H2
        html.H2(children=f'Carte des catastrophes naturelles',style={'textAlign': 'center',},
            className= 'subtitle_color'),
        # Ajout d'un RangeSlider pour sélectionner les années
        dcc.RangeSlider(id='annees',
                        className='RangeSlider',
                        marks={str(year): str(year) for year in annees if year %10 == 0},
                        min=min(annees),
                        max=max(annees),
                        value=[max(annees)-1, max(annees)],
                        step=1,
                        tooltip={"placement":"bottom","always_visible":True}),
        # Div pour afficher la carte mise à jour
        html.Div(id='map_annee')
    ])

# Callback pour mettre à jour la carte en fonction de la sélection de l'année
@app.callback(
    Output('map_annee', 'children'),  # Spécifie l'élément à mettre à jour et sa propriété
    [Input('annees', 'value')]  # Input basé sur la valeur sélectionnée dans le RangeSlider
)
def update_map(year_range):  # Fonction pour mettre à jour la carte, prenant en entrée une plage d'années.
    coord = (48.8398094, 2.5840685)  # Coordonnées géographiques pour centrer la carte sur l'Esiee.
    carte = folium.Map(location = coord, tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}', attr='ESRI', zoom_start=3)  # Création de la carte avec Folium, en utilisant un service de tuiles.

    debut , fin = year_range  # Séparer la plage d'années en année de début et de fin.
    
    feature_groups = {}  # Initialiser un dictionnaire pour les groupes de fonctionnalités (marqueurs de type de catastrophe).
    for disaster_type in marqueur_type_de_catastrophe.keys():  # Parcourir chaque type de catastrophe.
        feature_groups[disaster_type] = folium.FeatureGroup(name=disaster_type)  # Créer un groupe de fonctionnalités pour chaque type de catastrophe.

    df_catastrophe_location_selected = df_catastrophe_location[(df_catastrophe_location['Year'] >= debut) & (df_catastrophe_location['Year'] <= fin)]  # Filtrer les données de catastrophe selon la plage d'années sélectionnée.

    for location, latitude, longitude,type_de_catastrophe in zip(df_catastrophe_location_selected['Location'], 
                                                                 df_catastrophe_location_selected['Latitude'], 
                                                                 df_catastrophe_location_selected['Longitude'],
                                                                 df_catastrophe_location_selected['Disaster Type']):  # Itérer sur les données filtrées.
        
        coords = [latitude, longitude]  # Coordonnées de chaque catastrophe.

        if type_de_catastrophe in marqueur_type_de_catastrophe:  # Vérifier si le type de catastrophe est reconnu.

            icon_color = marqueur_type_de_catastrophe[type_de_catastrophe]['color']  # Couleur de l'icône.
            icon_type = marqueur_type_de_catastrophe[type_de_catastrophe]['icon']  # Type de l'icône.
            icon = folium.Icon(color=icon_color, icon=icon_type)  # Création de l'icône.
            marker = folium.Marker(location=coords, popup=location, icon=icon)  # Création du marqueur.
            marker.add_to(feature_groups[type_de_catastrophe])  # Ajouter le marqueur au groupe de fonctionnalités correspondant.

    # Ajouter chaque FeatureGroup à la carte.
    for fg in feature_groups.values():
        fg.add_to(carte)

    # Ajouter un contrôle pour afficher/masquer chaque FeatureGroup.
    folium.map.LayerControl().add_to(carte)

    legend_html = """
    <div style="position: fixed; 
    bottom: 50px; left: 50px; width: 250px; height: auto; 
    border:2px solid grey; z-index:9999; font-size:14px; background-color: white; padding: 10px;">
    &nbsp; <b>Legend</b> <br>
    """  # Début du code HTML pour la légende.

    for catastrophe, attributes in marqueur_type_de_catastrophe.items():  # Itérer sur les types de catastrophes pour créer la légende.
        color = attributes['color']  # Couleur pour la légende.
        icon = attributes['icon'].replace('-sign', '')  # Icône pour la légende.
        legend_html += f'&nbsp; <i class="fa fa-map-marker" style="color:{color}"></i>&nbsp; <i class="fa fa-{icon}"></i>&nbsp; {catastrophe} <br>'  # Ajouter chaque élément à la légende.

    legend_html += '</div>'  # Fin du code HTML pour la légende.
    carte.get_root().html.add_child(folium.Element(legend_html))  # Ajouter la légende à la carte.

    carte.save('map.html')  # Sauvegarder la carte en tant que fichier HTML.


    return html.Iframe(srcDoc=open('map.html', 'r', encoding='utf-8').read(), width='100%', height='600px')
        
def generate_histogram_content():
    # Cette fonction génère le contenu de l'histogramme.

    return html.Div(children=[
        # Titre de la section.
        html.H2(children='Histogramme des décès dus aux catastrophes naturelles',
                style={'textAlign': 'center'},
                className= 'subtitle_color'),
        
        # Slider pour sélectionner la plage d'années.
        dcc.RangeSlider(
            id='year-slider',
            className='RangeSlider',
            min=min(annees),
            max= max(annees),
            value=[min(annees),max(annees)],
            marks={str(year): str(year) for year in annees if year % 10 == 0},
            step=1,
            tooltip={"placement": "bottom", "always_visible": True}
        ),
        
        # Première visualisation d'histogramme.
        html.H3(children='Histogramme global du nombre total de décès dus aux catastrophes naturelles',
                style={'textAlign': 'center'},
                className= 'subtitle_color mb-4'),
        dcc.Graph(id='graph1'),

        # Deuxième visualisation d'histogramme.
        html.H3(children='Histogramme des décès (0 à 10,000) dus aux catastrophes naturelles',
                style={'textAlign': 'center'},
                className= 'subtitle_color marge_top mb-4'),
        dcc.Graph(id='graph2'),

        # Troisième visualisation d'histogramme.
        html.H3(children='Histogramme des décès (0 à 10,000) dus aux catastrophes naturelles',
                style={'textAlign': 'center'},
                className= 'subtitle_color marge_top mb-4'),
        dcc.Graph(id='graph3'),

        # Quatrième visualisation d'histogramme (densité).
        html.H3(children='Densité de la distribution des décès et des dommages',
                style={'textAlign': 'center'},
                className= 'subtitle_color marge_top mb-4'),
        dcc.Graph(id='graph4'),

        # Description sous les histogrammes.
        html.Div(children='''
            Les histogrammes représentent la distribution du nombre total de décès 
            dus aux catastrophes naturelles.
        ''', className= 'description_color text-center p-3 marge_top')
    ])


# Rappel pour mettre à jour les histogrammes en fonction de la sélection de l'année
@app.callback(
    [Output('graph1', 'figure'),
     Output('graph2', 'figure'),
     Output('graph3', 'figure'),
     Output('graph4', 'figure')],
    [Input('year-slider', 'value')]
)
def update_histogram(selected_years):
    # Filtrer le DataFrame en fonction de la plage d'années sélectionnée.
    filtered_df = natural_disaster_df[(natural_disaster_df['Year'] >= selected_years[0]) & 
                                      (natural_disaster_df['Year'] <= selected_years[1])]
    
    # Premier histogramme, représentant le nombre total de décès.
    fig1 = px.histogram(filtered_df, x="Total Deaths",
                        nbins=50,
                        log_y=True)
    
    # Deuxième histogramme, pour les décès entre 0 et 10,000.
    fig2 = px.histogram(filtered_df[(filtered_df["Total Deaths"] >= 0) & 
                                    (filtered_df["Total Deaths"] <= 10000)],
                        x="Total Deaths",
                        nbins=100,
                        log_y=True)
    
    # Troisième histogramme, avec coloration par sous-groupe de catastrophe.
    fig3 = px.histogram(filtered_df[(filtered_df["Total Deaths"] >= 0) & 
                                    (filtered_df["Total Deaths"] <= 10000)],
                        x="Total Deaths",
                        color="Disaster Subgroup",
                        nbins=100,
                        log_y=True,
                        hover_data=["Disaster Subgroup"])
    
    # Préparation des données pour le quatrième histogramme (heatmap).
    filtered_for_heatmap = filtered_df[(filtered_df["Total Deaths"] <= 500) & 
                                       (filtered_df["Total Damages ('000 US$)"] <= 1000000)]
    
    # Quatrième histogramme en tant que heatmap 2D.
    fig4 = px.density_heatmap(filtered_for_heatmap, 
                              x="Total Deaths", 
                              y="Total Damages ('000 US$)",
                              marginal_x="histogram", 
                              marginal_y="histogram",
                              nbinsx=6,
                              nbinsy=6)
    fig4.add_trace(px.scatter(filtered_for_heatmap, 
               x="Total Deaths", 
               y="Total Damages ('000 US$)",
               opacity=0.5).data[0])

    # Retourner les quatre figures pour mise à jour sur l'interface.
    return fig1, fig2, fig3, fig4


def generate_graph3_content():
    # Nettoyage et préparation des données de température.
    global_temp_data.columns = global_temp_data.columns.str.strip()  # Nettoyer les noms de colonnes.
    annual_anomaly_data = global_temp_data[['Year', 'Annual Anomaly']].dropna(subset=['Annual Anomaly'])  # Sélectionner et nettoyer les données d'anomalie annuelle.
    annual_anomaly_data = annual_anomaly_data[(annual_anomaly_data['Year'] >= 1900) & (annual_anomaly_data['Year'] <= 2021)]  # Filtrer les données par année.
    annual_anomaly_data['Smoothed Anomaly'] = annual_anomaly_data['Annual Anomaly'].rolling(window=50, center=True).mean()  # Lisser les anomalies sur une fenêtre de 50 ans.

    # Préparation des données de catastrophes naturelles.
    disaster_count_per_year = natural_disaster_df.groupby('Year').size()  # Compter les catastrophes par année.
    disaster_count_by_type = natural_disaster_df.groupby(['Year', 'Disaster Type']).size().unstack().fillna(0)  # Compter et organiser les catastrophes par type et par année.

    # Création du premier graphique avec deux axes y.
    fig1 = make_subplots(specs=[[{"secondary_y": True}]])  # Initialiser un graphique avec deux axes y.

    # Ajout des courbes au premier graphique.
    fig1.add_trace(
        go.Scatter(x=disaster_count_per_year.index, y=disaster_count_per_year, mode='lines', name='Nombre de catastrophes'),  # Tracer le nombre de catastrophes.
        secondary_y=False,
    )

    fig1.add_trace(
        go.Scatter(x=annual_anomaly_data['Year'], y=annual_anomaly_data['Smoothed Anomaly'], mode='lines', name='Écart de température'),  # Tracer l'écart de température.
        secondary_y=True,
    )

    # Mise à jour des axes du premier graphique.
    fig1.update_xaxes(title_text="Année")
    fig1.update_yaxes(title_text="Nombre de catastrophes", secondary_y=False)
    fig1.update_yaxes(title_text="Écart de température", secondary_y=True)

    # Création du deuxième graphique (Évolution par type de catastrophe).
    fig2 = go.Figure()

    # Ajouter des courbes pour chaque type de catastrophe.
    for disaster_type in disaster_count_by_type.columns:
        fig2.add_trace(go.Scatter(x=disaster_count_by_type.index, y=disaster_count_by_type[disaster_type], mode='lines', name=disaster_type))

    # Mise à jour de la mise en page du deuxième graphique.
    fig2.update_layout(xaxis_title="Année", yaxis_title="Nombre de catastrophes")

    # Retourner les deux graphiques enveloppés dans un Div HTML pour affichage dans l'application Dash.
    return html.Div(children=[
        html.H2(children=f'Nombre de catastrophes naturelles et écart de température (par rapport à l\'air pré-industrielle) par an',style={'textAlign': 'center'},
                className= 'subtitle_color mb-4'),
        dcc.Graph(figure=fig1),
        html.H2(children=f'Nombre de catastrophes naturelles par type par an',style={'textAlign': 'center'},
                className= 'subtitle_color marge_top mb-4'),
        dcc.Graph(figure=fig2)
    ])


def generate_graph4_content():
    # Cette fonction génère le contenu pour le quatrième graphique de l'application Dash.

    return html.Div(children=[
        # Titre de la section de la carte.
        html.H2(children=f'Carte des catastrophes et morts',style={'textAlign': 'center'},
                className= 'subtitle_color'),

        # Slider pour sélectionner la plage d'années.
        dcc.RangeSlider(id='range_annees',
                        className='RangeSlider',
                        marks={str(year): str(year) for year in annees if year %10 == 0},
                        min=min(annees),
                        max=max(annees),
                        value=[max(annees)-1, max(annees)],
                        step=1,
                        tooltip={"placement":"bottom","always_visible":True}),

        # Div pour afficher la carte.
        html.Div(id='map_2'),

        # Description sous la carte.
        html.H4(children = '''
                On peut décocher et cocher en haut a droite pour voir seulement le nombre de catastrophes par pays ou le nombre de morts par pays.
                ''', className='description_color text-center p-3 marge_top'),

        # Titre de la section du treemap.
        html.H2(children=f'Treemap des morts causés par les catastrophes naturelles',style={'textAlign': 'center'},
                className= 'subtitle_color mb-4'),

        # Graphique Treemap.
        dcc.Graph(id='treemap-natural-disaster')
    ])


@app.callback(
    Output('map_2', 'children'),
    [Input('range_annees', 'value')]
)
def update_map_2(year_range):
    # Cette fonction met à jour la carte en fonction de la plage d'années sélectionnée.

    coord = (48.8398094, 2.5840685) # Coordonnées pour centrer la carte.
    # Création de la carte avec Folium.
    carte = folium.Map(location = coord, tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}', attr='ESRI',zoom_start=3)

    debut , fin = year_range  # Plage d'années sélectionnée.

    # Filtrer les données de catastrophes.
    df_filtered = disaster_counts[(disaster_counts['Year'] >= debut) & (disaster_counts['Year'] <= fin)]

    # Calcul et affichage des catastrophes par pays sur la carte.
    country_disaster_counts = df_filtered.groupby('ISO')['Disaster Count'].sum().reset_index()
    folium.Choropleth(
        geo_data=country_geojson,
        name='Nombre de castrophes naturelles par pays',
        data=country_disaster_counts,
        columns=['ISO', 'Disaster Count'],
        key_on='feature.properties.ISO_A3',
        fill_color='OrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Nombre de catastrophes naturelles par pays'
    ).add_to(carte)

    # Calcul et affichage des décès par pays sur la carte.
    df_filtered_death = disaster_death_counts[(disaster_death_counts['Year'] >= debut) & (disaster_death_counts['Year'] <= fin)]
    country_death_counts = df_filtered_death.groupby('ISO')['Death Count'].sum().reset_index()
    folium.Choropleth(
        geo_data=country_geojson,
        name='Nombre de morts par pays',
        data=country_death_counts,
        columns=['ISO', 'Death Count'],
        key_on='feature.properties.ISO_A3',
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Nombre de morts par pays'
    ).add_to(carte)

    folium.LayerControl().add_to(carte)

    # Retourner la carte pour l'affichage dans Dash.
    carte_html = carte._repr_html_()
    return html.Iframe(srcDoc=carte_html, width='100%', height='600px')


# Callback pour mettre à jour le graphique en fonction de la plage d'années sélectionnée
@app.callback(
    Output('treemap-natural-disaster', 'figure'),
    [Input('range_annees', 'value')]
)
def update_treemap_graph_4(selected_years):
    # Cette fonction met à jour le treemap en fonction de la plage d'années sélectionnée.

    # Filtrer les données de catastrophes naturelles selon les années sélectionnées.
    filtered_data = natural_disaster_df[(natural_disaster_df['Year'] >= selected_years[0]) & 
                                        (natural_disaster_df['Year'] <= selected_years[1])]

    # Grouper les données par continent et pays.
    grouped_data = filtered_data.groupby(['Continent', 'Country']).agg(
        Total_Deaths=('Total Deaths', 'sum'),
        Total_Disasters=('Seq', 'count')
    ).reset_index()

    # Appliquer une transformation logarithmique sur le nombre total de décès.
    grouped_data['Log_Total_Deaths'] = np.log1p(grouped_data['Total_Deaths'])

    # Créer le treemap.
    fig = px.treemap(grouped_data, path=[px.Constant("world"), 'Continent', 'Country'], values='Total_Disasters',
                     color='Log_Total_Deaths', hover_data=['Total_Deaths'],
                     color_continuous_scale='RdBu_r')

    # Mise à jour de la mise en page du treemap.
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))

    # Définir les valeurs de l'échelle de couleurs.
    tickvals = [np.log1p(x) for x in [1, 10, 100, 1000, 10_000, 100_000, 1_000_000, 10_000_000]]
    ticktext = ['1', '10', '100', '1k', '10k', '100k', '1M', '10M']
    
    fig.update_layout(
        coloraxis_colorbar=dict(
            tickvals=tickvals,
            ticktext=ticktext
        )
    )

    # Retourner le treemap pour l'affichage dans Dash.
    return fig


def generate_graph5_content():
    
    fig = go.Figure(data=[go.Sankey(
    node=dict(
    pad=15,
    thickness=20,
    line=dict(color="black", width=0.5),
    label=labels,  # Labels de nœuds
    #color=node_colors  # Couleurs des nœuds
    ),
    link=dict(
      source=source,  # indices de la source
      target=target,  # indices de la cible
      value=value,  # valeurs correspondantes
      color=link_colors # Couleurs des liens
    ))])

    fig.update_layout(font_size=10, height=800)

    return html.Div(children=[
        html.H2(children=f'Diagramme de Sankey sur les types de catastrophes',style={'textAlign': 'center',},
            className= 'subtitle_color mb-4'),
        dcc.Graph(figure = fig),
        html.H2(children=f'Sun graph sur les types de catastrophes',style={'textAlign': 'center',},
            className= 'subtitle_color marge_top'),
        dcc.RangeSlider(id='year-slider',
                        className='RangeSlider',
                        marks={str(year): str(year) for year in annees if year %10 == 0},
                        min=min(annees),
                        max=max(annees),
                        value=[max(annees)-1, max(annees)],
                        step=1,
                        tooltip={"placement":"bottom","always_visible":True}),
        dcc.Graph(id='sunburst-plot')

    ])

# Callback pour mettre à jour le graphique
@app.callback(
    Output('sunburst-plot', 'figure'),
    [Input('year-slider', 'value')]
)
def update_graph5_content(selected_years):
    # Utiliser .loc pour filtrer le DataFrame et éviter SettingWithCopyWarning
    filtered_df = natural_disaster_df.loc[(natural_disaster_df['Year'] >= selected_years[0]) & (natural_disaster_df['Year'] <= selected_years[1])].copy()
    
    # Remplir les valeurs manquantes par des chaînes vides en utilisant .loc
    for col in ['Disaster Group', 'Disaster Subgroup', 'Disaster Type', 'Disaster Subtype', 'Disaster Subsubtype']:
        filtered_df.loc[:, col] = filtered_df[col].fillna('')

    # Construire des identifiants uniques
    filtered_df['GroupId'] = filtered_df['Disaster Group']
    filtered_df['SubgroupId'] = filtered_df['GroupId'] + '-' + filtered_df['Disaster Subgroup']
    filtered_df['TypeId'] = filtered_df['SubgroupId'] + '-' + filtered_df['Disaster Type']
    filtered_df['SubtypeId'] = filtered_df['TypeId'] + '-' + filtered_df['Disaster Subtype']
    filtered_df['SubsubtypeId'] = filtered_df['SubtypeId'] + '-' + filtered_df['Disaster Subsubtype']

    # Créer le diagramme en soleil
    fig = px.sunburst(filtered_df, path=['GroupId', 'SubgroupId', 'TypeId', 'SubtypeId', 'SubsubtypeId'], values='Total Deaths')
    fig.update_layout(height=1000)

    return fig

def generate_graph6_content():
    # Initialisation des graphiques avec des données par défaut ou vides
    fig1 = go.Figure()  # Un graphique vide ou initialisé avec des données par défaut
    fig2 = go.Figure()  # Un graphique vide ou initialisé avec des données par défaut

    fig1.update_layout(title='Diagramme en Soleil - Catastrophes Naturelles', height=1000)
    fig2.update_layout(height=600)

    # Préparation des composants de l'interface utilisateur
    return html.Div(children = [
        html.H2(children=f'Sun graph sur les types de catastrophes',style={'textAlign': 'center',},
            className= 'subtitle_color'),
        dcc.RangeSlider(
            id='year-slider2',
            className='RangeSlider',
            min=natural_disaster_df['Year'].min(),
            max=natural_disaster_df['Year'].max(),
            value=[natural_disaster_df['Year'].min(), natural_disaster_df['Year'].max()],
            marks={str(year): str(year) for year in range(natural_disaster_df['Year'].min(), natural_disaster_df['Year'].max() + 1, 10)},
            step=1,
            tooltip={"placement": "bottom", "always_visible": True}
        ),
        dcc.Graph(id='sunburst-plot2', figure=fig1),  # Graphique initial
        html.H2(children=f'Coût total des catastrophes par année',style={'textAlign': 'center',},
            className= 'subtitle_color marge_top mb-4'),
        dcc.Graph(id='cost-over-time-graph', figure=fig2)  # Autre graphique initial
    ])



@app.callback(
    [Output('sunburst-plot2', 'figure'),
     Output('cost-over-time-graph', 'figure')],
    [Input('year-slider2', 'value')]
)
def update_graph6_content(selected_years):
    # Filtrer le DataFrame en fonction de la plage d'années sélectionnée
    filtered_df = natural_disaster_df.loc[(natural_disaster_df['Year'] >= selected_years[0]) & (natural_disaster_df['Year'] <= selected_years[1])].copy()

    # Remplir les valeurs manquantes par des chaînes vides en utilisant .loc pour les colonnes hiérarchiques
    for col in ['Disaster Group', 'Disaster Subgroup', 'Disaster Type', 'Disaster Subtype', 'Disaster Subsubtype']:
        filtered_df.loc[:, col] = filtered_df[col].fillna('')

    # Remplir les valeurs manquantes par 0 pour la colonne des coûts
    filtered_df.loc[:, "Total Damages ('000 US$)"] = filtered_df["Total Damages ('000 US$)"].fillna(0)

    # Construire des identifiants uniques
    filtered_df['GroupId'] = filtered_df['Disaster Group']
    filtered_df['SubgroupId'] = filtered_df['GroupId'] + '-' + filtered_df['Disaster Subgroup']
    filtered_df['TypeId'] = filtered_df['SubgroupId'] + '-' + filtered_df['Disaster Type']
    filtered_df['SubtypeId'] = filtered_df['TypeId'] + '-' + filtered_df['Disaster Subtype']
    filtered_df['SubsubtypeId'] = filtered_df['SubtypeId'] + '-' + filtered_df['Disaster Subsubtype']

    # Créer le diagramme en soleil avec le coût des catastrophes
    fig1 = px.sunburst(filtered_df, path=['GroupId', 'SubgroupId', 'TypeId', 'SubtypeId', 'SubsubtypeId'], values="Total Damages ('000 US$)")

    # Graphique de coût total des catastrophes par année
    data_summarized = filtered_df.groupby('Year')['Total Damages (\'000 US$)'].sum().reset_index()
    data_summarized.columns = ['Year', 'TotalCost']
    fig2 = go.Figure(data=go.Scatter(x=data_summarized['Year'], y=data_summarized['TotalCost'], mode='lines+markers'))
    fig2.update_layout(xaxis_title='Année', yaxis_title='Coût Total (en milliers de dollars US)', height=600)

    return fig1, fig2

