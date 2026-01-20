"""
Styles et configuration visuelle du dashboard
"""

# Thème sombre moderne
COLORS = {
    'background': '#0f172a',
    'surface': '#1e293b',
    'surface_light': '#334155',
    'primary': '#3b82f6',
    'success': '#10b981',
    'warning': '#f59e0b',
    'danger': '#ef4444',
    'info': '#06b6d4',
    'text': '#f1f5f9',
    'text_muted': '#94a3b8',
    'border': '#334155',
    'gradient_start': "#F2CB05",
    'gradient_end': "#836D02"
}

GRAPH_LAYOUT = {
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)',
    'font': {
        'family': 'Inter, system-ui, sans-serif',
        'size': 12,
        'color': COLORS['text']
    },
    'margin': dict(l=20, r=20, t=30, b=20),
    'hovermode': 'closest',
    'xaxis': {
        'showgrid': False,
        'showline': True,
        'linecolor': COLORS['border'],
        'color': COLORS['text_muted']
    },
    'yaxis': {
        'showgrid': True,
        'gridcolor': COLORS['border'],
        'gridwidth': 0.5,
        'showline': False,
        'color': COLORS['text_muted']
    }
}

CUSTOM_CSS = """
    body {
        background: #0f172a !important;
    }
    
    .main-container {
        background: #0f172a;
        min-height: 100vh;
        padding: 20px;
    }
    
    .header-container {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border-bottom: 1px solid #334155;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    
    .header-title {
        color: #f1f5f9;
        font-weight: 700;
        font-size: 1.75rem;
        margin: 0;
    }
    
    .header-subtitle {
        color: #94a3b8;
        font-size: 0.875rem;
        margin: 0;
    }
    
    .nav-pills .nav-link {
        color: #94a3b8;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        margin: 0 0.25rem;
        transition: all 0.3s ease;
    }
    
    .nav-pills .nav-link:hover {
        background: rgba(59, 130, 246, 0.1);
        color: #3b82f6;
    }
    
    .nav-pills .nav-link.active {
        background: #3b82f6 !important;
        color: #ffffff !important;
    }
    
    .kpi-card {
        background: transparent !important;
        border-radius: 16px;
        border: 1px solid #334155;
        transition: all 0.3s ease;
    }
    
    .card-body {
        background: transparent !important;
    }
    
    .kpi-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 40px rgba(99, 102, 241, 0.2);
        border-color: #6366f1;
    }
    
    .graph-card {
        background: #1e293b;
        border-radius: 16px;
        border: 1px solid #334155;
        overflow: hidden;
    }
    
    .card-header-dark {
        background: transparent !important;
        padding: 16px 24px;
        border: none;
    }
    
    .filter-section {
        background: #1e293b;
        border-radius: 16px;
        border: 1px solid #334155;
        padding: 24px;
    }
    
    /* Personnalisation des dropdowns */
    .Select-control {
        background-color: #334155 !important;
        border-color: #475569 !important;
        color: #f1f5f9 !important;
    }
    
    /* DatePicker */
    .DateInput_input {
        background-color: #334155 !important;
        color: #f1f5f9 !important;
        border-color: #475569 !important;
    }
    
    /* Input forms */
    .form-control, .form-select, input[type="number"] {
        background-color: #334155 !important;
        color: #f1f5f9 !important;
        border-color: #475569 !important;
    }
    
    .form-control:focus, .form-select:focus, input[type="number"]:focus {
        background-color: #475569 !important;
        border-color: #3b82f6 !important;
        color: #f1f5f9 !important;
    }
    
    .form-label {
        color: #94a3b8;
        font-weight: 500;
    }
    
    /* Titres des pages */
    h2, h3, h4, h5, h6 {
        color: #f1f5f9 !important;
    }
    
    /* Textes et paragraphes */
    p, li, ul {
        color: #f1f5f9 !important;
    }
    
    .text-muted {
        color: #94a3b8 !important;
    }
    
    /* Forcer backgrounds sombres */
    .dash-graph, .js-plotly-plot {
        background: transparent !important;
    }
    
    #react-entry-point {
        background: #0f172a !important;
    }
    
    .card {
        background: #1e293b !important;
        border-color: #334155 !important;
    }
    
    /* Container Bootstrap */
    .container, .container-fluid {
        background: transparent !important;
    }
    
    /* Row et Col */
    .row, [class*="col-"] {
        background: transparent !important;
    }
    
    /* Tous les éléments de type card */
    .card, .card-body, .card-header {
        background-color: #1e293b !important;
    }
    
    /* Fond général de l'application */
    html, body, #_dash-app-content {
        background: #0f172a !important;
    }
"""
