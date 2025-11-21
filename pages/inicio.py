import dash
from dash import html, dcc

dash.register_page(__name__, path="/", name="inicio")

layout = html.Div([

    html.Section(className='inicio-hero-section', children=[
        html.Div(className='inicio-hero-container', children=[
            html.Div(className='inicio-hero-content', children=[
                
                html.Div(className='lava-lamp-container', children=[
                    html.Div(className='lava-blobs', children=[
                        html.Div(className='blob blob-1'),
                        html.Div(className='blob blob-2'),
                        html.Div(className='blob blob-3'),
                    ]),
                    html.Img(
                        src='/assets/imagenes/yo.webp', 
                        alt='Hiron Axl Ortega Yucra',
                        className='lava-profile-image'    
                    ),
                ]),
                html.Div(className='inicio-hero-text', children=[
                    html.H1("Hiron Axl Ortega Yucra", className='inicio-hero-title'),
                    html.P("Estudiante de Computación Científica – UNMSM", className='inicio-hero-subtitle'),
                    html.Div(className='inicio-divider'),
                    dcc.Markdown("""
                    Apasionado por el **desarrollo web**, el **análisis de datos** y la aplicación de 
                    **Modelamiento Matemáticos** para crear soluciones con impacto real.
                    """, className='inicio-hero-desc', mathjax=True),
                    html.Div(className='inicio-hero-skills', children=[
                        html.Span("Python", className='skill-tag'),
                        html.Span("Modelamiento Matemático", className='skill-tag'),
                        html.Span("Desarrollo Web", className='skill-tag'),
                        html.Span("Análisis de Datos", className='skill-tag'),
                    ]),
                ])
            ])
        ])
    ]),

    html.Section(className='inicio-about-section', children=[
        html.Div(className='inicio-container', children=[
            html.H2("Mi Trayectoria", className='inicio-section-title'),
            html.Div(className='inicio-trayectoria-grid', children=[
                html.Div(className='inicio-card academic', children=[
                    html.H3("🎓 Formación Académica", className='card-title'),
                    dcc.Markdown("""
                    Comprometido con la excelencia académica desde el inicio. Mi formación en 
                    **Computación Científica** me ha permitido desarrollar una sólida base en 
                    programación, análisis numérico y modelamiento matemático.
                    
                    Busco constantemente combinar rigor teórico con aplicaciones prácticas que 
                    resuelvan problemas reales y complejos.
                    """, className='card-text', mathjax=True),
                ]),
                html.Div(className='judo-medal-card', children=[
                    html.Img(
                        src='/assets/imagenes/judomedalla.webp',
                        alt='Campeón Judo - Comité Olímpico Peruano',
                        className='judo-medal-showcase'
                    )
                ]),
                html.Div(className='inicio-card deportivo', children=[
                    html.H3("🥋 Trayectoria Deportiva", className='card-title'),
                    dcc.Markdown("""
                    **Judoka** de la Sección de Judo de la UNMSM y ex-competidor de 
                    **Lucha Olímpica** en la Selección Universitaria.
                    
                    **Campeón en Judo** por el Comité Olímpico Peruano – un logro que reforzó 
                    mi mentalidad de disciplina, resiliencia y enfoque competitivo.
                    
                    Estos valores deportivos los aplico en cada proyecto académico y profesional.
                    """, className='card-text', mathjax=True),
                ]),
            ])
        ])
    ]),

    html.Section(className='inicio-skills-section', children=[
        html.Div(className='inicio-container', children=[
            html.H2("Habilidades Principales", className='inicio-section-title'),
            html.Div(className='inicio-skills-grid', children=[
                html.Div(className='skill-card', children=[
                    html.Span("🐍", className='skill-icon'),
                    html.H4("Python", className='skill-name'),
                    html.P("Desarrollo, análisis de datos y automatización", className='skill-desc')
                ]),
                html.Div(className='skill-card', children=[
                    html.Span("∑", className='skill-icon'),
                    html.H4("Modelamiento Matemático", className='skill-name'),
                    html.P("Ecuaciones diferenciales, análisis numérico", className='skill-desc')
                ]),
                html.Div(className='skill-card', children=[
                    html.Span("🌐", className='skill-icon'),
                    html.H4("Desarrollo Web", className='skill-name'),
                    html.P("Dash, Python, diseño responsive", className='skill-desc')
                ]),
                html.Div(className='skill-card', children=[
                    html.Span("📊", className='skill-icon'),
                    html.H4("Análisis de Datos", className='skill-name'),
                    html.P("Visualización, estadística aplicada", className='skill-desc')
                ]),
            ])
        ])
    ]),

    html.Section(className='inicio-objetivo-section', children=[
        html.Div(className='inicio-container', children=[
            html.Div(className='inicio-objetivo-card', children=[
                html.H2("Mi Objetivo", className='objetivo-title'),
                dcc.Markdown("""
                Integrar mis **conocimientos en computación** y **modelamiento matemático** con mi 
                **mentalidad competitiva** para crear **soluciones eficientes e innovadoras** 
                que tengan un **impacto positivo en la sociedad**.
                
                Creo que la excelencia académica, la disciplina deportiva y la pasión por la tecnología 
                convergen en la capacidad de transformar problemas complejos en herramientas útiles 
                y con propósito.
                """, className='objetivo-text', mathjax=True),
            ])
        ])
    ]),

    html.Section(className='inicio-cta-section', children=[
        html.Div(className='inicio-container', children=[
            html.H3("Explora mis Proyectos", className='cta-title'),
            html.P("Modelos matemáticos interactivos y análisis de datos", className='cta-subtitle'),
            html.Div(className='inicio-projects-grid', children=[
                dcc.Link(['📈 Crecimiento\nPoblacional'], href='/clase1', className='proyecto-btn'),
                dcc.Link(['🌱 Modelo\nLogístico'], href='/clase2', className='proyecto-btn'),
                dcc.Link(['🔧 Sistemas\nInteractivos'], href='/clase3', className='proyecto-btn'),
                dcc.Link(['🦠 Modelo\nSIR'], href='/clase4', className='proyecto-btn'),
                dcc.Link(['🧭 Campo\nVectorial'], href='/clase5', className='proyecto-btn'),
                dcc.Link(['📊 Modelo\nSEIR'], href='/clase6', className='proyecto-btn'),
                dcc.Link(['📉 Gráficos\nAvanzados'], href='/clase7', className='proyecto-btn'),
                dcc.Link(['💪 Datos que\nSudan'], href='/clase8', className='proyecto-btn destacado'),
            ]),
        ])
    ]),

])