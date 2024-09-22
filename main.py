# Importation du module dash pour créer l'application web
import dash

# Importation des configurations depuis le fichier config.py
from config import *

# Importation de la mise en page depuis le fichier layout.py
from layout import layout

# Importation de composants bootstrap pour une mise en page stylisée
import dash_bootstrap_components as dbc

# Création de l'application Dash avec des styles externes de Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

# Importation des callbacks depuis le fichier callbacks.py
from callbacks import *

# Définition de la mise en page de l'application
app.layout = layout

# Point d'entrée principal pour exécuter l'application
if __name__ == '__main__':
    # Lancement du serveur en mode debug
    app.run_server(debug=True)
