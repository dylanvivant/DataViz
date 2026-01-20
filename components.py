"""
Composants réutilisables pour le dashboard
"""

import dash_bootstrap_components as dbc
from dash import html, dcc
from styles import COLORS


def create_kpi_card(number, title, value, icon, color_key='primary'):
    """Crée une carte KPI moderne avec design sombre"""
    
    color_map = {
        'primary': COLORS['primary'],
        'success': COLORS['success'],
        'warning': COLORS['warning'],
        'danger': COLORS['danger'],
        'info': COLORS['info']
    }
    
    color = color_map.get(color_key, COLORS['primary'])
    
    return dbc.Card([
        dbc.CardBody([
            html.Div([
                html.Div([
                    html.Span(
                        f"KPI {number}",
                        style={
                            'fontSize': '0.75rem',
                            'color': color,
                            'fontWeight': '600',
                            'textTransform': 'uppercase',
                            'letterSpacing': '1px'
                        }
                    )
                ], className="mb-2"),
                html.Div([
                    html.I(
                        className=f"fas fa-{icon}",
                        style={
                            'fontSize': '2rem',
                            'color': color,
                            'opacity': '0.8'
                        }
                    )
                ], className="mb-3"),
                html.H3(
                    value,
                    style={
                        'color': COLORS['text'],
                        'fontWeight': '700',
                        'fontSize': '1.75rem',
                        'marginBottom': '0.5rem'
                    }
                ),
                html.P(
                    title,
                    style={
                        'color': COLORS['text_muted'],
                        'fontSize': '0.875rem',
                        'marginBottom': '0',
                        'fontWeight': '500'
                    }
                )
            ], style={'textAlign': 'center', 'padding': '1rem 0'})
        ], style={'background': 'transparent'})
    ], className="kpi-card h-100", style={'border': 'none', 'background': '#1e293b'})


def create_graph_card(kpi_number, title, graph_id, icon="chart-line", scrollable=False, graph_height='400px'):
    """Crée une carte pour graphique avec header stylé"""
    
    graph_style = {'height': graph_height}
    body_style = {'padding': '20px', 'background': COLORS['surface']}
    
    if scrollable:
        body_style['maxHeight'] = '600px'
        body_style['overflowY'] = 'auto'
    
    return dbc.Card([
        html.Div([
            html.I(className=f"fas fa-{icon} me-2"),
            html.Span(f"KPI {kpi_number} : {title}", style={'fontWeight': '600'})
        ], className="card-header-dark", style={'color': 'white'}),
        dbc.CardBody([
            dcc.Graph(
                id=graph_id,
                config={
                    'displayModeBar': False,
                    'displaylogo': False
                },
                style=graph_style
            )
        ], style=body_style)
    ], className="graph-card", style={'border': 'none'})


def create_header():
    """En-tête du dashboard"""
    
    return html.Div([
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.I(
                            className="fas fa-chart-bar fa-2x mb-3",
                            style={'color': 'white'}
                        ),
                        html.H1(
                            "Dashboard Northwind",
                            style={
                                'color': 'white',
                                'fontWeight': '700',
                                'marginBottom': '0.5rem',
                                'fontSize': '2.5rem'
                            }
                        ),
                        html.P(
                            "Analyse des Ventes",
                            style={
                                'color': 'rgba(255,255,255,0.85)',
                                'fontSize': '1.1rem',
                                'marginBottom': '0'
                            }
                        )
                    ], style={'textAlign': 'center', 'padding': '2rem 0'})
                ])
            ])
        ], fluid=True)
    ], style={
        'background': f'linear-gradient(135deg, {COLORS["gradient_start"]} 0%, {COLORS["gradient_end"]} 100%)',
        'marginBottom': '2rem',
        'boxShadow': '0 4px 6px rgba(0,0,0,0.3)'
    })


def create_filters(countries, categories, min_date, max_date):
    """Section des filtres"""
    
    return dbc.Card([
        dbc.CardBody([
            html.Div([
                html.I(className="fas fa-filter me-2", style={'color': COLORS['primary']}),
                html.Span(
                    "Filtres Dynamiques",
                    style={'fontWeight': '600', 'fontSize': '1.1rem', 'color': COLORS['text']}
                )
            ], className="mb-3"),
            dbc.Row([
                dbc.Col([
                    html.Label(
                        [html.I(className="fas fa-calendar me-2"), "Période"],
                        style={'color': COLORS['text'], 'fontSize': '0.9rem', 'fontWeight': '500'}
                    ),
                    dcc.DatePickerRange(
                        id='date-filter',
                        start_date=min_date,
                        end_date=max_date,
                        display_format='DD/MM/YYYY',
                        style={'width': '100%'}
                    )
                ], md=4, className="mb-3"),
                dbc.Col([
                    html.Label(
                        [html.I(className="fas fa-globe me-2"), "Pays"],
                        style={'color': COLORS['text'], 'fontSize': '0.9rem', 'fontWeight': '500'}
                    ),
                    dcc.Dropdown(
                        id='country-filter',
                        options=[{'label': c, 'value': c} for c in countries],
                        multi=True,
                        placeholder="Tous les pays",
                        className="dark-dropdown"
                    )
                ], md=4, className="mb-3"),
                dbc.Col([
                    html.Label(
                        [html.I(className="fas fa-tags me-2"), "Catégories"],
                        style={'color': COLORS['text'], 'fontSize': '0.9rem', 'fontWeight': '500'}
                    ),
                    dcc.Dropdown(
                        id='category-filter',
                        options=[{'label': c, 'value': c} for c in categories],
                        multi=True,
                        placeholder="Toutes les catégories",
                        className="dark-dropdown"
                    )
                ], md=4, className="mb-3")
            ])
        ])
    ], className="filter-section", style={'border': 'none', 'marginBottom': '2rem'})
