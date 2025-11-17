import dash
from dash import dcc, html, Input, Output, callback
import plotly.graph_objects as go
import numpy as np
from scipy.integrate import odeint

dash.register_page(__name__,
                   path="/clase6",
                   name="Clase 6: Modelo SEIR",
                   title="SEIR – DASH-TM")

def seir(y, t, N, beta, sigma, gamma):
    S, E, I, R = y
    dS = -beta * S * I / N
    dE = beta * S * I / N - sigma * E
    dI = sigma * E - gamma * I
    dR = gamma * I
    return [dS, dE, dI, dR]

layout = html.Div(className="page-container", children=[

    html.H2("Modelo SEIR con período de incubación", className="titulo-viva"),

    html.Div(className="fila-40-60", children=[

        html.Div(className="col-40 card-viva", children=[
            html.H4("Parámetros", className="subt-viva"),

            html.Label("Población N", className="label-viva"),
            dcc.Input(id="N", type="number", value=1000, min=100, step=100,
                      className="input-viva"),

            html.Label("Tasa de transmisión β", className="label-viva"),
            dcc.Slider(id="beta", min=0.1, max=1, step=0.05, value=0.4,
                       marks={0.1:"0.1", 0.5:"0.5", 1:"1"},
                       tooltip={"placement":"bottom","always_visible":True}),

            html.Label("Tasa de incubación σ = 1/T_inc", className="label-viva"),
            dcc.Slider(id="sigma", min=0.1, max=1, step=0.05, value=0.33,
                       marks={0.1:"0.1", 0.5:"0.5", 1:"1"},
                       tooltip={"placement":"bottom","always_visible":True}),

            html.Label("Tasa de recuperación γ", className="label-viva"),
            dcc.Slider(id="gamma", min=0.05, max=0.5, step=0.05, value=0.1,
                       marks={0.05:"0.05", 0.25:"0.25", 0.5:"0.5"},
                       tooltip={"placement":"bottom","always_visible":True}),

            html.H6("Condiciones iniciales", className="subt-viva"),
            html.Label("Expuestos iniciales E₀", className="label-viva"),
            dcc.Input(id="E0", type="number", value=10, min=0, step=1,
                      className="input-viva"),
            html.Label("Infectados iniciales I₀", className="label-viva"),
            dcc.Input(id="I0", type="number", value=0, min=0, step=1,
                      className="input-viva"),

            dcc.Markdown(id="info-seir", mathjax=True,
                         className="context-viva mt-3")
        ]),

        html.Div(className="col-60", children=[
            dcc.Graph(id="seir-graph", style={"height":"70vh"})
        ])
    ])
])

@callback(
    Output("seir-graph", "figure"),
    Output("info-seir", "children"),
    Input("N", "value"),
    Input("beta", "value"),
    Input("sigma", "value"),
    Input("gamma", "value"),
    Input("E0", "value"),
    Input("I0", "value")
)
def update_seir(N, beta, sigma, gamma, E0, I0):
    if N is None or N <= 0: N = 1000
    if E0 is None or E0 < 0: E0 = 0
    if I0 is None or I0 < 0: I0 = 0
    S0 = N - E0 - I0
    R0 = 0
    t = np.linspace(0, 200, 500)

    sol = odeint(seir, [S0, E0, I0, R0], t, args=(N, beta, sigma, gamma))
    S, E, I, R = sol.T

    fig = go.Figure()
    fig.add_scatter(x=t, y=S, name="Susceptibles", line=dict(color="#004d80", width=2))
    fig.add_scatter(x=t, y=E, name="Expuestos", line=dict(color="#b35a00", width=2))
    fig.add_scatter(x=t, y=I, name="Infectados", line=dict(color="#d35400", width=2.5))
    fig.add_scatter(x=t, y=R, name="Recuperados", line=dict(color="#00846a", width=2))

    fig.update_layout(
        title="Dinámica SEIR",
        xaxis_title="Tiempo (días)",
        yaxis_title="Número de individuos",
        template="simple_white",
        hovermode="x unified",
        margin=dict(l=60, r=30, t=60, b=60),
        legend=dict(x=0.02, y=0.98)
    )

    texto = rf"""
    **Período de incubación** = 1/σ ≈ **{1/sigma:.1f} días**  
    **Período infeccioso** = 1/γ ≈ **{1/gamma:.1f} días**  
    **R₀** = β/γ ≈ **{beta/gamma:.2f}**
    """
    return fig, texto