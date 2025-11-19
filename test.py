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
                }
                h1 {
                    margin-bottom: 40px;
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
                }
            """)
        ),
        html.body(
            html.h1('Hej, World!'),
            html.div(
                html.button('Download Hej'),
                html.button('View Docs', onclick="window.location.href='/docs'"),
                class_='buttons'
            )
        )
    ) 

def generate_docs():
    """Generate documentation from hej.py automatically"""
    import ast
    import inspect
    from pathlib import Path

    hej_file = Path(__file__).parent / 'hej' / 'hej.py'
    with open(hej_file, 'r') as f:
        source = f.read()

    tree = ast.parse(source)

    classes = {}
    functions = {}
    decorators = {}

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            classes[node.name] = {
                'docstring': ast.get_docstring(node),
                'methods': []
            }
        elif isinstance(node, ast.FunctionDef) and not node.name.startswith('_'):
            if node.name in ['get', 'post', 'put', 'delete']:
                decorators[node.name] = ast.get_docstring(node)
            else:
                functions[node.name] = ast.get_docstring(node)

    sidebar_items = []
    content_sections = []

    sidebar_items.append(html.li(html.a('Quickstart', href='#quickstart')))
    content_sections.append(html.div(
        html.h2('Quickstart', id='quickstart'),
        html.p('Get started with Hej in under 5 minutes.'),
        html.div(
            html.h3('Installation'),
            html.pre('pip install hej-framework', class_='code'),
            html.h3('Basic App'),
            html.pre('import hej\n\n@get(\'/\')\ndef home():\n    return html.html(\n        html.head(html.title(\'Hello\')),\n        html.body(html.h1(\'Hello, World!\'))\n    )\n\nif __name__ == \'__main__\':\n    hej.run()', class_='code'),
            class_='step'
        )
    ))

    if classes:
        sidebar_items.append(html.li(html.a('API Reference', href='#api')))
        api_content = [html.h2('API Reference', id='api')]

        for class_name, class_info in classes.items():
            api_content.extend([
                html.h3(f'Class: {class_name}'),
                html.p(class_info['docstring'] or 'No documentation available.'),
                html.h4('Methods:'),
                html.ul(*[html.li(f"{method}: {getattr(getattr(globals().get(class_name.lower(), type), method, None), '__doc__', 'No docs') or 'No documentation'}")
                         for method in dir(globals().get(class_name.lower(), type))
                         if not method.startswith('_') and callable(getattr(globals().get(class_name.lower(), type), method, None))][:5])
            ])

        content_sections.append(html.div(*api_content, class_='step'))

    if decorators:
        sidebar_items.append(html.li(html.a('Decorators', href='#decorators')))
        decorator_content = [html.h2('Decorators', id='decorators')]

        for decorator_name, docstring in decorators.items():
            decorator_content.append(html.div(
                html.h3(f'@{decorator_name}'),
                html.p(docstring or 'Route decorator'),
                html.pre(f'@{decorator_name}(\'/path\')\ndef handler():\n    return html.html(...)', class_='code'),
                class_='step'
            ))

        content_sections.append(html.div(*decorator_content))

    return html.html(
        html.head(
            html.title('Hej Documentation'),
            html.style("""
                body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 0; display: flex; min-height: 100vh; line-height: 1.6; }
                .sidebar { width: 280px; background: #f8f9fa; padding: 20px; border-right: 1px solid #dee2e6; overflow-y: auto; position: sticky; top: 0; height: 100vh; }
                .sidebar h3 { margin-top: 0; color: #495057; font-size: 18px; }
                .sidebar ul { list-style: none; padding: 0; }
                .sidebar li { margin: 8px 0; }
                .sidebar a { text-decoration: none; color: #007bff; display: block; padding: 5px 0; }
                .sidebar a:hover { text-decoration: underline; }
                .main { flex: 1; padding: 40px; max-width: 800px; }
                .step { background: #f8f9fa; padding: 20px; margin: 25px 0; border-radius: 8px; }
                .code { background: #f1f3f4; padding: 15px; font-family: 'SF Mono', Monaco, 'Cascadia Code', monospace; border-radius: 6px; overflow-x: auto; font-size: 14px; }
                h1 { color: #212529; margin-bottom: 10px; }
                h2 { color: #343a40; margin: 40px 0 20px 0; padding-bottom: 10px; border-bottom: 2px solid #e9ecef; }
                h3 { color: #495057; margin: 30px 0 15px 0; }
                p { margin: 15px 0; }
            """)
        ),
        html.body(
            html.div(
                html.h3('Hej Framework Docs'),
                html.ul(*sidebar_items),
                class_='sidebar'
            ),
            html.div(
                html.h1('Hej Framework Documentation'),
                html.p('Automatically generated documentation from hej.py'),
                *content_sections,
                class_='main'
            )
        )
    )

@get('/docs')
def docs():
    return generate_docs()

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