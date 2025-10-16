import dash
from dash import html, dcc, Input, Output, callback
import plotly.graph_objects as go
import numpy as np

dash.register_page(__name__,
                   path="/clase3",
                   name="Clase 3: Crecimiento Poblacional",
                   title="Población – DASH-TM")

def solve_exp(r, P0, t):
    return P0 * np.exp(r * t)

def solve_log(r, K, P0, t):
    return K * P0 / (P0 + (K - P0) * np.exp(-r * t))

colores = {"exp": {"bg": "#d4f5e0", "line": "#00a085", "accent": "#00b894"},
           "log": {"bg": "#ffe2c2", "line": "#d35400", "accent": "#e17055"}}

layout = html.Div(className="page-container", children=[

    html.Div(className="fila-50-50", children=[

        html.Div(className="col-50 card-viva", id="control-card", children=[
            html.H4("Modelo y parámetros", className="titulo-viva"),

            dcc.RadioItems(id="modelo",
                options=[{"label": html.Span("📈 Exponencial", className="radio-label"), "value": "exp"},
                         {"label": html.Span("🌱 Logístico",   className="radio-label"), "value": "log"}],
                value="exp", inputClassName="radio-input", className="radio-group"
            ),

            html.Hr(),

            html.Label("Tasa de crecimiento  r", className="label-viva"),
            dcc.Slider(id="r", min=0.01, max=0.5, step=0.01, value=0.05,
                       marks={0.01:"0.01", 0.25:"0.25", 0.5:"0.5"},
                       tooltip={"placement":"bottom","always_visible":True}),

            html.Div(id="k-slider", children=[
                html.Label("Capacidad de carga  K", className="label-viva"),
                dcc.Slider(id="K", min=100, max=5000, step=100, value=1000,
                           marks={100:"100", 2500:"2500", 5000:"5000"},
                           tooltip={"placement":"bottom","always_visible":True})
            ]),

            html.H6("Población inicial  P₀", className="subt-viva"),
            dcc.Input(id="P0", type="number", value=100, min=1, step=1,
                      className="input-viva"),

            html.Label("Tiempo (días)", className="label-viva"),
            dcc.Slider(id="dias", min=10, max=200, step=5, value=80,
                       marks={10:"10", 100:"100", 200:"200"},
                       tooltip={"placement":"bottom","always_visible":True}),

            dcc.Markdown(id="texto-info", mathjax=True,
                         className="context-viva mt-3")
        ]),

        html.Div(className="col-50", children=[
            dcc.Graph(id="grafica", style={"height":"65vh"})
        ])
    ])
])

@callback(
    Output("grafica","figure"),
    Output("texto-info","children"),
    Output("control-card","style"),
    Input("modelo","value"),
    Input("r","value"),
    Input("K","value"),
    Input("P0","value"),
    Input("dias","value")
)
def update_page(modelo, r, K, P0, dias):
    if P0 is None or P0 <= 0: P0 = 1
    t = np.linspace(0, dias, dias*10 + 1)
    c = colores[modelo]

    if modelo == "exp":
        y = solve_exp(r, P0, t)
        tit = f"Exponencial  (r = {r:.3f})"
        eq = r"""
        **Ecuación exponencial**  
        $\displaystyle P(t)=P_0\,e^{rt}$  
        Sin límite: la población crece **sin freno**.
        """
    else:
        y = solve_log(r, K, P0, t)
        tit = f"Logístico  (r = {r:.3f},  K = {K:.0f})"
        eq = r"""
        **Ecuación logística**  
        $\displaystyle \frac{dP}{dt}=rP\left(1-\frac{P}{K}\right)$  
        *K* = capacidad de carga; cuando $P\to K$ el crecimiento se frena.
        """

    fig = go.Figure()
    fig.add_scatter(x=t, y=y, mode="lines", name="P(t)",
                    line=dict(color=c["line"], width=3.5))

    fig.update_layout(
        title=tit,
        xaxis_title="Tiempo (días)",
        yaxis_title="Población",
        template="simple_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=c["bg"],
        font=dict(family="Segoe UI", size=13, color="#2d3436"),
        margin=dict(l=60, r=30, t=60, b=60),
        legend=dict(x=0.02, y=0.98)
    )
    return fig, eq, {"background":c["bg"]}