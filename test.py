import hej

@get('/')
def home():
    return html.html(
        html.head(
            html.title('Hej'),
            html.style(
                css.body({
                    'font-family': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
                    'margin': '0',
                    'padding': '0',
                    'min-height': '100vh',
                    'display': 'flex',
                    'flex-direction': 'column',
                    'align-items': 'center',
                    'justify-content': 'center',
                    'background-color': '#1a1a1a',
                    'color': '#ffffff'
                }),
                css.h1({
                    'margin': '0 0 40px 0',
                    'font-size': '3.5rem',
                    'font-weight': '200',
                    'color': '#ffffff',
                    'letter-spacing': '-0.03em'
                }),
                css.buttons({
                    'display': 'flex',
                    'gap': '20px',
                    'justify-content': 'center',
                    'flex-wrap': 'wrap'
                }),
                css.button({
                    'padding': '14px 28px',
                    'font-size': '16px',
                    'font-weight': '500',
                    'cursor': 'pointer',
                    'background-color': '#333333',
                    'color': '#ffffff',
                    'border': '1px solid #555555',
                    'border-radius': '6px',
                    'transition': 'all 0.2s ease',
                    'text-transform': 'uppercase',
                    'letter-spacing': '0.5px'
                }),
                css.button__hover({
                    'background-color': '#444444',
                    'border-color': '#666666'
                }),
            )
        ),
        html.body(
            html.div(
                html.h1('Hej Framework'),
                html.div(
                    html.button('Download Hej', onclick="window.location.href='https://pypi.org/project/hej/'"),
                    html.button('View API Docs', onclick="window.location.href='/docs'"),
                    class_='buttons'
                ),
                style='text-align: center;'
            ),
            html.div('Version: 0.3.0', style='position: fixed; bottom: 20px; left: 20px; background-color: #333333; color: white; padding: 8px 16px; border-radius: 6px; font-size: 14px; font-weight: bold; z-index: 1000;'),
            html.div('Powered by Hej', style='position: fixed; bottom: 20px; right: 20px; background-color: #5dade2; color: white; padding: 8px 16px; border-radius: 6px; font-size: 14px; font-weight: bold; z-index: 1000;')
        )
    )

@not_found
def custom_404():
    return html.html(
        html.head(
            html.title('404 Not Found')
        ),
        html.body(
            html.h1('404 Not Found'),
            html.p('This page doesn\'t exist!')
        )
    )

@get('/docs')
def docs():
    return 'docs.html'

if __name__ == '__main__':
    debug_config = {'enabled': True, 'log_level': 'DEBUG', 'log_requests': True, 'log_responses': True, 'log_timing': True, 'show_stack_traces': True, 'log_static_files': False, 'log_templates': True, 'colorize_logs': True}

    hej.run(host='0.0.0.0', port=5000, debug=debug_config)