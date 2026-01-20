"""
Dashboard Northwind avec 10 KPIs obligatoires + ML Clustering
Architecture modulaire avec thème sombre moderne et navigation multi-pages
"""

import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from data_model import DataModel
from components import create_kpi_card, create_graph_card, create_header, create_filters
from callbacks import register_callbacks
from styles import CUSTOM_CSS
import joblib
import pandas as pd
import numpy as np

# Initialiser le modèle de données
data_model = DataModel()

# Charger le modèle de clustering
try:
    model_artifacts = joblib.load('models/customer_clustering_model.pkl')
    cluster_data = pd.read_csv('data/enriched/customer_clusters.csv')
    print("✅ Modèle de clustering chargé avec succès")
except Exception as e:
    print(f"⚠️  Modèle de clustering non disponible: {e}")
    model_artifacts = None
    cluster_data = None

# Initialiser l'application Dash avec thème Bootstrap
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"
    ],
    suppress_callback_exceptions=True
)

app.title = "Dashboard Northwind - 10 KPIs"

# Exposer le serveur Flask pour Gunicorn
server = app.server

# Injecter le CSS personnalisé
app.index_string = f'''
<!DOCTYPE html>
<html>
    <head>
        {{%metas%}}
        <title>{{%title%}}</title>
        {{%favicon%}}
        {{%css%}}
        <style>{CUSTOM_CSS}</style>
    </head>
    <body>
        {{%app_entry%}}
        <footer>
            {{%config%}}
            {{%scripts%}}
            {{%renderer%}}
        </footer>
    </body>
</html>
'''

# Récupérer les données pour les filtres
countries = sorted(data_model.full_dataset['country'].dropna().unique())
categories = sorted(data_model.full_dataset['categoryName'].dropna().unique())
min_date = data_model.full_dataset['orderDate'].min()
max_date = data_model.full_dataset['orderDate'].max()

# Définir les labels des clusters
cluster_labels = {
    0: 'Low-Value Inactive',
    1: 'Lost Customers',
    2: 'VIP Premium'
}

# ===== LAYOUTS DES PAGES =====

# Layout Dashboard principal
dashboard_layout = html.Div([
    # Section filtres
    create_filters(countries, categories, min_date, max_date),
    
    # Section KPIs (1-5)
    dbc.Row([
        dbc.Col(create_kpi_card(1, "Chiffre d'Affaires Total", html.Span(id='kpi-ca'), "dollar-sign", 'primary'), md=12, lg=2, className="mb-3"),
        dbc.Col(create_kpi_card(2, "Nombre de Commandes", html.Span(id='kpi-orders'), "shopping-cart", 'success'), md=6, lg=2, className="mb-3"),
        dbc.Col(create_kpi_card(3, "Clients Uniques", html.Span(id='kpi-clients'), "users", 'info'), md=6, lg=2, className="mb-3"),
        dbc.Col(create_kpi_card(4, "Panier Moyen", html.Span(id='kpi-panier'), "shopping-basket", 'warning'), md=6, lg=3, className="mb-3"),
        dbc.Col(create_kpi_card(5, "Quantité Moy./Commande", html.Span(id='kpi-qty'), "box", 'danger'), md=6, lg=3, className="mb-3"),
    ], className="mb-4"),
    
    # KPI 6 - Évolution temporelle en pleine largeur
    dbc.Row([
        dbc.Col(create_graph_card(6, "Évolution du CA par Mois", "graph-evolution-ca", "chart-line"), md=12, className="mb-4"),
    ]),
    
    # KPI 7 - Top 10 Produits en pleine largeur pour meilleure lisibilité des noms
    dbc.Row([
        dbc.Col(create_graph_card(7, "Top 10 Produits par CA", "graph-top-products", "trophy", graph_height='550px'), md=12, className="mb-4"),
    ]),
    
    # KPIs 8 & 9 - Disposition 50/50 pour meilleure lisibilité
    dbc.Row([
        dbc.Col(create_graph_card(8, "Répartition du CA par Pays", "graph-ca-pays", "globe"), md=12, lg=6, className="mb-4"),
        dbc.Col(create_graph_card(9, "Top 5 Clients", "graph-top-clients", "star"), md=12, lg=6, className="mb-4"),
    ]),
    
    # KPI 10 - Pleine largeur pour maximiser la visibilité de l'évolution temporelle
    dbc.Row([
        dbc.Col(create_graph_card(10, "Évolution des Commandes", "graph-evolution-orders", "chart-bar"), md=12, className="mb-4"),
    ]),
])

# Layout Page Prédiction
prediction_layout = html.Div([
    dbc.Row([
        dbc.Col([
            html.H2([html.I(className="fas fa-robot me-2"), "Prédiction de Cluster Client"], className="mb-4"),
            html.P("Entrez les caractéristiques d'un client pour prédire son segment.", className="text-muted mb-4"),
            
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Label("Récence (jours depuis dernière commande)", className="form-label"),
                            dbc.Input(id='input-recency', type='number', placeholder='Ex: 15', value=15, min=0),
                        ], md=6, className="mb-3"),
                        dbc.Col([
                            html.Label("Fréquence (nombre de commandes)", className="form-label"),
                            dbc.Input(id='input-frequency', type='number', placeholder='Ex: 12', value=12, min=1),
                        ], md=6, className="mb-3"),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            html.Label("Montant total dépensé ($)", className="form-label"),
                            dbc.Input(id='input-monetary', type='number', placeholder='Ex: 5000', value=5000, min=0),
                        ], md=6, className="mb-3"),
                        dbc.Col([
                            html.Label("Réduction moyenne (%)", className="form-label"),
                            dbc.Input(id='input-discount', type='number', placeholder='Ex: 5', value=5, min=0, max=100, step=0.1),
                        ], md=6, className="mb-3"),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            html.Label("Jours moyens entre commandes", className="form-label"),
                            dbc.Input(id='input-days-between', type='number', placeholder='Ex: 25', value=25, min=0),
                        ], md=6, className="mb-3"),
                        dbc.Col([
                            html.Label("Ratio commandes récentes (0-1)", className="form-label"),
                            dbc.Input(id='input-recent-ratio', type='number', placeholder='Ex: 0.42', value=0.42, min=0, max=1, step=0.01),
                        ], md=6, className="mb-3"),
                    ]),
                    html.Hr(className="my-4"),
                    dbc.Button([html.I(className="fas fa-magic me-2"), "Prédire le Cluster"], 
                              id='btn-predict', color='primary', size='lg', className="w-100"),
                ])
            ], className="shadow-sm mb-4"),
            
            html.Div(id='prediction-result', className="mt-4")
            
        ], md=12, lg=8, className="mx-auto")
    ])
])

# Layout Page Clusters
clusters_layout = html.Div([
    html.H2([html.I(className="fas fa-users me-2"), "Analyse des Segments Clients"], className="mb-4"),
    
    # Sélecteur de cluster
    dbc.Row([
        dbc.Col([
            html.Label("Sélectionnez un segment client :", className="form-label mb-3"),
            dbc.ButtonGroup([
                dbc.Button([html.I(className="fas fa-user-slash me-2"), "Low-Value Inactive"], 
                          id='btn-cluster-0', color='warning', outline=True, className="me-2"),
                dbc.Button([html.I(className="fas fa-user-times me-2"), "Lost Customers"], 
                          id='btn-cluster-1', color='danger', outline=True, className="me-2"),
                dbc.Button([html.I(className="fas fa-crown me-2"), "VIP Premium"], 
                          id='btn-cluster-2', color='success', outline=True),
            ], className="mb-4 w-100", style={'flexWrap': 'wrap'})
        ], md=12)
    ]),
    
    # Contenu du cluster sélectionné
    html.Div(id='cluster-content')
])

# Layout de l'application
app.layout = html.Div([
    # URL pour la navigation
    dcc.Location(id='url', refresh=False),
    
    # Header avec navigation
    html.Div([
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.H1([
                        html.I(className="fas fa-chart-line me-3"),
                        "Dashboard Northwind"
                    ], className="header-title"),
                    html.P("Analyse des ventes et segmentation client", className="header-subtitle")
                ], md=6),
                dbc.Col([
                    dbc.Nav([
                        dbc.NavItem(dbc.NavLink([html.I(className="fas fa-chart-bar me-2"), "Dashboard"], 
                                                href="/", id="nav-dashboard", active=True)),
                        dbc.NavItem(dbc.NavLink([html.I(className="fas fa-robot me-2"), "Prédiction"], 
                                                href="/prediction", id="nav-prediction")),
                        dbc.NavItem(dbc.NavLink([html.I(className="fas fa-users me-2"), "Clusters"], 
                                                href="/clusters", id="nav-clusters")),
                    ], pills=True, className="justify-content-end")
                ], md=6, className="d-flex align-items-center justify-content-end")
            ])
        ], fluid=True, className="py-3")
    ], className="header-container"),
    
    # Container principal
    dbc.Container([
        # Contenu de la page
        html.Div(id='page-content')
    ], fluid=True, style={'padding': '2rem'}),
    
    # Footer
    html.Div([
        dbc.Container([
            html.Hr(style={'borderColor': 'rgba(255,255,255,0.1)', 'margin': '2rem 0'}),
            html.P(
                "Dashboard Northwind - TP DataViz + ML Clustering",
                style={'textAlign': 'center', 'color': '#94a3b8', 'fontSize': '0.875rem'}
            )
        ], fluid=True)
    ])
])

# Enregistrer tous les callbacks
register_callbacks(app, data_model)

# Enregistrer les callbacks ML si le modèle est disponible
if model_artifacts is not None:
    from ml_callbacks import register_ml_callbacks
    register_ml_callbacks(app, data_model, model_artifacts, cluster_data)

if __name__ == '__main__':
    print("🚀 Lancement du dashboard Northwind...")
    print(f"📊 Données chargées: {len(data_model.full_dataset)} lignes")
    print("🌐 Accéder à: http://127.0.0.1:8050")
    app.run_server(debug=True)
