"""
Callbacks pour les interactions du dashboard
"""

from dash import Input, Output
import plotly.graph_objects as go
from styles import GRAPH_LAYOUT, COLORS


def register_callbacks(app, data_model):
    """Enregistre tous les callbacks de l'application"""
    
    @app.callback(
        Output('kpi-ca', 'children'),
        Output('kpi-orders', 'children'),
        Output('kpi-clients', 'children'),
        Output('kpi-panier', 'children'),
        Output('kpi-qty', 'children'),
        Input('date-filter', 'start_date'),
        Input('date-filter', 'end_date'),
        Input('country-filter', 'value'),
        Input('category-filter', 'value')
    )
    def update_kpis(start_date, end_date, countries, categories):
        """Met à jour les 5 premiers KPIs"""
        
        # Filtrer les données
        filtered = data_model.get_filtered_data(start_date, end_date, countries, categories)
        
        # Calculer les KPIs
        ca_total = filtered['lineTotal'].sum()
        nb_orders = filtered['orderID'].nunique()
        nb_clients = filtered['customerID'].nunique()
        panier_moyen = ca_total / nb_orders if nb_orders > 0 else 0
        qty_moyenne = filtered['quantity'].sum() / nb_orders if nb_orders > 0 else 0
        
        return (
            f"${ca_total:,.0f}",
            f"{nb_orders:,}",
            f"{nb_clients}",
            f"${panier_moyen:,.2f}",
            f"{qty_moyenne:.1f}"
        )
    
    @app.callback(
        Output('graph-evolution-ca', 'figure'),
        Input('date-filter', 'start_date'),
        Input('date-filter', 'end_date'),
        Input('country-filter', 'value'),
        Input('category-filter', 'value')
    )
    def update_evolution_ca(start_date, end_date, countries, categories):
        """KPI 6: Évolution du CA par mois"""
        
        filtered = data_model.get_filtered_data(start_date, end_date, countries, categories)
        monthly_sales = filtered.groupby(filtered['orderDate'].dt.to_period('M'))['lineTotal'].sum()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=[str(period) for period in monthly_sales.index],
            y=monthly_sales.values,
            mode='lines+markers',
            name='CA mensuel',
            line=dict(color=COLORS['primary'], width=3),
            marker=dict(size=8),
            fill='tozeroy',
            fillcolor=f'rgba({int(COLORS["primary"][1:3], 16)}, {int(COLORS["primary"][3:5], 16)}, {int(COLORS["primary"][5:7], 16)}, 0.2)'
        ))
        
        fig.update_layout(
            **GRAPH_LAYOUT,
            title="Évolution du Chiffre d'Affaires Mensuel",
            xaxis_title="Mois",
            yaxis_title="Chiffre d'Affaires ($)"
        )
        
        return fig
    
    @app.callback(
        Output('graph-top-products', 'figure'),
        Input('date-filter', 'start_date'),
        Input('date-filter', 'end_date'),
        Input('country-filter', 'value'),
        Input('category-filter', 'value')
    )
    def update_top_products(start_date, end_date, countries, categories):
        """KPI 7: Top 10 produits par CA"""
        
        filtered = data_model.get_filtered_data(start_date, end_date, countries, categories)
        top_products = filtered.groupby('productName')['lineTotal'].sum().nlargest(10).sort_values()
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=top_products.values,
            y=top_products.index,
            orientation='h',
            marker=dict(
                color=top_products.values,
                colorscale=[[0, COLORS['info']], [1, COLORS['primary']]],
                showscale=False
            ),
            text=[f"${v:,.0f}" for v in top_products.values],
            textposition='outside'
        ))
        
        fig.update_layout(
            **GRAPH_LAYOUT,
            title="Top 10 Produits par Chiffre d'Affaires",
            xaxis_title="Chiffre d'Affaires ($)",
            yaxis_title="",
            height=500
        )
        
        return fig
    
    @app.callback(
        Output('graph-ca-pays', 'figure'),
        Input('date-filter', 'start_date'),
        Input('date-filter', 'end_date'),
        Input('country-filter', 'value'),
        Input('category-filter', 'value')
    )
    def update_ca_pays(start_date, end_date, countries, categories):
        """KPI 8: Répartition du CA par pays"""
        
        filtered = data_model.get_filtered_data(start_date, end_date, countries, categories)
        sales_by_country = filtered.groupby('country')['lineTotal'].sum().nlargest(15)
        
        colors_gradient = [COLORS['primary'], COLORS['success'], COLORS['warning'], 
                          COLORS['danger'], COLORS['info']] * 3
        
        fig = go.Figure()
        fig.add_trace(go.Pie(
            labels=sales_by_country.index,
            values=sales_by_country.values,
            hole=0.4,
            marker=dict(colors=colors_gradient[:len(sales_by_country)], line=dict(color=COLORS['background'], width=2)),
            textposition='auto',
            textinfo='label+percent',
            hovertemplate='<b>%{label}</b><br>CA: $%{value:,.0f}<br>Part: %{percent}<extra></extra>'
        ))
        
        fig.update_layout(
            **GRAPH_LAYOUT,
            title="Répartition du CA par Pays (Top 15)",
            showlegend=False
        )
        
        return fig
    
    @app.callback(
        Output('graph-top-clients', 'figure'),
        Input('date-filter', 'start_date'),
        Input('date-filter', 'end_date'),
        Input('country-filter', 'value'),
        Input('category-filter', 'value')
    )
    def update_top_clients(start_date, end_date, countries, categories):
        """KPI 9: Top 5 clients"""
        
        filtered = data_model.get_filtered_data(start_date, end_date, countries, categories)
        top_clients = filtered.groupby('companyName')['lineTotal'].sum().nlargest(5).sort_values(ascending=True)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=top_clients.values,
            y=top_clients.index,
            orientation='h',
            marker=dict(
                color=[COLORS['success'], COLORS['info'], COLORS['primary'], 
                       COLORS['warning'], COLORS['danger']],
                line=dict(color=COLORS['background'], width=1)
            ),
            text=[f"${v:,.0f}" for v in top_clients.values],
            textposition='outside'
        ))
        
        fig.update_layout(
            **GRAPH_LAYOUT,
            title="Top 5 Clients par Chiffre d'Affaires",
            xaxis_title="Chiffre d'Affaires ($)",
            yaxis_title=""
        )
        
        return fig
    
    @app.callback(
        Output('graph-evolution-orders', 'figure'),
        Input('date-filter', 'start_date'),
        Input('date-filter', 'end_date'),
        Input('country-filter', 'value'),
        Input('category-filter', 'value')
    )
    def update_evolution_orders(start_date, end_date, countries, categories):
        """KPI 10: Évolution du nombre de commandes"""
        
        filtered = data_model.get_filtered_data(start_date, end_date, countries, categories)
        monthly_orders = filtered.groupby(filtered['orderDate'].dt.to_period('M'))['orderID'].nunique()
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=[str(period) for period in monthly_orders.index],
            y=monthly_orders.values,
            marker=dict(
                color=monthly_orders.values,
                colorscale=[[0, COLORS['info']], [1, COLORS['success']]],
                showscale=False,
                line=dict(color=COLORS['background'], width=1)
            ),
            text=monthly_orders.values,
            textposition='outside'
        ))
        
        fig.update_layout(
            **GRAPH_LAYOUT,
            title="Évolution du Nombre de Commandes par Mois",
            xaxis_title="Mois",
            yaxis_title="Nombre de Commandes"
        )
        
        return fig
