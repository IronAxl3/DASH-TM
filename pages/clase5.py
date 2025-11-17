import dash
from dash import dcc, html, Input, Output, State, callback
import plotly.graph_objects as go
import numpy as np

dash.register_page(__name__,
                   path="/clase5",
                   name="Clase 5: Campo Vectorial 2D",
                   title="Campo Vectorial – DASH-TM",
                   description="Dibuja cualquier campo vectorial 2D interactivamente.")

def safe_eval(expr, X, Y):
    try:
        d = {"X": X, "Y": Y, "np": np,
             "sin": np.sin, "cos": np.cos, "tan": np.tan,
             "exp": np.exp, "sqrt": np.sqrt,
             "pi": np.pi, "e": np.e}
        return eval(expr, d)
    except Exception:
        return np.full_like(X, np.nan)

layout = html.Div(className="page-container", children=[

    html.H2("Campo Vectorial 2D", className="titulo-viva center"),
    html.P("Escribe las ecuaciones y pulsa «Generar». Usa X e Y como variables.",
           className="subtitulo-viva center"),

    html.Div(className="fila-40-60 gap-2", children=[

        html.Div(className="col-40 card-viva", children=[
            html.H4("Controles", className="subt-viva"),

            html.Label("dx/dt =", className="label-viva"),
            dcc.Input(id="input-fx", type="text", value="np.sin(X)", className="input-viva"),

            html.Label("dy/dt =", className="label-viva"),
            dcc.Input(id="input-fy", type="text", value="np.cos(Y)", className="input-viva"),

            html.Label("Rango eje X", className="label-viva"),
            dcc.Input(id="input-xmax", type="number", value=5, min=1, className="input-viva"),

            html.Label("Rango eje Y", className="label-viva"),
            dcc.Input(id="input-ymax", type="number", value=5, min=1, className="input-viva"),

            html.Label("Puntos de malla", className="label-viva"),
            dcc.Input(id="input-n", type="number", value=15, min=5, max=30, className="input-viva"),

            html.Button("Generar campo", id="btn-generar", className="btn btn-primary btn-block"),

            html.Hr(className="hr-viva"),
            html.H5("Ejemplos rápidos", className="subt-viva"),
            html.Ul(className="lista-ejemplos", children=[
                html.Li(html.Button("X , Y", id="btn-xy", className="btn-ejemplo")),
                html.Li(html.Button("-Y , X", id="btn-rot", className="btn-ejemplo")),
                html.Li(html.Button("X+Y , np.cos(Y)", id="btn-mix", className="btn-ejemplo")),
            ]),
            html.Div(id="info-campo", className="context-viva mt-2")
        ]),

        # Gráfico
        html.Div(className="col-60", children=[
            dcc.Graph(id="grafica-campo", className="graph-viva", config={'displayModeBar': False})
        ])
    ])
])

@callback(
    Output("grafica-campo", "figure"),
    Output("info-campo", "children"),
    Input("btn-generar", "n_clicks"),
    Input("btn-xy", "n_clicks"),
    Input("btn-rot", "n_clicks"),
    Input("btn-mix", "n_clicks"),
    State("input-fx", "value"),
    State("input-fy", "value"),
    State("input-xmax", "value"),
    State("input-ymax", "value"),
    State("input-n", "value"),
    prevent_initial_call=True
)
def actualizar(_, __, ___, ____, fx_orig, fy_orig, xmax, ymax, n):
    try:
        ctx = dash.callback_context
        if not ctx.triggered:
            raise dash.exceptions.PreventUpdate
        boton = ctx.triggered[0]["prop_id"].split(".")[0]

        if boton == "btn-xy":
            fx_str, fy_str = "X", "Y"
        elif boton == "btn-rot":
            fx_str, fy_str = "-Y", "X"
        elif boton == "btn-mix":
            fx_str, fy_str = "X+Y", "np.cos(Y)"
        else:
            fx_str, fy_str = fx_orig, fy_orig

        x = np.linspace(-xmax, xmax, n)
        y = np.linspace(-ymax, ymax, n)
        X, Y = np.meshgrid(x, y)

        fx = safe_eval(fx_str, X, Y)
        fy = safe_eval(fy_str, X, Y)

        if np.isnan(fx).any() or np.isnan(fy).any():
            raise ValueError("Revisa la sintaxis de las funciones.")

        mag = np.hypot(fx, fy)
        mag_min, mag_max = mag.min(), mag.max()

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=[None], y=[None],
            mode="markers",
            marker=dict(colorscale="Viridis", cmin=mag_min, cmax=mag_max,
                        colorbar=dict(title="Magnitud"), showscale=True),
            showlegend=False
        ))

        for i in range(n):
            for j in range(n):
                x0, y0 = X[i, j], Y[i, j]
                u, v = fx[i, j], fy[i, j]
                if np.isnan(u) or np.isnan(v) or (u == 0 and v == 0):
                    continue
                # color indexado por magnitud
                color_int = int(255 * (mag[i, j] - mag_min) / (mag_max - mag_min + 1e-12))
                rgb = f"rgb({int(255 - color_int)}, {int(color_int)}, {int(255 - color_int * 0.5)})"

                fig.add_trace(go.Scatter(
                    x=[x0, x0 + u], y=[y0, y0 + v],
                    mode="lines+markers",
                    line=dict(width=2.5, color=rgb),
                    marker=dict(size=4, color=rgb),
                    hovertemplate=f"Punto: ({x0:.1f}, {y0:.1f})<br>Vector: ({u:.2f}, {v:.2f})<extra></extra>",
                    showlegend=False
                ))

        fig.update_layout(
            title=dict(text=f"dx/dt = {fx_str} | dy/dt = {fy_str}", x=0.5),
            xaxis_title="X", yaxis_title="Y",
            template="simple_white",
            margin=dict(l=40, r=40, t=60, b=40),
            xaxis=dict(scaleanchor="y", scaleratio=1, constrain="domain"),
            yaxis=dict(constrain="domain"),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)"
        )

        return fig, f"Magnitud vectorial: min = {mag_min:.2f}, max = {mag_max:.2f}"

    except Exception as e:
        fig = go.Figure().add_annotation(
            text=f"Error: {e}", showarrow=False, font_size=14
        )
        return fig, f"Error: {e}"