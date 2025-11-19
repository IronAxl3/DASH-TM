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

layout = html.Div(className="page-container", children=[

    html.H2("Modelo SIR clásico", className="titulo-viva center"),
    html.P("Explora cómo cambian los compartimentos S-I-R al variar β y γ.", className="subtitulo-viva center"),

    html.Div(className="fila-40-60 gap-2", children=[

        html.Div(className="col-40 card-viva", children=[
            html.H4("Panel de control", className="subt-viva"),

            html.Label("Población total N", className="label-viva"),
            dcc.Input(id="N", type="number", value=1000, min=100, step=100, className="input-viva"),

            html.Label("Tasa de transmisión β", className="label-viva"),
            dcc.Slider(id="beta", min=0.1, max=1, step=0.05, value=0.4,
                       marks={0.1: "0.1", 0.5: "0.5", 1: "1"},
                       tooltip={"placement": "bottom", "always_visible": True},
                       className="slider-viva"),

            html.Label("Tasa de recuperación γ", className="label-viva"),
            dcc.Slider(id="gamma", min=0.05, max=0.5, step=0.05, value=0.1,
                       marks={0.05: "0.05", 0.25: "0.25", 0.5: "0.5"},
                       tooltip={"placement": "bottom", "always_visible": True},
                       className="slider-viva"),

            html.H6("Condiciones iniciales", className="subt-viva"),
            html.Label("Infectados iniciales I₀", className="label-viva"),
            dcc.Input(id="I0", type="number", value=10, min=1, step=1, className="input-viva"),

            html.Hr(className="hr-viva"),
            dcc.Markdown(id="info-basic", mathjax=True, className="context-viva")
        ]),

        html.Div(className="col-60", children=[
            dcc.Graph(id="sir-graph", className="graph-viva", config={'displayModeBar': False})
        ])
    ])
])

@callback(
    Output("sir-graph", "figure"),
    Output("info-basic", "children"),
    Input("N", "value"),
    Input("beta", "value"),
    Input("gamma", "value"),
    Input("I0", "value")
)
def update_sir(N, beta, gamma, I0):
    N = N or 1000
    I0 = max(I0 or 1, 1)
    S0 = N - I0
    t = np.linspace(0, 160, 400)

    S, I, R = odeint(sir, [S0, I0, 0], t, args=(N, beta, gamma)).T

    fig = go.Figure()
    fig.add_scatter(x=t, y=S, name="Susceptibles", line=dict(color="var(--uv-mate)", width=3))
    fig.add_scatter(x=t, y=I, name="Infectados", line=dict(color="var(--uv-graf)", width=3.5))
    fig.add_scatter(x=t, y=R, name="Recuperados", line=dict(color="var(--uv-bio)", width=3))

    fig.update_layout(
        title=dict(text="Dinámica S-I-R", x=0.5, font_size=20),
        xaxis_title="Tiempo (días)",
        yaxis_title="Individuos",
        template="simple_white",
        hovermode="x unified",
        margin=dict(l=40, r=20, t=60, b=40),
        legend=dict(x=0.02, y=0.98),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )

    R0 = beta / gamma
    info = rf"""
    **Población**: {N}  **β** = {beta}  **γ** = {gamma}  
    **R₀** = β/γ ≈ **{R0:.2f}**  
    - Si **R₀ < 1** la enfermedad desaparece.  
    - Si **R₀ > 1** puede generarse una epidemia.
    """
    return fig, info