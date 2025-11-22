import hej

@get('/')
def home():
    return html.html(
        html.head(
            html.title('Hej'),
            html.style(
                css.body({
                    'font-family': 'Arial, sans-serif',
                    'margin': '0',
                    'padding': '40px',
                    'text-align': 'center',
                    'background-color': '#1a1a1a',
                    'color': '#ffffff'
                }),
                css.h1({
                    'margin-bottom': '40px',
                    'color': '#ffffff'
                }),
                css.buttons({
                    'display': 'flex',
                    'gap': '20px',
                    'justify-content': 'center'
                }),
                css.button({
                    'padding': '10px 20px',
                    'font-size': '16px',
                    'cursor': 'pointer',
                    'background-color': '#333333',
                    'color': '#ffffff',
                    'border': '1px solid #555555',
                    'border-radius': '4px'
                }),
                css.button__hover({
                    'background-color': '#444444'
                })
            )
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
    urls = {
        'require_js': 'https://cdnjs.cloudflare.com/ajax/libs/require.js/2.3.6/require.min.js',
        'monaco_loader': 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.45.0/min/vs/loader.min.js',
        'monaco_base': 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.45.0/min/',
        'monaco_worker': 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.45.0/min/vs/base/worker/workerMain.js',
        'monaco_unpkg': 'https://unpkg.com/monaco-editor@0.45.0/min/vs'
    }

    return html.html(
        html.head(
            html.title('Hej - Documentation'),
            html.script(src=urls['require_js']),
            html.script(src=urls['monaco_loader']),
            html.script(f"""
                window.MonacoEnvironment = {{
                    getWorkerUrl: function(workerId, label) {{
                        return `data:text/javascript;charset=utf-8,${{encodeURIComponent(`
                            self.MonacoEnvironment = {{
                                baseUrl: '{urls['monaco_base']}'
                            }};
                            importScripts('{urls['monaco_worker']}');
                        `)}}`;
                    }}
                }};
            """),
            html.style(
                css.monaco_editor({
                    'margin': '10px 0',
                    'border': '1px solid #404040',
                    'border-radius': '4px'
                }),
                css.monaco_editor__margin({
                    'background-color': '#2d2d2d !important'
                })
            ),
            html.style(
                css.body({
                    'font-family': 'Arial, sans-serif',
                    'margin': '0',
                    'padding': '0',
                    'background-color': '#1a1a1a',
                    'color': '#ffffff',
                    'display': 'flex',
                    'min-height': '100vh'
                }),
                css.sidebar({
                    'width': '200px',
                    'background-color': '#2a2a2a',
                    'padding': '20px',
                    'border-right': '1px solid #444444',
                    'box-shadow': '2px 0 5px rgba(0,0,0,0.3)'
                }),
                css.sidebar__h2({
                    'color': '#cccccc',
                    'font-size': '18px',
                    'margin-bottom': '20px',
                    'font-weight': 'normal'
                }),
                css.sidebar__nav({
                    'display': 'flex',
                    'flex-direction': 'column',
                    'gap': '10px'
                }),
                css.sidebar__a({
                    'color': '#aaaaaa',
                    'text-decoration': 'none',
                    'padding': '8px 12px',
                    'border-radius': '4px',
                    'transition': 'background-color 0.2s',
                    'font-size': '14px'
                }),
                css.sidebar__a__hover({
                    'background-color': '#3a3a3a',
                    'color': '#ffffff'
                }),
                css.sidebar__a__active({
                    'background-color': '#444444',
                    'color': '#ffffff'
                }),
                css.main_content({
                    'flex': '1',
                    'padding': '40px',
                    'overflow-y': 'auto'
                }),
                css.h1({
                    'margin-bottom': '20px',
                    'color': '#ffffff'
                }),
                css.p({
                    'line-height': '1.6',
                    'margin-bottom': '15px'
                }),
                css.code_block({
                    'display': 'none'
                }),
                css.tab_content({
                    'display': 'none'
                }),
                css.tab_content__active({
                    'display': 'block'
                })
            )
        ),
        html.body(
            html.div(
                html.h2('Navigation'),
                html.nav(
                    html.a('Home', href='/'),
                    html.a('Quickstart', href='#', class_='active', **{'data-tab': 'quickstart'}),
                    html.a('Templates', href='#', **{'data-tab': 'templates'}),
                    html.a('CSS', href='#', **{'data-tab': 'css'}),
                    html.a('404 Handling', href='#', **{'data-tab': 'error-handling'})
                ),
                class_='sidebar'
            ),
            html.div(
                html.div(
                    html.h1('Quick Start - Hej Framework'),
                    html.p('Create a file called app.py and add this code:'),
                    html.textarea('''import hej

@get('/')
def home():
    return html.html(
        html.head(
            html.title('My App')
        ),
        html.body(
            html.h1('Hello, World!'),
            html.p('Welcome to Hej Framework')
        )
    )

if __name__ == '__main__':
    hej.run()''', class_='code-block'),
                    html.p('Visit http://127.0.0.1:5000 to see your app!'),
                    html.h2('Add More Routes'),
                    html.textarea('''@get('/about')
def about():
    return html.html(
        html.head(
            html.title('About')
        ),
        html.body(
            html.h1('About Page')
        )
    )''', class_='code-block'),
                    class_='tab-content active',
                    id='quickstart'
                ),
                html.div(
                    html.h1('Templates'),
                    html.p('Hej supports both programmatic HTML building and using external HTML template files:'),
                    html.h2('Using HTML Template Files'),
                    html.p('Create HTML files in a templates directory and serve them directly:'),
                    html.textarea('''# templates/index.html
<!DOCTYPE html>
<html>
<head>
    <title>My App</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            padding: 50px;
        }
        .buttons {
            display: flex;
            gap: 20px;
            justify-content: center;
            margin-top: 30px;
        }
        button {
            padding: 10px 20px;
            cursor: pointer;
            background-color: #333;
            color: white;
            border: none;
            border-radius: 4px;
        }
        button:hover {
            background-color: #555;
        }
    </style>
</head>
<body>
    <h1>Hello, World!</h1>
    <p>Welcome to Hej Framework</p>
    <div class="buttons">
        <button onclick="alert('Hello!')">Click me!</button>
    </div>
</body>
</html>''', class_='code-block', **{'data-language': 'html'}),
                    html.p('Then serve the HTML file in your route:'),
                    html.textarea('''import hej

@get('/')
def home():
    return 'index.html'

if __name__ == '__main__':
    hej.run()''', class_='code-block'),
                    html.p('You can also pass context variables to templates:'),
                    html.textarea('''@get('/greet')
def greet():
    return hej.template('example.html', {
        'title': 'Greetings',
        'heading': 'Hello, World!',
        'message': 'Welcome to Hej Framework with templates',
        'button_text': 'Hello from template!'
    })''', class_='code-block'),
                    html.p('Or simply return the template name as a string:'),
                    html.textarea('''@get('/simple')
def simple():
    return 'example.html' ''', class_='code-block'),
                    class_='tab-content',
                    id='templates'
                ),
                html.div(
                    html.h1('CSS in Hej'),
                    html.p('Hej provides a convenient way to add CSS styles to your HTML elements. You can use the css module to create styles programmatically:'),
                    html.h2('Basic CSS Styling'),
                    html.textarea('''import hej
from hej import css

@get('/')
def home():
    return html.html(
        html.head(
            html.title('My App'),
            html.style(
                css.body({
                    'font-family': 'Arial, sans-serif',
                    'margin': '0',
                    'padding': '40px',
                    'text-align': 'center',
                    'background-color': '#f0f0f0',
                    'color': '#333'
                }),
                css.h1({
                    'color': '#2c3e50',
                    'margin-bottom': '20px'
                }),
                css.button({
                    'padding': '10px 20px',
                    'background-color': '#3498db',
                    'color': 'white',
                    'border': 'none',
                    'border-radius': '4px',
                    'cursor': 'pointer'
                }),
                css.button__hover({
                    'background-color': '#2980b9'
                })
            )
        ),
        html.body(
            html.h1('Hello, World!'),
            html.button('Click me!', onclick="alert('Hello!')")
        )
    )''', class_='code-block'),
                    html.h2('CSS Classes and Selectors'),
                    html.p('You can target specific CSS selectors and classes:'),
                    html.textarea('''html.style(
    css('.my-class', {
        'color': 'red',
        'font-size': '18px'
    }),
    css('#my-id', {
        'background-color': 'blue'
    }),
    css('p:hover', {
        'text-decoration': 'underline'
    })
)''', class_='code-block'),
                    html.h2('Using External CSS Files'),
                    html.p('You can also link to external CSS files:'),
                    html.textarea('''html.head(
    html.title('My App'),
    html.link(rel='stylesheet', href='/static/style.css')
)''', class_='code-block'),
                    class_='tab-content',
                    id='css'
                ),
                html.div(
                    html.h1('404 Error Handling'),
                    html.p('Handle 404 errors with a custom page using the @not_found decorator:'),
                    html.textarea('''@not_found
def custom_404():
    return html.html(
        html.head(
            html.title('404 Not Found')
        ),
        html.body(
            html.h1('404 Not Found'),
            html.p('This page doesn\'t exist!'),
            html.a('Go Home', href='/')
        )
    )''', class_='code-block'),
                    html.p('The @not_found decorator registers a function to handle all 404 errors. When a route is not found, this function will be called instead of showing the default "Not Found" message.'),
                    class_='tab-content',
                    id='error-handling'
                ),
                class_='main-content'
            ),
            html.script("""
                require.config({ paths: { vs: '""" + urls['monaco_unpkg'] + """' } });
                require(['vs/editor/editor.main'], function() {
                    const codeBlocks = document.querySelectorAll('.code-block');
                    codeBlocks.forEach(function(block, index) {
                        const container = document.createElement('div');
                        container.id = 'editor-' + index;
                        container.style.height = '200px';
                        block.parentNode.insertBefore(container, block);

                        const language = block.getAttribute('data-language') || 'python';

                        monaco.editor.create(container, {
                            value: block.value,
                            language: language,
                            theme: 'vs-dark',
                            readOnly: true,
                            minimap: { enabled: false },
                            scrollBeyondLastLine: false,
                            automaticLayout: true,
                            fontSize: 14,
                            lineNumbers: 'on',
                            roundedSelection: false,
                            scrollbar: {
                                vertical: 'visible',
                                horizontal: 'visible'
                            }
                        });
                    });

                    const sidebarLinks = document.querySelectorAll('.sidebar a[data-tab]');
                    const tabContents = document.querySelectorAll('.tab-content');

                    sidebarLinks.forEach(link => {
                        link.addEventListener('click', function(e) {
                            e.preventDefault();

                            sidebarLinks.forEach(l => l.classList.remove('active'));
                            this.classList.add('active');

                            tabContents.forEach(content => content.classList.remove('active'));

                            const tabId = this.getAttribute('data-tab');
                            const selectedTab = document.getElementById(tabId);
                            if (selectedTab) {
                                selectedTab.classList.add('active');
                            }
                        });
                    });
                });
            """)
        )
    )

if __name__ == '__main__':
    debug_config = {'enabled': True, 'log_level': 'DEBUG', 'log_requests': True, 'log_responses': True, 'log_timing': True, 'show_stack_traces': True, 'log_static_files': False, 'log_templates': True, 'colorize_logs': True}

    hej.run(host='0.0.0.0', port=5000, debug=debug_config)