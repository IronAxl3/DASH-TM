import dash
from dash import html, dcc
import os

app = dash.Dash(
    __name__,
    use_pages=True,
    assets_folder='assets',
    assets_url_path='assets'
)

app.layout = html.Div([
    html.H1("Técnicas de Modelamiento Matemático", className='app-header'),
    html.Div([
        html.Div([
            dcc.Link(f"{page['name']}", 
                   href=page["relative_path"], 
                   className='nav-link')
        ]) for page in dash.page_registry.values()
    ], className='nav-links'),
    dash.page_container
], className='app-container')

if __name__ == "__main__":
    app.run(debug=True, port=8080)
