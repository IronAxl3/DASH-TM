import dash
from dash import dcc, html, Input, Output, callback
import plotly.graph_objects as go
import numpy as np
from scipy.integrate import odeint

dash.register_page(__name__, path="/clase4",
                   name="Clase 4: Modelo SIR",
                   title="SIR – DASH-TM",
                   description="Simulador interactivo del modelo SIR clásico.")

def sir(y, t, N, beta, gamma):
    S, I, R = y
    dS = -beta * S * I / N
    dI = beta * S * I / N - gamma * I
    dR = gamma * I
    return [dS, dI, dR]

layout = html.Div([
    html.Div(style={
        'background': 'linear-gradient(135deg, #002b45 0%, #001f30 100%)',
        'color': 'white',
        'padding': '3rem 2rem',
        'textAlign': 'center',
        'borderBottom': '3px solid #00846a',
        'animation': 'fadeInUp 0.6s ease-out'
    }, children=[
        html.H1("Modelo SIR - Dinámica de Enfermedades", style={
            'margin': '0 0 0.5rem 0',
            'fontSize': '2.5rem',
            'fontWeight': '700',
            'letterSpacing': '-0.5px'
        }),
        html.P("Simulador interactivo de transmisión de enfermedades infecciosas", style={
            'margin': '0',
            'fontSize': '1.1rem',
            'color': '#b0b0b0',
            'fontWeight': '500'
        })
    ]),

    html.Div(className="page-container", style={'padding': '2rem'}, children=[

        html.Div(className="fila-40-60 gap-2", style={'gap': '2rem', 'animation': 'fadeInUp 0.6s ease-out 0.1s backwards'}, children=[

            html.Div(className="col-40 card-viva", style={
                'background': 'linear-gradient(135deg, #ffffff 0%, #f8fbfa 100%)',
                'borderRadius': '16px',
                'padding': '2.5rem',
                'boxShadow': '0 8px 32px rgba(0, 43, 69, 0.12)',
                'border': '1px solid rgba(0, 132, 106, 0.12)',
                'animation': 'slideInLeft 0.7s ease-out',
                'backdropFilter': 'blur(10px)'
            }, children=[
                html.H4("Panel de Control", className="titulo-viva", style={
                    'fontSize': '1.5rem',
                    'margin': '0 0 1.5rem 0',
                    'color': '#002b45',
                    'fontWeight': '700'
                }),

                html.Label("Población Total (N)", className="label-viva"),
                dcc.Input(id="N", type="number", value=1000, min=100, step=100, 
                         className="input-viva", style={'width': '100%', 'marginBottom': '1.5rem'}),

                html.Label("📊 Tasa de Transmisión (β)", className="label-viva"),
                dcc.Slider(id="beta", min=0.1, max=1, step=0.05, value=0.4,
                           marks={0.1: "0.1", 0.5: "0.5", 1: "1"},
                           tooltip={"placement": "bottom", "always_visible": True},
                           className="slider-viva"),

                html.Label("💉 Tasa de Recuperación (γ)", className="label-viva"),
                dcc.Slider(id="gamma", min=0.05, max=0.5, step=0.05, value=0.1,
                           marks={0.05: "0.05", 0.25: "0.25", 0.5: "0.5"},
                           tooltip={"placement": "bottom", "always_visible": True},
                           className="slider-viva"),

                html.H6("Condiciones Iniciales", className="subt-viva", style={
                    'fontSize': '0.95rem',
                    'fontWeight': '700',
                    'textTransform': 'uppercase',
                    'letterSpacing': '0.8px',
                    'marginTop': '1.5rem',
                    'marginBottom': '0.75rem'
                }),
                html.Label("🦠 Infectados Iniciales (I₀)", className="label-viva"),
                dcc.Input(id="I0", type="number", value=10, min=1, step=1, 
                         className="input-viva", style={'width': '100%', 'marginBottom': '1rem'}),

                html.Hr(className="hr-viva", style={'borderColor': 'rgba(0, 132, 106, 0.2)', 'margin': '2rem 0'}),
                dcc.Markdown(id="info-basic", mathjax=True, className="context-viva", style={
                    'padding': '1.5rem',
                    'background': 'linear-gradient(135deg, rgba(0, 132, 106, 0.06) 0%, rgba(0, 77, 128, 0.06) 100%)',
                    'borderLeft': '4px solid #00846a',
                    'borderRadius': '8px',
                    'fontSize': '0.95rem',
                    'lineHeight': '1.8',
                    'border': '1px solid rgba(0, 132, 106, 0.1)'
                })
            ]),

            html.Div(className="col-60", style={
                'animation': 'slideInRight 0.7s ease-out'
            }, children=[
                html.Div(style={
                    'background': 'white',
                    'borderRadius': '16px',
                    'padding': '2rem',
                    'boxShadow': '0 8px 32px rgba(0, 43, 69, 0.12)',
                    'border': '1px solid rgba(0, 132, 106, 0.12)',
                    'height': '100%'
                }, children=[
                    dcc.Graph(id="sir-graph", style={"height":"70vh"}, config={'displayModeBar': False})
                ])
            ])
        ])
    ])
], style={'margin': '0', 'padding': '0'})

@callback(
    Output("sir-graph", "figure"),
    Output("info-basic", "children"),
    Input("N", "value"),
    Input("beta", "value"),
    Input("gamma", "value"),
    Input("I0", "value")
)
def update_sir(N, beta, gamma, I0):
    N = int(N) if N else 1000
    beta = float(beta) if beta else 0.4
    gamma = float(gamma) if gamma else 0.1
    I0 = int(I0) if I0 else 10
    I0 = max(I0, 1)
    S0 = N - I0
    t = np.linspace(0, 160, 400)

    S, I, R = odeint(sir, [S0, I0, 0], t, args=(N, beta, gamma)).T

    fig = go.Figure()
    fig.add_scatter(x=t, y=S, name="Susceptibles", 
                   line=dict(color="#004d80", width=3.5),
                   fill='tozeroy',
                   fillcolor='rgba(0, 77, 128, 0.1)',
                   hovertemplate='<b>Susceptibles</b><br>t: %{x:.0f} días<br>S: %{y:.0f}<extra></extra>')
    fig.add_scatter(x=t, y=I, name="Infectados", 
                   line=dict(color="#b35a00", width=3.5),
                   fill='tozeroy',
                   fillcolor='rgba(179, 90, 0, 0.1)',
                   hovertemplate='<b>Infectados</b><br>t: %{x:.0f} días<br>I: %{y:.0f}<extra></extra>')
    fig.add_scatter(x=t, y=R, name="Recuperados", 
                   line=dict(color="#00846a", width=3.5),
                   fill='tozeroy',
                   fillcolor='rgba(0, 132, 106, 0.1)',
                   hovertemplate='<b>Recuperados</b><br>t: %{x:.0f} días<br>R: %{y:.0f}<extra></extra>')

    fig.update_layout(
        title={
            'text': '<b>Dinámica SIR - Compartimientos de Población</b>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': '#002b45', 'family': 'Linux Libertine, Georgia, serif'}
        },
        xaxis_title="<b>Tiempo (días)</b>",
        yaxis_title="<b>Número de Individuos</b>",
        template="plotly_white",
        hovermode="x unified",
        margin=dict(l=70, r=40, t=80, b=60),
        legend=dict(x=0.02, y=0.98, bgcolor="rgba(255,255,255,0.85)", bordercolor="rgba(0, 132, 106, 0.3)", borderwidth=1),
        plot_bgcolor="rgba(232, 245, 241, 0.3)",
        paper_bgcolor="rgba(248, 251, 250, 0.5)",
        font={"family": "Segoe UI, Arial, sans-serif", "size": 12, "color": "#212529"}
    )
    
    fig.update_xaxes(title_font={"size": 13, "color": "#002b45", "family": "Linux Libertine, Georgia, serif"},
                     showgrid=True, gridcolor="rgba(0, 43, 69, 0.1)", zeroline=False)
    fig.update_yaxes(title_font={"size": 13, "color": "#002b45", "family": "Linux Libertine, Georgia, serif"},
                     showgrid=True, gridcolor="rgba(0, 43, 69, 0.1)", zeroline=False)

    R0 = beta / gamma
    info = rf"""
    #### 📈 Análisis de Parámetros
    
    **Población**: {N} | **β** = {beta:.2f} | **γ** = {gamma:.2f}
    
    ---
    
    #### **Número Reproductivo Básico: R₀ = β/γ = {R0:.2f}**
    
    - 🔴 Si **R₀ < 1**: enfermedad desaparece rápidamente
    - 🟡 Si **R₀ = 1**: punto de inflexión epidémico  
    - 🟢 Si **R₀ > 1**: **potencial para epidemia**
    
    **Interpretación**: cada persona infectada contagia, en promedio, a **{R0:.2f}** personas.
    """
    return fig, info
