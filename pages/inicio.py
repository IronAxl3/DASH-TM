import dash
from dash import html, dcc

dash.register_page(__name__, path="/", name="inicio")

layout = html.Div([


    html.Section(className='hero', children=[
        html.Div(className='hero-card', children=[
            html.Img(
                src='/assets/imagenes/yo.webp', 
                alt='Hiron Axl Ortega Yucra',
                className='hero-img'    
            ),
            html.Div(className='hero-text', children=[
                html.H1("Hiron Axl Ortega Yucra", className='hero-title'),
                html.P("Estudiante de Computación Científica – UNMSM", className='hero-subtitle'),
                html.Hr(className='hero-divider'),
                dcc.Markdown("""
                Apasionado por el **desarrollo web**, el **análisis de datos** y la
                aplicación de **Modelamiento Matemáticos** para resolver problemas del mundo real.
                """, className='hero-desc', mathjax=True),
                html.Div(className='hero-tags', children=[
                    html.Span("Python", className='tag bio'),
                    html.Span("Técnicas de Modelamiento Matemático", className='tag mate'),

                ]),
            ], style={'paddingLeft': '2rem'})
        ])
    ]),

    html.Section(className='bio-box section-bio', children=[
        html.H2("Un poco más sobre mí"),
        dcc.Markdown("""
        Desde pequeño me ha interesado la tecnología y cómo esta puede ser utilizada
        para resolver problemas complejos.  
        Además de mi pasión por la programación, soy **Judoka** desde hace varios años;
        este deporte me ha enseñado *disciplina, perseverancia y trabajo en equipo*.

        Mi objetivo es combinar mis conocimientos en computación con mi pasión por la
        resolución de problemas para crear **soluciones innovadoras** que tengan un
        **impacto positivo en la sociedad**.
        """, mathjax=True),
    ]),

   html.Section(className='cta-box', children=[
    html.H3("¡Exploremos modelos matemáticos juntos!"),

    html.Div(className='btn-grid', children=[
        # Fila 1
        dcc.Link(["📈 ", html.Br(), "Crecimiento Poblacional"], href='/clase1', className='btn btn-primary'),
        dcc.Link(["🌱 ", html.Br(), "Modelo Logístico"], href='/clase2', className='btn btn-secondary'),
        dcc.Link(["🔧 ", html.Br(), "Logístico Interactivo"], href='/clase3', className='btn btn-secondary'),

        # Fila 2
        dcc.Link(["🦠 ", html.Br(), "Modelo SIR"], href='/clase4', className='btn btn-accent'),
        dcc.Link(["🧭 ", html.Br(), "Campo Vectorial"], href='/clase5', className='btn btn-accent'),
        dcc.Link(["📊 ", html.Br(), "Modelo SEIR"], href='/clase6', className='btn btn-accent'),
    ]),

    html.P("Haz clic en cualquier tema para comenzar.", className='cta-hint')
])
])