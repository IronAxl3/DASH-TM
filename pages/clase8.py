import dash
from dash import html, dcc, callback, Input, Output, State
import plotly.graph_objects as go
import requests
import numpy as np
from datetime import datetime
import random

dash.register_page(__name__, path="/clase8", name="Clase 8: Datos que Sudan")

MESSAGES = [
    "Datos que entrenan. Músculos que responden.",
    "Cada gramo es una función de voluntad.",
    "El acero no miente. Los números tampoco.",
    "Entrena duro. Modela preciso.",
    "La gloria es matemática."
]

WGER_URL = "https://wger.de/api/v2"

def get_muscles():
    
    try:
        r = requests.get(f"{WGER_URL}/muscle/?limit=30", timeout=5)
        r.raise_for_status()
        return [{"id": m["id"], "name": m["name_en"]} for m in r.json()["results"]]
    except Exception as e:
        print("API reposo – respaldo local:", e)
        return [
            {"id": 1, "name": "Chest"}, {"id": 2, "name": "Back"},
            {"id": 3, "name": "Legs"}, {"id": 4, "name": "Shoulders"},
            {"id": 5, "name": "Arms"}, {"id": 6, "name": "Core"}
        ]

def get_exercises_with_gif(muscle_id):
    
    local_gifs = {
        "chest": [
            {"name": "Press", "gif": "/assets/gif/press.gif", "target": "Pecho"},
            {"name": "Press Militar", "gif": "/assets/gif/press-militar.gif", "target": "Pecho"}
        ],
        "back": [
            {"name": "Dominada", "gif": "/assets/gif/dominada.gif", "target": "Espalda"},
            {"name": "Fondo", "gif": "/assets/gif/fondo.gif", "target": "Espalda"}
        ],
        "legs": [
            {"name": "Sentadilla", "gif": "/assets/gif/sentadilla.gif", "target": "Piernas"},
            {"name": "Fondo", "gif": "/assets/gif/fondo.gif", "target": "Piernas"}
        ],
        "shoulders": [
            {"name": "Press Militar", "gif": "/assets/gif/press-militar.gif", "target": "Hombros"},
            {"name": "Fondo", "gif": "/assets/gif/fondo.gif", "target": "Hombros"}
        ],
        "arms": [
            {"name": "Curl de Bíceps", "gif": "/assets/gif/curl-de-biceps.gif", "target": "Brazos"},
            {"name": "Fondo", "gif": "/assets/gif/fondo.gif", "target": "Brazos"}
        ],
        "core": [
            {"name": "Fondo", "gif": "/assets/gif/fondo.gif", "target": "Core"},
            {"name": "Dominada", "gif": "/assets/gif/dominada.gif", "target": "Core"}
        ]
    }
    return local_gifs.get(muscle_id.lower(), local_gifs["chest"])

def get_gym_images(query="gym workout", per_page=6):
    try:
        return [f"https://source.unsplash.com/400x300/?{query},{i}" for i in range(per_page)]
    except:
        return [f"https://via.placeholder.com/400x300?text=Ejercicio+{i}" for i in range(per_page)]

def get_sound_url():
    return "https://www.fesliyanstudios.com/play-mp3/6701"

def calculate_1RM(peso, repeticiones):
    return peso * (1 + repeticiones/30)

def muscle_activation(peso, reps, series, tempo, descanso, nivel):
    one_rm = calculate_1RM(peso, reps)
    porcentaje_1rm = (peso / one_rm) * 100
    volumen = reps * series
    factor_tempo = 1 + (tempo - 2) * 0.1 
    factor_descanso = 1 + (90 - descanso) * 0.002  
    factor_nivel = {"principiante": 0.85, "intermedio": 1.0, "avanzado": 1.15}[nivel]
    activacion = min(100, (porcentaje_1rm * 0.5 + volumen * 0.25 + factor_tempo * 10 + factor_descanso * 5) * factor_nivel)
    return activacion, porcentaje_1rm, volumen

layout = html.Div(className="page-container gym-dark", children=[

    html.Div(className="gym-hero-premium", children=[
        html.H1("⚡ LA DONCELLA DE HIERRO", className="gym-title-main"),
        html.Blockquote(random.choice(MESSAGES), className="gym-poem-premium"),
        html.Span("🔥 Transforma datos en poder", className="gym-subtitle-premium")
    ]),

    html.Div(className="gym-input-section", children=[
        html.Div(className="gym-card-input", children=[
            html.H4("💪 PERFIL PERSONAL", className="gym-card-title"),
            html.Div(className="gym-input-group", children=[
                html.Label("Peso corporal (kg)", className="gym-input-label"),
                dcc.Input(id="input-peso", type="number", value=70, min=30, max=200, className="gym-input-field")
            ]),
            html.Div(className="gym-input-group", children=[
                html.Label("Edad (años)", className="gym-input-label"),
                dcc.Input(id="input-edad", type="number", value=25, min=10, max=100, className="gym-input-field")
            ]),
            html.Div(className="gym-input-group", children=[
                html.Label("Nivel de entrenamiento", className="gym-input-label"),
                dcc.Dropdown(id="dd-nivel", options=[
                    {"label": "🤸 Principiante", "value": "principiante"},
                    {"label": "🤸 Intermedio", "value": "intermedio"},
                    {"label": "🤸 Avanzado", "value": "avanzado"}
                ], value="intermedio", className="gym-input-field")
            ])
        ]),

        html.Div(className="gym-card-input", children=[
            html.H4("🏋️ EJERCICIO + PARÁMETROS", className="gym-card-title"),
            html.Div(className="gym-input-group", children=[
                html.Label("Grupo muscular", className="gym-input-label"),
                dcc.Dropdown(
                    id="dd-muscle",
                    options=[{"label": m["name"], "value": m["name"].lower()} for m in get_muscles()],
                    value="chest",
                    className="gym-input-field"
                )
            ]),
            html.Div(className="gym-slider-group", children=[
                html.Label("⚖️ PESO (kg)", className="gym-slider-label"),
                dcc.Slider(id="slider-peso", min=20, max=200, step=2.5, value=60,
                           marks={20: "20", 60: "60", 100: "100", 150: "150", 200: "200"}, className="gym-slider")
            ]),
            html.Div(className="gym-slider-group", children=[
                html.Label("🔄 REPETICIONES", className="gym-slider-label"),
                dcc.Slider(id="slider-reps", min=1, max=20, step=1, value=8,
                           marks={1: "1", 5: "5", 10: "10", 15: "15", 20: "20"}, className="gym-slider")
            ]),
            html.Div(className="gym-slider-group", children=[
                html.Label("📈 SERIES", className="gym-slider-label"),
                dcc.Slider(id="slider-series", min=1, max=10, step=1, value=3,
                           marks={1: "1", 5: "5", 10: "10"}, className="gym-slider")
            ]),
            html.Div(className="gym-slider-group", children=[
                html.Label("⏱️ TIEMPO (segundos)", className="gym-slider-label"),
                dcc.Slider(id="slider-tempo", min=1, max=6, step=0.5, value=2,
                           marks={1: "1s", 2: "2s", 3: "3s", 4: "4s", 5: "5s", 6: "6s"}, className="gym-slider")
            ]),
            html.Div(className="gym-slider-group", children=[
                html.Label("😤 DESCANSO (segundos)", className="gym-slider-label"),
                dcc.Slider(id="slider-descanso", min=30, max=300, step=15, value=90,
                           marks={30: "30s", 90: "90s", 180: "3m", 300: "5m"}, className="gym-slider")
            ])
        ])
    ]),

    html.Div(className="gym-button-container mt-4", children=[
        html.Button("⚡ CALCULAR ENTRENAMIENTO", id="btn-calcular", className="gym-btn-main")
    ]),

    html.Div(className="gym-charts-section mt-4", children=[
        html.Div(className="gym-chart-card", children=[
            html.H4("🔥 ACTIVACIÓN MUSCULAR", className="gym-chart-title"),
            dcc.Graph(id="grafica-activacion", style={"height": "45vh"})
        ]),
        html.Div(className="gym-chart-card", children=[
            html.H4("📊 RADAR DE CAPACIDADES", className="gym-chart-title"),
            dcc.Graph(id="grafica-radar", style={"height": "45vh"})
        ])
    ]),

    html.Div(id="info-detallada", className="gym-analysis-section mt-4", children=[
        html.H4("📈 ANÁLISIS DETALLADO", className="gym-section-title"),
        html.Div(className="gym-analysis", children=[])
    ]),

    html.Div(className="gym-exercises-section mt-4", children=[
        html.H4("💪 EJERCICIOS RECOMENDADOS", className="gym-section-title"),
        html.Div(id="ejercicios-galeria", className="gym-exercises-gallery")
    ]),

    html.Div(className="gym-audio-section mt-4", children=[
        html.H4("🔊 MOTIVACIÓN SONORA", className="gym-section-title"),
        html.Audio(id="gym-sound", controls=True, className="gym-audio-player"),
        html.P("Entrena fuerte, corre más rápido, sube más alto", className="gym-audio-text"),
        html.Span("🎵 "+random.choice(MESSAGES), className="gym-audio-quote")
    ]),

    html.Footer(className="gym-footer-premium", children=[
        html.P("El dolor es momentáneo. La gloria es eterna. – @Iron_Axl", className="gym-footer-text"),
        html.A("🔗 GitHub", href="https://github.com/IronAxl3", target="_blank", className="gym-footer-link")
    ])
])

@callback(
    Output("grafica-activacion", "figure"),
    Output("grafica-radar", "figure"),
    Output("ejercicios-galeria", "children"),
    Output("info-detallada", "children"),
    Input("btn-calcular", "n_clicks"),
    State("input-peso", "value"),
    State("input-edad", "value"),
    State("dd-nivel", "value"),
    State("slider-peso", "value"),
    State("slider-reps", "value"),
    State("slider-series", "value"),
    State("slider-tempo", "value"),
    State("slider-descanso", "value"),
    prevent_initial_call=False
)
def calcular_entrenamiento(_, peso_corporal, edad, nivel, peso_levantado, reps, series, tempo, descanso):
    if any(v is None for v in [peso_corporal, edad, peso_levantado, reps, series, tempo, descanso]):
        fig1 = go.Figure().add_annotation(text="Completa todos los campos", showarrow=False)
        return fig1, go.Figure(), [], "Por favor completa todos los campos."

    one_rm = calculate_1RM(peso_levantado, reps)
    activacion, porcentaje_1rm, volumen = muscle_activation(peso_levantado, reps, series, tempo, descanso, nivel)
    
    fig1 = go.Figure()
    fig1.add_trace(go.Indicator(
        mode="gauge+number+delta",
        value=activacion,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Activación muscular (%)"},
        delta={'reference': 70, 'increasing': {'color': "green"}},
        gauge={'axis': {'range': [None, 100]},
               'bar': {'color': "darkblue"},
               'steps': [
                   {'range': [0, 50], 'color': "lightgray"},
                   {'range': [50, 80], 'color': "yellow"},
                   {'range': [80, 100], 'color': "green"}],
               'threshold': {'line': {'color': "red", 'width': 4},
                             'thickness': 0.75,
                             'value': 90}}))
    fig1.update_layout(height=350)

    categorias = ["Fuerza", "Resistencia", "Técnica", "Cardio", "Core"]
    valores = [
        min(100, porcentaje_1rm * 1.2),
        min(100, volumen * 0.8),
        min(100, 100 - abs(tempo - 2) * 10),
        min(100, (300 - descanso) * 0.4),
        min(100, activacion * 0.9)
    ]
    fig2 = go.Figure(data=go.Scatterpolar(
        r=valores,
        theta=categorias,
        fill='toself',
        fillcolor='rgba(255,127,80,0.3)',
        line_color='#ff7f50',
        name='Tu sesión'
    ))
    fig2.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        title="Radar de capacidades",
        height=350
    )

    ejercicios = get_exercises_with_gif("chest")
    cards = [
        html.Div(className="gym-card", children=[
            html.Img(src=ex["gif"], className="gym-gif", title=ex["name"]),
            html.H5(ex["name"]),
            html.P(ex["target"], className="gym-target")
        ]) for ex in ejercicios
    ]

    zona = "Hipertrofia" if activacion > 70 else "Fuerza-resistencia" if activacion > 50 else "Recuperación activa"
    recomendacion = (
        "¡Perfecto! Estás en zona óptima para hipertrofia. Mantén esta intensidad."
        if activacion > 70 else
        "Aumenta 5 kg o reduce descanso a 60 s para entrar en hipertrofia."
    )
    
    color_activacion = "#4CAF50" if activacion > 70 else "#FF9800" if activacion > 50 else "#F44336"
    
    info = html.Div(className="gym-analysis", children=[
        html.Div(className="gym-metric", children=[
            html.Span("🔥 1RM ESTIMADO", className="gym-label"),
            html.Span(f"{one_rm:.1f}", className="gym-value"),
            html.Span("kg", className="gym-unit")
        ]),
        html.Div(className="gym-metric", children=[
            html.Span("⚡ % DE 1RM", className="gym-label"),
            html.Span(f"{porcentaje_1rm:.1f}", className="gym-value"),
            html.Span("%", className="gym-unit")
        ]),
        html.Div(className="gym-metric", children=[
            html.Span("📊 VOLUMEN", className="gym-label"),
            html.Span(f"{volumen}", className="gym-value"),
            html.Span("reps", className="gym-unit")
        ]),
        html.Div(className="gym-metric", children=[
            html.Span("💪 ACTIVACIÓN", className="gym-label"),
            html.Span(f"{activacion:.1f}", className="gym-value", style={"color": color_activacion}),
            html.Span("%", className="gym-unit")
        ]),
        html.Div(className="gym-metric", children=[
            html.Span("🎯 ZONA", className="gym-label"),
            html.Span(zona, className="gym-value"),
        ]),
        html.Div(className="gym-recommendation", children=[
            html.Span("💡 RECOMENDACIÓN", className="gym-label-rec"),
            html.Span(recomendacion, className="gym-text-rec")
        ])
    ])
    return fig1, fig2, cards, info

@callback(
    Output("gym-sound", "src"),
    Input("gym-sound", "id")
)
def load_sound(_):
    return get_sound_url()