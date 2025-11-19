import dash
from dash import dcc, html
import plotly.graph_objects as go
import numpy as np

dash.register_page(__name__, name="Clase 2: E. Logística", path="/clase2")


r = 0.08                       
K = 100                        
t = np.linspace(0, 60, 400)    


P0_vals = [10, 30, 50, 120, 140]
colors  = ["var(--uv-bio)", "var(--uv-mate)", "var(--uv-graf)", "#b35a00", "#6f42c1"]

fig = go.Figure()
for p0, c in zip(P0_vals, colors):
    P = K * p0 / (p0 + (K - p0) * np.exp(-r * t))
    fig.add_trace(go.Scatter(
        x=t, y=P, mode='lines', name=f"P₀ = {p0}",
        line=dict(color=c, width=2.5),
        hovertemplate="t = %{x:.1f}<br>P = %{y:.1f}<extra></extra>"
    ))

Tgrid = np.linspace(2, 60, 15)       
Pgrid = np.linspace(5, 145, 12)      
T, P  = np.meshgrid(Tgrid, Pgrid)
dPdt  = r * P * (1 - P / K)          

for i in range(len(Tgrid)):
    for j in range(len(Pgrid)):
        dt = 2.0
        dp = dPdt[j,i] * 0.5
        
        fig.add_annotation(
            x=T[j,i] + dt/2,
            y=P[j,i] + dp/2,
            ax=T[j,i] - dt/2,
            ay=P[j,i] - dp/2,
            xref="x",
            yref="y",
            axref="x",
            ayref="y",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=1.5,
            arrowcolor='rgba(0, 82, 147, 0.7)'
        )

fig.add_hline(y=K, line_dash="dash", line_color="var(--uv-navbar)",
              annotation_text="Capacidad de carga K", annotation_position="right")

fig.update_layout(
    title={
        "text": "<b>Campo de vectores – Ecuación logística</b>",
        "x": 0.5,
        "font": {"size": 20, "color": "var(--uv-navbar)"}
    },
    xaxis_title="Tiempo (t)",
    yaxis_title="Población P(t)",
    template="simple_white",
    paper_bgcolor="var(--uv-blanco)",
    plot_bgcolor="var(--uv-blanco)",
    font={"family": "Segoe UI", "size": 13, "color": "var(--uv-texto)"},
    margin={"l": 60, "r": 30, "t": 60, "b": 60},
    legend={"x": 0.02, "y": 0.98}
)

layout = html.Div(className="page-container", children=[
    html.Div(className="fila-50-50", children=[
        html.Div(className="col-50 section-mate", children=[
            dcc.Markdown(r"""
La ecuación diferencial
$$
\frac{dP}{dt}=rP\left(1-\frac{P}{K}\right)
$$
modela el crecimiento de una población con recursos limitados.

**Puntos clave:**

- **Crecimiento inicial**: cuando $P\ll K$ la tasa es $\approx rP$ (crecimiento casi exponencial).  
- **Capacidad de carga** $K$: límite máximo sostenible.  
- **Equilibrio estable**: $P=K\Rightarrow\frac{dP}{dt}=0$; cualquier valor inicial tiende a $K$.  
- **Decrecimiento**: si $P>K$ los vectores apuntan hacia abajo, forzando el retorno a $K$.

El gráfico interactivo muestra varias soluciones (líneas de color) sobre el campo de vectores (segmentos grises).
""", mathjax=True)
        ]),
        html.Div(className="col-50", children=dcc.Graph(figure=fig, style={"height": "80vh"}))
    ])
])