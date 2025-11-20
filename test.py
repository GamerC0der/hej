import hej

@get('/')
def home():
    return html.html(
        html.head(
            html.title('Hej'),
            html.style("""
                body {
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 40px;
                    text-align: center;
                    background-color: #1a1a1a;
                    color: #ffffff;
                }
                h1 {
                    margin-bottom: 40px;
                    color: #ffffff;
                }
                .buttons {
                    display: flex;
                    gap: 20px;
                    justify-content: center;
                }
                button {
                    padding: 10px 20px;
                    font-size: 16px;
                    cursor: pointer;
                    background-color: #333333;
                    color: #ffffff;
                    border: 1px solid #555555;
                    border-radius: 4px;
                }
                button:hover {
                    background-color: #444444;
                }
            """)
        ),
        html.body(
            html.h1('Hej, World!'),
            html.div(
                html.button('Download Hej', onclick="window.location.href='https://pypi.org/project/hej/'"),
                html.button('View API Docs', onclick="window.location.href='/docs'"),
                class_='buttons'
            )
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
    debug_config = {
        'enabled': True,
        'log_level': 'DEBUG',
        'log_requests': True,
        'log_responses': True,
        'log_timing': True,
        'show_stack_traces': True,
        'log_static_files': False,
        'log_templates': True,
        'colorize_logs': True
    }

    hej.run(debug=debug_config)