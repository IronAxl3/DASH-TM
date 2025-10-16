import dash
from dash import dcc, html
import plotly.graph_objects as go
import numpy as np

dash.register_page(__name__)

layout = html.Div(style={
    'display': 'flex',
    'height': 'calc(100vh - 60px)',
    'margin': '0',
    'padding': '0',
    'fontFamily': 'sans-serif',
    'fontSize': '14px',
    'lineHeight': '1.6',
    'color': '#202122',
    'backgroundColor': '#f8f9fa'
}, children=[
    html.Div(style={
        'width': '50%',
        'padding': '20px',
        'overflowY': 'auto',
        'backgroundColor': 'white',
        'borderRight': '1px solid #a2a9b1',
        'boxSizing': 'border-box'
    }, children=[
        dcc.Markdown("""
        Para modelar el crecimiento de la población mediante una ecuación diferencial, primero 
        tenemos que introducir algunas variables y términos relevantes. La variable $t$
        representará el tiempo. Las unidades de tiempo pueden ser horas, días, semanas, 
        meses o incluso años. Cualquier problema dado debe especificar las unidades utilizadas 
        en ese problema en particular. La variable $P$
        representará a la población. Como la población varía con el tiempo, se entiende que es 
        una función del tiempo. Por lo tanto, utilizamos la notación $P(t)$
        para la población en función del tiempo. Si $P(t)$
        es una función diferenciable, entonces la primera derivada $\\dfrac{dP}{dt}$
        representa la tasa instantánea de cambio de la población en función del tiempo.
        """, mathjax=True),
        
        dcc.Markdown("""
        Un ejemplo de función de crecimiento exponencial es  $P(t)=P_0e^{rt}$.
        En esta función,  $P(t)$
        representa la población en el momento  $t$, $P_0$
        representa la población inicial (población en el tiempo  $t=0$),
        y la constante  $r>0$
        se denomina tasa de crecimiento. Aquí  $P_0=100$ y  $r=0,03$.
        """, mathjax=True)
    ]),
    
    html.Div(style={
        'width': '50%',
        'padding': '20px',
        'backgroundColor': 'white',
        'boxSizing': 'border-box',
        'display': 'flex',
        'flexDirection': 'column',
        'justifyContent': 'center',
        'alignItems': 'center',
        'borderLeft': '1px solid #a2a9b1'
    }, children=[
        html.Div(style={'width': '100%', 'height': '100%'}, children=[
            dcc.Graph(
                id='population-growth-graph',
                figure={
                    'data': [{
                        'x': list(np.linspace(0, 100, 10)),  
                        'y': list(100 * np.exp(0.03 * np.linspace(0, 100, 10))),  
                        'line': {
                            'dash': 'solid',
                            'color': 'var(--uv-bio)',
                            'width': 2
                        },
                        'marker': {
                            'color': 'var(--uv-mate)',
                            'symbol': 'circle',
                            'size': 8
                        },
                        'name': 'P(t) = P₀eʳᵗ',
                        'hovertemplate': 't: %{x:.2f}<br>P(t): %{y:.2f}<extra></extra>'
                    }],
                    'layout': {
                        'title': {
                            'text': '<b>Crecimiento de la población</b>',
                            'font': {
                                'size': 20,
                                'color': 'var(--uv-navbar)'
                            },
                            'x': 0.5,
                            'y': 0.93
                        },
                        'xaxis': {
                            'title': 'Tiempo (t)',
                            'showgrid': True,
                            'gridcolor': 'var(--uv-sombra)',
                            'zeroline': True,
                            'zerolinecolor': 'var(--uv-texto2)',
                            'showline': True,
                            'linecolor': 'var(--uv-texto2)',
                            'linewidth': 1,
                            'mirror': True,
                            'title_font': {'size': 14, 'color': 'var(--uv-texto)'},
                            'tickfont': {'size': 12, 'color': 'var(--uv-texto2)'}
                        },
                        'yaxis': {
                            'title': 'Población P(t)',
                            'showgrid': True,
                            'gridcolor': 'var(--uv-sombra)',
                            'zeroline': True,
                            'zerolinecolor': 'var(--uv-texto2)',
                            'showline': True,
                            'linecolor': 'var(--uv-texto2)',
                            'linewidth': 1,
                            'mirror': True,
                            'title_font': {'size': 14, 'color': 'var(--uv-texto)'},
                            'tickfont': {'size': 12, 'color': 'var(--uv-texto2)'}
                        },
                        'margin': {'l': 60, 'r': 30, 't': 60, 'b': 60},
                        'paper_bgcolor': 'rgba(0,0,0,0)',
                        'plot_bgcolor': 'var(--uv-blanco)',
                        'font': {
                            'family': 'Segoe UI, Arial, sans-serif',
                            'size': 13,
                            'color': 'var(--uv-texto)'
                        },
                        'legend': {
                            'font': {'size': 12, 'color': 'var(--uv-texto2)'},
                            'bgcolor': 'rgba(0,0,0,0)',
                            'bordercolor': 'var(--uv-sombra)',
                            'borderwidth': 1,
                            'x': 0.02,
                            'y': 0.98,
                            'yanchor': 'top',
                            'xanchor': 'left'
                        }
                    }
                },
                style={
                    'height': '100%',
                    'width': '100%',
                    'border': '1px solid #c8ccd1',
                    'backgroundColor': 'white'
                }
            )
        ])
    ])
])