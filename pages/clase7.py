import dash
from dash import html, dcc, callback, Input, Output, State
import plotly.graph_objects as go
import requests
from datetime import datetime

dash.register_page(__name__, path="/clase7", name="Clase 7: Covid-19 Global")

def fmt(n):
    return f"{int(n or 0):,}"

def get_countries_list():

    try:
        r = requests.get("https://disease.sh/v3/covid-19/countries", timeout=10)
        r.raise_for_status()
        data = r.json()
        return sorted([c["country"] for c in data])
    except Exception as e:
        print("Error obteniendo países:", e)
        return ["Peru", "Mexico", "USA", "Canada"]

def get_country_current(country):
    try:
        url = f"https://disease.sh/v3/covid-19/countries/{country}"
        return requests.get(url, timeout=10).json()
    except Exception as e:
        print("Error obteniendo datos actuales:", e)
        return None

def get_country_hist(country, days):
    try:
        url = f"https://disease.sh/v3/covid-19/historical/{country}"
        params = {"lastdays": days}
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print("Error obteniendo histórico:", e)
        return None

layout = html.Div(className="page-container", children=[

    html.H2("Covid-19 por País", className="titulo-viva center"),

    html.Div(className="fila-40-60 gap-2", children=[

        html.Div(className="col-40 card-viva", children=[
            html.H4("Controles", className="subt-viva"),

            html.Label("País", className="label-viva"),
            dcc.Dropdown(id="dd-pais",
                         options=[{"label": c, "value": c} for c in get_countries_list()],
                         value="Peru",
                         className="input-viva",
                         style={"width": "100%"}),

            html.Label("Días históricos", className="label-viva"),
            dcc.Dropdown(id="dd-dias",
                         options=[{"label": str(d), "value": d} for d in [30, 60, 90, 120]] + [{"label": "Todo", "value": "all"}],
                         value=30,
                         className="input-viva",
                         style={"width": "100%"}),

            html.Button("Actualizar", id="btn-actualizar", className="btn btn-primary btn-block"),

            html.Div(id="info-msg", className="context-viva mt-3")
        ]),

        html.Div(className="col-60", children=[

            html.Div(className="fila-50-50", children=[
                html.Div(className="col-50", children=[
                    html.Div(className="card-viva", style={"textAlign": "center"}, children=[
                        html.H5("Total Casos", style={"color": "#1976d2"}),
                        html.H3(id="total-casos", children="—")
                    ])
                ]),
                html.Div(className="col-50", children=[
                    html.Div(className="card-viva", style={"textAlign": "center"}, children=[
                        html.H5("Casos Hoy", style={"color": "#f57c00"}),
                        html.H3(id="casos-hoy", children="—")
                    ])
                ])
            ]),

            html.Div(className="fila-50-50", children=[
                html.Div(className="col-50", children=[
                    html.Div(className="card-viva", style={"textAlign": "center"}, children=[
                        html.H5("Total Muertes", style={"color": "#d32f2f"}),
                        html.H3(id="total-muertes", children="—")
                    ])
                ]),
                html.Div(className="col-50", children=[
                    html.Div(className="card-viva", style={"textAlign": "center"}, children=[
                        html.H5("Recuperados", style={"color": "#388e3c"}),
                        html.H3(id="total-recuperados", children="—")
                    ])
                ])
            ]),

            dcc.Graph(id="grafica-covid", style={"height": "60vh"})
        ])
    ])
])

@callback(
    Output("total-casos", "children"),
    Output("casos-hoy", "children"),
    Output("total-muertes", "children"),
    Output("total-recuperados", "children"),
    Output("grafica-covid", "figure"),
    Output("info-msg", "children"),
    Input("btn-actualizar", "n_clicks"),
    State("dd-pais", "value"),
    State("dd-dias", "value"),
    prevent_initial_call=False
)
def actualizar(_, pais, dias):
    curr = get_country_current(pais)
    if not curr:
        fig = go.Figure().add_annotation(text="Error al obtener datos", showarrow=False, font=dict(color="red"))
        return ["Error"] * 4 + [fig, "No se pudieron cargar los datos."]

    total_c = fmt(curr.get("cases"))
    hoy_c   = fmt(curr.get("todayCases"))
    total_d = fmt(curr.get("deaths"))
    recup   = fmt(curr.get("recovered"))

    hist = get_country_hist(pais, dias)
    if not hist or "timeline" not in hist:
        fig = go.Figure().add_annotation(text="Sin histórico", showarrow=False)
        return [total_c, hoy_c, total_d, recup, fig, "Datos actuales cargados (sin histórico)."]

    timeline = hist["timeline"]
    cases   = timeline["cases"]
    deaths  = timeline["deaths"]
    fechas  = [datetime.strptime(f, "%m/%d/%y") for f in cases.keys()]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=fechas,
        y=list(cases.values()),
        mode="lines",
        name="Casos",
        line=dict(color="#FF7F50", width=3),
        fill="tozeroy",
        fillcolor="rgba(255, 127, 80, 0.08)",
        hovertemplate="<b>Casos</b><br>%{x|%d %b %Y}<br>%{y:,} personas<extra></extra>"
    ))

    fig.add_trace(go.Scatter(
        x=fechas,
        y=list(deaths.values()),
        mode="lines",
        name="Muertes",
        line=dict(color="#B22222", width=3),
        fill="tozeroy",
        fillcolor="rgba(178, 34, 34, 0.08)",
        hovertemplate="<b>Muertes</b><br>%{x|%d %b %Y}<br>%{y:,} personas<extra></extra>"
    ))

    fig.update_layout(
        title=dict(
            text=f"Evolución de Covid-19 en <b>{pais}</b>",
            x=0.5,
            xanchor="center",
            font=dict(size=20, color="#002b45", family="Segoe UI")
        ),
        xaxis_title="Fecha",
        yaxis_title="Número de personas",
        font=dict(family="Segoe UI", size=13, color="#212529"),
        template="plotly_white",
        plot_bgcolor="rgba(245, 247, 250, 0.6)",
        paper_bgcolor="white",
        margin=dict(l=60, r=30, t=80, b=60),
        legend=dict(
            x=0.02,
            y=0.98,
            bgcolor="rgba(255, 255, 255, 0.7)",
            bordercolor="#a2a9b1",
            borderwidth=1,
            font=dict(size=12)
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor="rgba(162, 169, 177, 0.2)",
            linewidth=1,
            linecolor="#a2a9b1",
            mirror=True
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(162, 169, 177, 0.2)",
            linewidth=1,
            linecolor="#a2a9b1",
            mirror=True,
            zeroline=False
        ),
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor="white",
            font_size=13,
            font_family="Segoe UI"
        )
    )

    return total_c, hoy_c, total_d, recup, fig, f"Datos actualizados para {pais}."