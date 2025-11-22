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
                    'width': '240px',
                    'background-color': '#2a2a2a',
                    'padding': '24px 20px',
                    'border-right': '1px solid #444444',
                    'box-shadow': '2px 0 8px rgba(0,0,0,0.4)',
                    'position': 'sticky',
                    'top': '0',
                    'height': '100vh',
                    'overflow-y': 'auto'
                }),
                css.sidebar__h2({
                    'color': '#ffffff',
                    'font-size': '16px',
                    'margin-bottom': '24px',
                    'font-weight': '600',
                    'letter-spacing': '0.5px',
                    'text-transform': 'uppercase'
                }),
                css.sidebar__nav({
                    'display': 'flex',
                    'flex-direction': 'column',
                    'gap': '4px'
                }),
                css.sidebar__a({
                    'color': '#b0b0b0',
                    'text-decoration': 'none',
                    'padding': '12px 16px',
                    'border-radius': '6px',
                    'transition': 'all 0.2s ease',
                    'font-size': '14px',
                    'font-weight': '500',
                    'display': 'flex',
                    'align-items': 'center',
                    'position': 'relative',
                    'border-left': '3px solid transparent'
                }),
                css.sidebar__a__hover({
                    'background-color': '#3a3a3a',
                    'color': '#ffffff',
                    'transform': 'translateX(2px)',
                    'border-left-color': '#5dade2'
                }),
                css.sidebar__a__active({
                    'background-color': '#444444',
                    'color': '#ffffff',
                    'border-left-color': '#5dade2',
                    'box-shadow': '0 2px 8px rgba(93, 173, 226, 0.2)'
                }),
                css.sidebar__a__focus({
                    'outline': '2px solid #5dade2',
                    'outline-offset': '2px',
                    'background-color': '#3a3a3a',
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
                }),
                css.builder_container({
                    'display': 'flex',
                    'flex-direction': 'column',
                    'gap': '20px'
                }),
                css.editor_container({
                    'margin-bottom': '10px'
                }),
                css.convert_button({
                    'padding': '10px 20px',
                    'background-color': '#444444',
                    'color': '#ffffff',
                    'border': 'none',
                    'border-radius': '4px',
                    'cursor': 'pointer',
                    'font-size': '16px',
                    'align-self': 'center',
                    'transition': 'background-color 0.2s'
                }),
                css.convert_button__hover({
                    'background-color': '#555555'
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
                    html.a('Builder', href='#', **{'data-tab': 'builder'}),
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
                    html.h1('Hej Builder'),
                    html.p('Convert Flask or FastAPI code to Hej Framework code automatically:'),
                    html.div(
                        html.select(
                            html.option('Flask', value='flask', selected='selected'),
                            html.option('FastAPI', value='fastapi'),
                            id='framework-select',
                            onchange='changeFramework(this.value)',
                            style='margin-bottom: 10px; padding: 5px;'
                        ),
                        class_='framework-selector'
                    ),
                    html.div(
                        html.div(
                            html.h3('Flask Code Input', id='input-label'),
                            html.div(id='flask-editor', class_='monaco-editor', style='height: 300px;'),
                            class_='editor-container'
                        ),
                        html.div(
                            html.button('Convert to Hej', id='convert-btn', onclick='convertFlaskToHej()', class_='convert-button'),
                            class_='convert-container'
                        ),
                        html.div(
                            html.h3('Hej Code Output'),
                            html.div(id='hej-editor', class_='monaco-editor', style='height: 300px;'),
                            class_='editor-container'
                        ),
                        class_='builder-container'
                    ),
                    class_='tab-content',
                    id='builder'
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

                    window.currentFramework = 'flask';

                    window.flaskCode = `from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return '<h1>About Page</h1>'

if __name__ == '__main__':
    app.run(debug=True)`;

                    window.fastApiCode = `from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get('/', response_class=HTMLResponse)
async def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head><title>Home</title></head>
    <body><h1>Hello World</h1></body>
    </html>
    '''

@app.get('/about', response_class=HTMLResponse)
async def about():
    return '<h1>About Page</h1>'

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)`;

                    window.flaskEditor = monaco.editor.create(document.getElementById('flask-editor'), {
                        value: window.flaskCode,
                        language: 'python',
                        theme: 'vs-dark',
                        minimap: { enabled: false },
                        scrollBeyondLastLine: false,
                        automaticLayout: true,
                        fontSize: 14,
                        lineNumbers: 'on'
                    });

                    window.changeFramework = function(framework) {
                        window.currentFramework = framework;
                        const label = document.getElementById('input-label');
                        if (framework === 'fastapi') {
                            label.textContent = 'FastAPI Code Input';
                            flaskEditor.setValue(window.fastApiCode);
                        } else {
                            label.textContent = 'Flask Code Input';
                            flaskEditor.setValue(window.flaskCode);
                        }
                    };

                    window.hejEditor = monaco.editor.create(document.getElementById('hej-editor'), {
                        value: '',
                        language: 'python',
                        theme: 'vs-dark',
                        minimap: { enabled: false },
                        scrollBeyondLastLine: false,
                        automaticLayout: true,
                        fontSize: 14,
                        lineNumbers: 'on',
                        readOnly: true
                    });

                    window.convertFlaskToHej = function() {
                        const inputCode = flaskEditor.getValue();
                        let hejCode = '';

                        if (window.currentFramework === 'fastapi') {
                            hejCode = convertFastApiCode(inputCode);
                        } else {
                            hejCode = convertFlaskCode(inputCode);
                        }

                        hejEditor.setValue(hejCode);
                    };

                    function convertFlaskCode(flaskCode) {
                        let hejCode = 'import hej\\n\\n';
                        const lines = flaskCode.split('\\n');
                        let inRoute = false;
                        let routeFunction = '';
                        let indentLevel = 0;

                        for (let i = 0; i < lines.length; i++) {
                            const line = lines[i];
                            const trimmedLine = line.trim();

                            if (trimmedLine.includes('Flask(__name__)')) {
                                continue;
                            }

                            if (trimmedLine.includes('@app.route(')) {
                                const routeMatch = trimmedLine.match(/@app\\.route\\('([^']+)'(?:, methods=\\['([^']+)'\\])?/);
                                if (routeMatch) {
                                    const route = routeMatch[1];
                                    const method = routeMatch[2] ? routeMatch[2].toLowerCase() : 'get';
                                    hejCode += `@${method}('${route}')\\n`;
                                    inRoute = true;
                                    indentLevel = 0;
                                }
                                continue;
                            }

                            if (trimmedLine.includes('def ') && inRoute) {
                                const funcMatch = trimmedLine.match(/def (\\w+)\\(\\):/);
                                if (funcMatch) {
                                    routeFunction = funcMatch[1];
                                    hejCode += `def ${routeFunction}():\\n`;
                                    indentLevel = 1;
                                }
                                continue;
                            }

                            if (trimmedLine.includes('render_template(')) {
                                const templateMatch = trimmedLine.match(/render_template\\('([^']+)'(?:, (.+?))?\\)?$/);
                                if (templateMatch) {
                                    const template = templateMatch[1];
                                    const context = templateMatch[2];
                                    if (context) {
                                        hejCode += `    return hej.template('${template}', ${context})\\n`;
                                    } else {
                                        hejCode += `    return '${template}'\\n`;
                                    }
                                }
                                continue;
                            }

                            if (trimmedLine.includes('return ')) {
                                const returnMatch = trimmedLine.match(/return ['"](.+?)['"]/);
                                if (returnMatch) {
                                    const htmlContent = returnMatch[1];
                                    const hejHtml = convertHtmlStringToHej(htmlContent);
                                    hejCode += `    return ${hejHtml}\\n`;
                                }
                                continue;
                            }

                            if (trimmedLine.includes('if __name__') || trimmedLine.includes('app.run(')) {
                                continue;
                            }

                            if (trimmedLine && !trimmedLine.includes('from flask')) {
                                const indent = '    '.repeat(indentLevel);
                                hejCode += indent + line + '\\n';
                            }

                            if (trimmedLine.endsWith(':')) {
                                indentLevel++;
                            }
                            if (trimmedLine === '' && indentLevel > 1) {
                                indentLevel = Math.max(1, indentLevel - 1);
                            }
                        }

                        hejCode += '\\nif __name__ == \\'__main__\\':\\n    hej.run()';
                        return hejCode;
                    }

                    function convertFastApiCode(fastApiCode) {
                        let hejCode = 'import hej\\n\\n';
                        const lines = fastApiCode.split('\\n');
                        let inRoute = false;
                        let routeFunction = '';
                        let indentLevel = 0;

                        for (let i = 0; i < lines.length; i++) {
                            const line = lines[i];
                            const trimmedLine = line.trim();

                            if (trimmedLine.includes('FastAPI()')) {
                                continue;
                            }

                            if (trimmedLine.match(/@app\\.(get|post|put|delete|patch|head|options)\\(/)) {
                                const routeMatch = trimmedLine.match(/@app\\.(get|post|put|delete|patch|head|options)\\('([^']+)'/);
                                if (routeMatch) {
                                    const method = routeMatch[1];
                                    const route = routeMatch[2];
                                    hejCode += `@${method}('${route}')\\n`;
                                    inRoute = true;
                                    indentLevel = 0;
                                }
                                continue;
                            }

                            if (trimmedLine.includes('async def ') && inRoute) {
                                const funcMatch = trimmedLine.match(/async def (\\w+)\\(/);
                                if (funcMatch) {
                                    routeFunction = funcMatch[1];
                                    hejCode += `def ${routeFunction}():\\n`;
                                    indentLevel = 1;
                                }
                                continue;
                            }

                            if (trimmedLine.includes('def ') && inRoute && !trimmedLine.includes('async def ')) {
                                const funcMatch = trimmedLine.match(/def (\\w+)\\(\\):/);
                                if (funcMatch) {
                                    routeFunction = funcMatch[1];
                                    hejCode += `def ${routeFunction}():\\n`;
                                    indentLevel = 1;
                                }
                                continue;
                            }

                            if (trimmedLine.includes('return HTMLResponse(')) {
                                const htmlMatch = trimmedLine.match(/return HTMLResponse\\((.+?)\\)/s);
                                if (htmlMatch) {
                                    const htmlContent = htmlMatch[1].trim();
                                    if (htmlContent.startsWith('content=')) {
                                        const contentMatch = htmlContent.match(/content=['"](.+?)['"]/s);
                                        if (contentMatch) {
                                            const htmlString = contentMatch[1];
                                            const hejHtml = convertHtmlStringToHej(htmlString);
                                            hejCode += `    return ${hejHtml}\\n`;
                                        }
                                    }
                                }
                                continue;
                            }

                            if (trimmedLine.includes('return ')) {
                                const returnMatch = trimmedLine.match(/return ['"](.+?)['"]/);
                                if (returnMatch) {
                                    const htmlContent = returnMatch[1];
                                    const hejHtml = convertHtmlStringToHej(htmlContent);
                                    hejCode += `    return ${hejHtml}\\n`;
                                }
                                continue;
                            }

                            if (trimmedLine.includes('if __name__') || trimmedLine.includes('uvicorn.run(')) {
                                continue;
                            }

                            if (trimmedLine && !trimmedLine.includes('from fastapi') && !trimmedLine.includes('import uvicorn')) {
                                const indent = '    '.repeat(indentLevel);
                                hejCode += indent + line + '\\n';
                            }

                            if (trimmedLine.endsWith(':')) {
                                indentLevel++;
                            }
                            if (trimmedLine === '' && indentLevel > 1) {
                                indentLevel = Math.max(1, indentLevel - 1);
                            }
                        }

                        hejCode += '\\nif __name__ == \\'__main__\\':\\n    hej.run()';
                        return hejCode;
                    }

                    function convertHtmlStringToHej(htmlString) {
                        const parser = new DOMParser();
                        const doc = parser.parseFromString(htmlString, 'text/html');

                        function convertElement(element) {
                            if (element.nodeType === Node.TEXT_NODE) {
                                const text = element.textContent.trim();
                                return text ? `'${text}'` : '';
                            }

                            if (element.nodeType !== Node.ELEMENT_NODE) {
                                return '';
                            }

                            const tagName = element.tagName.toLowerCase();
                            let attrs = '';

                            for (let i = 0; i < element.attributes.length; i++) {
                                const attr = element.attributes[i];
                                if (attr.name === 'class') {
                                    attrs += `, class_='${attr.value}'`;
                                } else {
                                    attrs += `, ${attr.name}='${attr.value}'`;
                                }
                            }

                            let children = [];
                            for (let child of element.childNodes) {
                                const converted = convertElement(child);
                                if (converted) {
                                    children.push(converted);
                                }
                            }

                            if (children.length === 0) {
                                return `html.${tagName}(${attrs.slice(2)})`;
                            } else if (children.length === 1) {
                                return `html.${tagName}(${children[0]}${attrs})`;
                            } else {
                                return `html.${tagName}(\\n        ${children.join(',\\n        ')}\\n    ${attrs})`;
                            }
                        }

                        const bodyContent = Array.from(doc.body.childNodes)
                            .map(convertElement)
                            .filter(x => x)
                            .join(',\\n        ');

                        return `html.html(\\n        html.head(\\n            html.title('Page')\\n        ),\\n        html.body(\\n            ${bodyContent}\\n        )\\n    )`;
                    }

                    const sidebarLinks = document.querySelectorAll('.sidebar a[data-tab]');
                    const tabContents = document.querySelectorAll('.tab-content');

                    function switchTab(link) {
                        sidebarLinks.forEach(l => l.classList.remove('active'));
                        link.classList.add('active');

                        tabContents.forEach(content => content.classList.remove('active'));

                        const tabId = link.getAttribute('data-tab');
                        const selectedTab = document.getElementById(tabId);
                        if (selectedTab) {
                            selectedTab.classList.add('active');
                            selectedTab.scrollIntoView({ behavior: 'smooth', block: 'start' });
                        }
                    }

                    sidebarLinks.forEach((link, index) => {
                        link.addEventListener('click', function(e) {
                            e.preventDefault();
                            switchTab(this);
                        });

                        link.addEventListener('keydown', function(e) {
                            if (e.key === 'Enter' || e.key === ' ') {
                                e.preventDefault();
                                switchTab(this);
                            } else if (e.key === 'ArrowDown') {
                                e.preventDefault();
                                const nextIndex = (index + 1) % sidebarLinks.length;
                                sidebarLinks[nextIndex].focus();
                            } else if (e.key === 'ArrowUp') {
                                e.preventDefault();
                                const prevIndex = (index - 1 + sidebarLinks.length) % sidebarLinks.length;
                                sidebarLinks[prevIndex].focus();
                            }
                        });
                    });

                    // Set initial focus on active tab
                    const activeLink = document.querySelector('.sidebar a.active');
                    if (activeLink) {
                        activeLink.focus();
                    }
                });
            """)
        )
    )

if __name__ == '__main__':
    debug_config = {'enabled': True, 'log_level': 'DEBUG', 'log_requests': True, 'log_responses': True, 'log_timing': True, 'show_stack_traces': True, 'log_static_files': False, 'log_templates': True, 'colorize_logs': True}

    hej.run(host='0.0.0.0', port=5000, debug=debug_config)