import http.server
import socketserver
import threading
import urllib.parse
import os
import time
import json
from typing import Callable, Dict, Any

class HTMLElement:
    def __init__(self, tag: str, *children, **attrs):
        self.tag = tag
        self.attrs = attrs
        self.children = list(children)

    def __str__(self):
        attrs_str = ''
        if self.attrs:
            attr_map = {'class_': 'class', 'for_': 'for'}
            attrs = []
            for k, v in self.attrs.items():
                attr_name = attr_map.get(k, k)
                attrs.append(f'{attr_name}="{v}"')
            attrs_str = ' ' + ' '.join(attrs)

        if not self.children:
            return f'<{self.tag}{attrs_str}></{self.tag}>'

        children_str = ''.join(str(child) for child in self.children)
        return f'<{self.tag}{attrs_str}>{children_str}</{self.tag}>'

    def __call__(self, *children, **attrs):
        self.children.extend(children)
        self.attrs.update(attrs)
        return self

class ScriptBuilder:
    def __init__(self, code=None):
        self.blocks = []
        if code:
            self.blocks.append(code)

    def __call__(self, *blocks):
        sb = ScriptBuilder()
        sb.blocks.extend(self.blocks)
        for block in blocks:
            if isinstance(block, ScriptBuilder):
                sb.blocks.extend(block.blocks)
            elif hasattr(block, '__call__'):
                result = block()
                if isinstance(result, ScriptBuilder):
                    sb.blocks.extend(result.blocks)
            else:
                sb.blocks.append(str(block))
        return sb

    def when_dom_ready(self, *blocks):
        sb = ScriptBuilder("document.addEventListener('DOMContentLoaded', function() {")
        for block in blocks:
            if isinstance(block, ScriptBuilder):
                sb.blocks.extend(block.blocks)
            elif hasattr(block, '__call__'):
                result = block()
                if isinstance(result, ScriptBuilder):
                    sb.blocks.extend(result.blocks)
            else:
                sb.blocks.append(str(block))
        sb.blocks.append("});")
        return sb

    def on_click(self, selector, *blocks):
        sb = ScriptBuilder(f"document.querySelector('{selector}').addEventListener('click', function() {{")
        for block in blocks:
            if isinstance(block, ScriptBuilder):
                sb.blocks.extend(block.blocks)
            elif hasattr(block, '__call__'):
                result = block()
                if isinstance(result, ScriptBuilder):
                    sb.blocks.extend(result.blocks)
            else:
                sb.blocks.append(str(block))
        sb.blocks.append("});")
        return sb

    def alert(self, message):
        return ScriptBuilder(f"alert('{message}');")

    def __str__(self):
        return '\n'.join(self.blocks)

class HTMLBuilder:
    def __getattr__(self, tag: str):
        if tag == 'script':
            def script_builder(*children, **attrs):
                sb = ScriptBuilder()
                for child in children:
                    if isinstance(child, ScriptBuilder):
                        sb.blocks.extend(child.blocks)
                    elif hasattr(child, '__call__'):
                        result = child()
                        if isinstance(result, ScriptBuilder):
                            sb.blocks.extend(result.blocks)
                    else:
                        sb.blocks.append(str(child))
                return HTMLElement('script', sb, **attrs)
            return script_builder
        return lambda *children, **attrs: HTMLElement(tag, *children, **attrs)

html = HTMLBuilder()

class BlockBuilder:
    def __getattr__(self, name: str):
        def block_method(*args, **kwargs):
            return getattr(ScriptBuilder(), name)(*args, **kwargs)
        return block_method

blocks = BlockBuilder()

class App:
    def __init__(self):
        self.routes = {}
        self.server = None
        self.not_found_handler = None
        self.swagger_enabled = True

    def route(self, path: str, methods=None):
        if methods is None:
            methods = ['GET']

        def decorator(func: Callable):
            for method in methods:
                self.routes[(method, path)] = func
            return func
        return decorator

    def get(self, path: str):
        return self.route(path, ['GET'])

    def not_found(self, func: Callable):
        self.not_found_handler = func
        return func

    def render_template(self, template_name: str, context: dict = None):
        context = context or {}
        with open(os.path.join(os.path.dirname(__file__), '..', 'templates', template_name)) as f:
            template = f.read()
        for k, v in context.items():
            template = template.replace('{{ ' + k + ' }}', str(v))
        return template

    def generate_openapi_spec(self):
        """Generate OpenAPI 3.0 specification for all routes"""
        paths = {}
        for (method, path), handler in self.routes.items():
            if path not in paths:
                paths[path] = {}
            paths[path][method.lower()] = {
                'responses': {
                    '200': {
                        'description': 'Successful response'
                    }
                }
            }

        return {
            'openapi': '3.0.0',
            'info': {
                'title': 'Hej API',
                'version': '1.0.0',
                'description': 'Automatically generated API documentation'
            },
            'paths': paths
        }

    def serve_swagger_ui(self):
        """Serve Swagger UI HTML page"""
        spec = self.generate_openapi_spec()
        spec_json = json.dumps(spec)

        return f"""
<!DOCTYPE html>
<html>
<head>
    <title>Swagger UI - Hej API</title>
    <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@5.10.3/swagger-ui.css" />
    <style>
        html {{
            box-sizing: border-box;
            overflow: -moz-scrollbars-vertical;
            overflow-y: scroll;
        }}
        *, *:before, *:after {{
            box-sizing: inherit;
        }}
        body {{
            margin:0;
            background: #fafafa;
        }}
    </style>
</head>
<body>
    <div id="swagger-ui"></div>
    <script src="https://unpkg.com/swagger-ui-dist@5.10.3/swagger-ui-bundle.js"></script>
    <script src="https://unpkg.com/swagger-ui-dist@5.10.3/swagger-ui-standalone-preset.js"></script>
    <script>
        window.onload = function() {{
            const spec = {spec_json};
            const ui = SwaggerUIBundle({{
                spec: spec,
                dom_id: '#swagger-ui',
                deepLinking: true,
                presets: [
                    SwaggerUIBundle.presets.apis,
                    SwaggerUIStandalonePreset
                ],
                plugins: [
                    SwaggerUIBundle.plugins.DownloadUrl
                ],
                layout: "StandaloneLayout"
            }});
        }};
    </script>
</body>
</html>
"""

    def run(self, host='127.0.0.1', port=5000, debug=False):
        # Automatically add Swagger UI route
        if self.swagger_enabled and ('GET', '/swagger') not in self.routes:
            self.routes[('GET', '/swagger')] = self.serve_swagger_ui

        class Handler(http.server.BaseHTTPRequestHandler):
            def __init__(self, *args, app=None, **kwargs):
                self.app = app
                super().__init__(*args, **kwargs)

            def handle_request(self, method):
                path = urllib.parse.urlparse(self.path).path
                if (method, path) in self.app.routes:
                    try:
                        result = self.app.routes[(method, path)]()
                        if isinstance(result, tuple) and len(result) == 2:
                            result = self.app.render_template(*result)
                        elif isinstance(result, str) and result.endswith('.html'):
                            result = self.app.render_template(result)
                        result_str = str(result)
                        self.send_response(200)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                        self.wfile.write(result_str.encode())
                    except:
                        self.send_response(500)
                        self.end_headers()
                        self.wfile.write(b'Internal Server Error')
                else:
                    self.send_response(404)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    if self.app.not_found_handler:
                        try:
                            result = self.app.not_found_handler()
                            self.wfile.write(str(result).encode())
                        except:
                            self.wfile.write(b'Not Found')
                    else:
                        self.wfile.write(b'Not Found')
            def log_message(self, format, *args):
                if debug:
                    super().log_message(format, *args)
            do_GET = lambda self: self.handle_request('GET')
            do_POST = lambda self: self.handle_request('POST')
            do_PUT = lambda self: self.handle_request('PUT')
            do_DELETE = lambda self: self.handle_request('DELETE')

        def run_server():
            socketserver.TCPServer.allow_reuse_address = True
            try:
                self.server = socketserver.TCPServer((host, port), lambda *args, **kwargs: Handler(*args, app=self, **kwargs))
                print(f'Server running on http://{host}:{port}')
                self.server.serve_forever()
            except OSError as e:
                if e.errno == 48:
                    print(f'Port {port} is already in use. Try a different port or kill existing processes.')
                else:
                    print(f'Error starting server: {e}')
                return

        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()

        try:
            test_file = __import__('sys').argv[0]
            templates_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
            mtime_test = os.stat(test_file).st_mtime
            mtime_templates = 0
            if os.path.exists(templates_dir):
                mtime_templates = max((os.stat(os.path.join(templates_dir, f)).st_mtime for f in os.listdir(templates_dir) if f.endswith('.html')), default=0)
            while True:
                time.sleep(1)
                current_mtime_templates = 0
                if os.path.exists(templates_dir):
                    current_mtime_templates = max((os.stat(os.path.join(templates_dir, f)).st_mtime for f in os.listdir(templates_dir) if f.endswith('.html')), default=0)
                if os.stat(test_file).st_mtime != mtime_test or current_mtime_templates != mtime_templates:
                    print('Files changed, restarting...')
                    self.server.shutdown()
                    server_thread.join()
                    return self.run(host, port, debug)
        except KeyboardInterrupt:
            if self.server:
                self.server.shutdown()
            print('Server stopped')
