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
    return html.html(
        html.head(
            html.title('Hej - Documentation'),
            html.script(src='https://cdnjs.cloudflare.com/ajax/libs/require.js/2.3.6/require.min.js'),
            html.script(src='https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.45.0/min/vs/loader.min.js'),
            html.script("""
                window.MonacoEnvironment = {
                    getWorkerUrl: function(workerId, label) {
                        return `data:text/javascript;charset=utf-8,${encodeURIComponent(`
                            self.MonacoEnvironment = {
                                baseUrl: 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.45.0/min/'
                            };
                            importScripts('https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.45.0/min/vs/base/worker/workerMain.js');
                        `)}`;
                    }
                };
            """),
            html.style("""
                .monaco-editor {
                    margin: 10px 0;
                    border: 1px solid #404040;
                    border-radius: 4px;
                }
                .monaco-editor .margin {
                    background-color: #2d2d2d !important;
                }
            """),
            html.style("""
                body {
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    background-color: #1a1a1a;
                    color: #ffffff;
                    display: flex;
                    min-height: 100vh;
                }
                .sidebar {
                    width: 200px;
                    background-color: #2a2a2a;
                    padding: 20px;
                    border-right: 1px solid #444444;
                    box-shadow: 2px 0 5px rgba(0,0,0,0.3);
                }
                .sidebar h2 {
                    color: #cccccc;
                    font-size: 18px;
                    margin-bottom: 20px;
                    font-weight: normal;
                }
                .sidebar nav {
                    display: flex;
                    flex-direction: column;
                    gap: 10px;
                }
                .sidebar a {
                    color: #aaaaaa;
                    text-decoration: none;
                    padding: 8px 12px;
                    border-radius: 4px;
                    transition: background-color 0.2s;
                    font-size: 14px;
                }
                .sidebar a:hover {
                    background-color: #3a3a3a;
                    color: #ffffff;
                }
                .sidebar a.active {
                    background-color: #444444;
                    color: #ffffff;
                }
                .main-content {
                    flex: 1;
                    padding: 40px;
                    overflow-y: auto;
                }
                h1 {
                    margin-bottom: 20px;
                    color: #ffffff;
                }
                p {
                    line-height: 1.6;
                    margin-bottom: 15px;
                }
                .code-block {
                    display: none;
                }
            """)
        ),
        html.body(
            html.div(
                html.h2('Navigation'),
                html.nav(
                    html.a('Home', href='/'),
                    html.a('Quickstart', href='/docs', class_='active')
                ),
                class_='sidebar'
            ),
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
                class_='main-content'
            ),
            html.script("""
                require.config({ paths: { vs: 'https://unpkg.com/monaco-editor@0.45.0/min/vs' } });
                require(['vs/editor/editor.main'], function() {
                    const codeBlocks = document.querySelectorAll('.code-block');
                    codeBlocks.forEach(function(block, index) {
                        const container = document.createElement('div');
                        container.id = 'editor-' + index;
                        container.style.height = '200px';
                        block.parentNode.insertBefore(container, block);

                        monaco.editor.create(container, {
                            value: block.value,
                            language: 'python',
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
                });
            """)
        )
    )

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

    hej.run(host='0.0.0.0', port=5000, debug=debug_config)