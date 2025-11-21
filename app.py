import dash
from dash import html, dcc, Input, Output
import os

app = dash.Dash(
    __name__,
    use_pages=True,
    assets_folder='assets',
    assets_url_path='assets'
)

def get_page_order_key(page):
    """Extract numeric order from page name or path"""
    name_lower = page['name'].lower()
    path_lower = page['relative_path'].lower()
    
    
    if 'inicio' in name_lower or path_lower == '/':
        return 0
    elif 'clase 1' in name_lower or 'clase1' in path_lower:
        return 1
    elif 'clase 2' in name_lower or 'clase2' in path_lower:
        return 2
    elif 'clase 3' in name_lower or 'clase3' in path_lower:
        return 3
    elif 'clase 4' in name_lower or 'clase4' in path_lower:
        return 4
    elif 'clase 5' in name_lower or 'clase5' in path_lower:
        return 5
    elif 'clase 6' in name_lower or 'clase6' in path_lower:
        return 6
    elif 'clase 7' in name_lower or 'clase7' in path_lower:
        return 7
    elif 'clase 8' in name_lower or 'clase8' in path_lower:
        return 8
    else:
        return 999


all_pages = list(dash.page_registry.values())
sorted_pages = sorted(all_pages, key=get_page_order_key)

app.layout = html.Div([
   
    html.Header(className='app-header-nav', children=[
        html.Div(className='header-container', children=[
            html.H1("DASH-TM", className='app-title'),
            html.P("Técnicas de Modelamiento Matemático", className='app-subtitle'),
            
            
            html.Button(
                html.Span(className='hamburger-icon'),
                id='menu-toggle',
                className='menu-toggle-btn',
                n_clicks=0
            ),
            
           
            html.Nav(
                id='nav-menu',
                className='nav-menu closed',
                children=[
                    html.Div(className='nav-menu-header', children=[
                        html.H3("Navegación"),
                        html.Button('✕', id='menu-close', className='menu-close-btn')
                    ]),
                    html.Div(className='nav-links-container', children=[
                        dcc.Link(
                            html.Div(className='nav-item', children=[
                                html.Span(page['name'], className='nav-link-text'),
                                html.Span('→', className='nav-arrow')
                            ]),
                            href=page["relative_path"],
                            className='nav-link-item'
                        ) for page in sorted_pages
                    ])
                ]
            ),
        ])
    ]),
    
    
    html.Div(id='page-content', children=[
        dash.page_container
    ], className='page-wrapper'),
    
], className='app-container')


app.clientside_callback(
    """
    function(n_clicks, n_close) {
        const menu = document.getElementById('nav-menu');
        if(!menu) return 'closed';
        
        // Determine if we should open or close
        if(n_close > 0 || (n_clicks > 0 && menu.classList.contains('open'))) {
            menu.classList.remove('open');
            menu.classList.add('closed');
            return 'closed';
        } else if(n_clicks > 0) {
            menu.classList.remove('closed');
            menu.classList.add('open');
            return 'open';
        }
        return 'closed';
    }
    """,
    Output('nav-menu', 'className'),
    Input('menu-toggle', 'n_clicks'),
    Input('menu-close', 'n_clicks'),
    prevent_initial_call=True
)

if __name__ == "__main__":
    app.run(debug=True, port=8080)
