"""
Callbacks pour les fonctionnalités ML (prédiction et analyse de clusters)
"""

from dash import Input, Output, State, html, ctx
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from dash import dcc


def register_ml_callbacks(app, data_model, model_artifacts, cluster_data):
    """
    Enregistre tous les callbacks liés au ML
    """
    
    # Définir les labels des clusters
    cluster_labels = {
        0: 'Low-Value Inactive',
        1: 'Lost Customers',
        2: 'VIP Premium'
    }
    
    # Callback pour la navigation entre pages
    @app.callback(
        [Output('page-content', 'children'),
         Output('nav-dashboard', 'active'),
         Output('nav-prediction', 'active'),
         Output('nav-clusters', 'active')],
        Input('url', 'pathname')
    )
    def display_page(pathname):
        # Import des layouts (doit être fait ici pour éviter les imports circulaires)
        from app import dashboard_layout, prediction_layout, clusters_layout
        
        if pathname == '/prediction':
            return prediction_layout, False, True, False
        elif pathname == '/clusters':
            return clusters_layout, False, False, True
        else:  # '/' ou autre
            return dashboard_layout, True, False, False
    
    # Callback pour la prédiction
    @app.callback(
        Output('prediction-result', 'children'),
        Input('btn-predict', 'n_clicks'),
        [State('input-recency', 'value'),
         State('input-frequency', 'value'),
         State('input-monetary', 'value'),
         State('input-discount', 'value'),
         State('input-days-between', 'value'),
         State('input-recent-ratio', 'value')]
    )
    def predict_cluster(n_clicks, recency, frequency, monetary, discount, days_between, recent_ratio):
        if not n_clicks or model_artifacts is None:
            return html.Div()
        
        try:
            # Validation des inputs
            if None in [recency, frequency, monetary, discount, days_between, recent_ratio]:
                return dbc.Alert("⚠️ Veuillez remplir tous les champs", color="warning")
            
            # Préparer les données
            customer_features = {
                'recency': recency,
                'frequency': frequency,
                'monetary': monetary,
                'avg_discount': discount / 100,  # Convertir en décimal
                'avg_days_between_orders': days_between,
                'recent_ratio': recent_ratio
            }
            
            # Créer un DataFrame
            customer_df = pd.DataFrame([customer_features])
            
            # Appliquer la transformation log à monetary
            feature_cols = model_artifacts['feature_columns']
            if 'monetary_log' in feature_cols:
                customer_df['monetary_log'] = np.log1p(customer_df['monetary'])
            
            # Sélectionner les features dans le bon ordre
            customer_df = customer_df[feature_cols]
            
            # Normaliser
            scaler = model_artifacts['scaler']
            customer_scaled = scaler.transform(customer_df)
            
            # Prédire
            kmeans = model_artifacts['kmeans_model']
            cluster = kmeans.predict(customer_scaled)[0]
            
            # Récupérer le label et les statistiques du cluster
            label = cluster_labels.get(cluster, f'Cluster {cluster}')
            cluster_profile = model_artifacts['cluster_profiles'].loc[cluster]
            
            # Définir la couleur selon le cluster
            color_map = {0: 'warning', 1: 'danger', 2: 'success'}
            color = color_map.get(cluster, 'info')
            
            # Créer le résultat
            result = dbc.Card([
                dbc.CardBody([
                    html.H3([
                        html.I(className=f"fas fa-{'user-slash' if cluster==0 else 'user-times' if cluster==1 else 'crown'} me-3"),
                        f"Segment prédit : {label}"
                    ], className=f"text-{color} mb-3"),
                    
                    html.Hr(),
                    
                    html.H5("📊 Profil du segment", className="mb-3"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.P("Récence moyenne", className="text-muted mb-1"),
                                    html.H4(f"{cluster_profile.get('recency', 0):.0f} jours", className="mb-0")
                                ])
                            ], className="text-center mb-2")
                        ], md=4),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.P("Fréquence moyenne", className="text-muted mb-1"),
                                    html.H4(f"{cluster_profile.get('frequency', 0):.1f} cmd", className="mb-0")
                                ])
                            ], className="text-center mb-2")
                        ], md=4),
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    html.P("Montant moyen", className="text-muted mb-1"),
                                    html.H4(f"${cluster_profile.get('monetary', 0):.0f}", className="mb-0")
                                ])
                            ], className="text-center mb-2")
                        ], md=4),
                    ]),
                    
                    html.Hr(className="my-3"),
                    
                    html.Div([
                        html.H5("💡 Recommandations", className="mb-2"),
                        html.Ul([
                            html.Li(get_recommendation(cluster, 0)),
                            html.Li(get_recommendation(cluster, 1)),
                            html.Li(get_recommendation(cluster, 2)),
                        ])
                    ])
                ])
            ], color=color, outline=True, className="shadow")
            
            return result
            
        except Exception as e:
            return dbc.Alert(f"❌ Erreur lors de la prédiction : {str(e)}", color="danger")
    
    # Callbacks pour la sélection de cluster
    @app.callback(
        Output('cluster-content', 'children'),
        [Input('btn-cluster-0', 'n_clicks'),
         Input('btn-cluster-1', 'n_clicks'),
         Input('btn-cluster-2', 'n_clicks')]
    )
    def display_cluster_analysis(n0, n1, n2):
        # Déterminer quel bouton a été cliqué
        triggered_id = ctx.triggered_id
        
        if triggered_id is None:
            cluster_id = 2  # Par défaut, afficher VIP Premium
        else:
            cluster_id = int(triggered_id.split('-')[-1])
        
        if cluster_data is None:
            return dbc.Alert("⚠️ Données de clustering non disponibles", color="warning")
        
        try:
            # Filtrer les clients du cluster
            cluster_customers = cluster_data[cluster_data['cluster'] == cluster_id]['customerID'].tolist()
            
            # Filtrer les données du data_model
            cluster_orders = data_model.full_dataset[
                data_model.full_dataset['customerID'].isin(cluster_customers)
            ].copy()
            
            if len(cluster_orders) == 0:
                return dbc.Alert(f"⚠️ Aucune donnée pour ce cluster", color="warning")
            
            # Calculer les métriques
            total_revenue = cluster_orders['lineTotal'].sum()
            avg_basket = cluster_orders.groupby('orderID')['lineTotal'].sum().mean()
            num_customers = len(cluster_customers)
            num_orders = cluster_orders['orderID'].nunique()
            
            # Calcul des jours moyens entre commandes
            orders_by_customer = cluster_orders.groupby('customerID')['orderDate'].apply(
                lambda x: x.sort_values().diff().dt.days.mean() if len(x) > 1 else 0
            )
            avg_days_between = orders_by_customer.mean()
            
            # Top 10 produits
            top_products = cluster_orders.groupby('productName').agg({
                'quantity': 'sum',
                'lineTotal': 'sum'
            }).sort_values('lineTotal', ascending=False).head(10)
            
            # Créer le graphique top produits
            fig_products = px.bar(
                top_products.reset_index(),
                x='lineTotal',
                y='productName',
                orientation='h',
                title=f'Top 10 Produits - {cluster_labels[cluster_id]}',
                labels={'lineTotal': 'Chiffre d\'Affaires ($)', 'productName': 'Produit'},
                color='lineTotal',
                color_continuous_scale='Viridis'
            )
            fig_products.update_layout(
                template='plotly_dark',
                showlegend=False,
                height=450
            )
            
            # Évolution temporelle
            monthly_data = cluster_orders.groupby(
                cluster_orders['orderDate'].dt.to_period('M')
            ).agg({
                'lineTotal': 'sum',
                'orderID': 'nunique'
            }).reset_index()
            monthly_data['orderDate'] = monthly_data['orderDate'].dt.to_timestamp()
            
            fig_evolution = go.Figure()
            fig_evolution.add_trace(go.Scatter(
                x=monthly_data['orderDate'],
                y=monthly_data['lineTotal'],
                mode='lines+markers',
                name='CA Mensuel',
                line=dict(color='#00d4ff', width=3)
            ))
            fig_evolution.update_layout(
                template='plotly_dark',
                title=f'Évolution du CA - {cluster_labels[cluster_id]}',
                xaxis_title='Mois',
                yaxis_title='Chiffre d\'Affaires ($)',
                height=450
            )
            
            # Layout du résultat
            result = html.Div([
                # KPIs du cluster
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.Div([
                                    html.I(className="fas fa-users fa-2x mb-2", style={'color': '#00d4ff'}),
                                    html.H6("Clients", style={'color': '#f1f5f9'}, className="mb-1"),
                                    html.H3(f"{num_customers}", className="mb-0")
                                ], className="text-center")
                            ])
                        ], className="shadow-sm")
                    ], md=3, className="mb-3"),
                    
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.Div([
                                    html.I(className="fas fa-shopping-cart fa-2x mb-2", style={'color': '#00ff88'}),
                                    html.H6("Commandes", style={'color': '#f1f5f9'}, className="mb-1"),
                                    html.H3(f"{num_orders}", className="mb-0")
                                ], className="text-center")
                            ])
                        ], className="shadow-sm")
                    ], md=3, className="mb-3"),
                    
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.Div([
                                    html.I(className="fas fa-shopping-basket fa-2x mb-2", style={'color': '#ffd700'}),
                                    html.H6("Panier Moyen", style={'color': '#f1f5f9'}, className="mb-1"),
                                    html.H3(f"${avg_basket:,.0f}", className="mb-0")
                                ], className="text-center")
                            ])
                        ], className="shadow-sm")
                    ], md=3, className="mb-3"),
                    
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.Div([
                                    html.I(className="fas fa-calendar-alt fa-2x mb-2", style={'color': '#ff6b6b'}),
                                    html.H6("Jours entre cmd", style={'color': '#f1f5f9'}, className="mb-1"),
                                    html.H3(f"{avg_days_between:.0f}", className="mb-0")
                                ], className="text-center")
                            ])
                        ], className="shadow-sm")
                    ], md=3, className="mb-3"),
                ]),
                
                # Graphiques
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                dcc.Graph(figure=fig_products)
                            ])
                        ], className="shadow-sm")
                    ], md=6, className="mb-3"),
                    
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                dcc.Graph(figure=fig_evolution)
                            ])
                        ], className="shadow-sm")
                    ], md=6, className="mb-3"),
                ])
            ])
            
            return result
            
        except Exception as e:
            return dbc.Alert(f"❌ Erreur lors de l'analyse : {str(e)}", color="danger")


def get_recommendation(cluster_id, rec_index):
    """
    Retourne une recommandation basée sur le cluster
    """
    recommendations = {
        0: [  # Low-Value Inactive
            "Campagne de réactivation avec offre spéciale pour relancer l'engagement",
            "Programme de fidélité avec récompenses pour augmenter la fréquence",
            "Communication ciblée pour comprendre les raisons de l'inactivité"
        ],
        1: [  # Lost Customers
            "Campagne de reconquête avec une offre irrésistible (réduction importante)",
            "Enquête de satisfaction pour identifier les causes de départ",
            "Programme VIP avec avantages exclusifs pour les encourager à revenir"
        ],
        2: [  # VIP Premium
            "Programme VIP avec service premium et avantages exclusifs",
            "Accès prioritaire aux nouveaux produits et promotions privées",
            "Communication personnalisée et suivi dédié pour maintenir la satisfaction"
        ]
    }
    
    return recommendations.get(cluster_id, ["Recommandation non disponible"])[rec_index]
