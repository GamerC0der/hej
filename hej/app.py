import http.server
import socketserver
import threading
import urllib.parse
import os
import time
import json
import sys
import glob
import ast
import runpy
from typing import Callable, Dict, Any

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

    def run(self, host='0.0.0.0', port=5000, debug=False):
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
                        if method != 'HEAD':
                            self.wfile.write(result_str.encode())
                    except:
                        self.send_response(500)
                        self.end_headers()
                        if method != 'HEAD':
                            self.wfile.write(b'Internal Server Error')
                else:
                    self.send_response(404)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    if self.app.not_found_handler:
                        try:
                            result = self.app.not_found_handler()
                            if method != 'HEAD':
                                self.wfile.write(str(result).encode())
                        except:
                            if method != 'HEAD':
                                self.wfile.write(b'Not Found')
                    else:
                        if method != 'HEAD':
                            self.wfile.write(b'Not Found')
            def log_message(self, format, *args):
                if debug:
                    super().log_message(format, *args)
            do_GET = lambda self: self.handle_request('GET')
            do_POST = lambda self: self.handle_request('POST')
            do_PUT = lambda self: self.handle_request('PUT')
            do_DELETE = lambda self: self.handle_request('DELETE')
            do_HEAD = lambda self: self.handle_request('HEAD')

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

            watch_file_changes = os.path.isfile(test_file)
            mtime_test = 0
            if watch_file_changes:
                mtime_test = os.stat(test_file).st_mtime

            mtime_templates = 0
            if os.path.exists(templates_dir):
                mtime_templates = max((os.stat(os.path.join(templates_dir, f)).st_mtime for f in os.listdir(templates_dir) if f.endswith('.html')), default=0)
            while True:
                time.sleep(1)
                current_mtime_templates = 0
                if os.path.exists(templates_dir):
                    current_mtime_templates = max((os.stat(os.path.join(templates_dir, f)).st_mtime for f in os.listdir(templates_dir) if f.endswith('.html')), default=0)

                file_changed = False
                if watch_file_changes:
                    current_mtime_test = os.stat(test_file).st_mtime
                    file_changed = current_mtime_test != mtime_test
                    mtime_test = current_mtime_test

                if file_changed or current_mtime_templates != mtime_templates:
                    print('Files changed, restarting...')
                    if self.server:
                        self.server.shutdown()
                    server_thread.join()
                    return self.run(host, port, debug)
        except KeyboardInterrupt:
            if self.server:
                self.server.shutdown()
            print('Server stopped')


def find_hej_app_files():
    candidates = [
        'app.py', 'main.py', 'server.py', 'application.py',
        'test.py', 'run.py', 'index.py', 'start.py'
    ]

    for candidate in candidates:
        if os.path.isfile(candidate):
            if has_hej_import_and_run(candidate):
                return candidate

    for py_file in glob.glob('*.py'):
        if py_file not in ['__init__.py'] and has_hej_import_and_run(py_file):
            return py_file

    return None

def has_hej_import_and_run(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()

        tree = ast.parse(content)

        has_hej_import = False
        has_run_call = False

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name == 'hej':
                        has_hej_import = True
            elif isinstance(node, ast.ImportFrom):
                if node.module == 'hej':
                    has_hej_import = True

            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    if isinstance(node.func.value, ast.Name):
                        if node.func.attr == 'run':
                            has_run_call = True
                elif isinstance(node.func, ast.Name) and node.func.id == 'run':
                    has_run_call = True

        return has_hej_import and has_run_call
    except:
        return False

def convert_flask_to_hej(content):
    import re

    lines = content.split('\n')
    converted_lines = []
    app_name = None
    has_run_call = False

    for line in lines:
        original_line = line

        if 'from flask import' in line or 'import flask' in line:
            line = 'import hej'

        elif 'app = Flask(' in line:
            match = re.search(r'app\s*=\s*Flask\([^)]*\)', line)
            if match:
                app_name = 'app'
                continue

        elif re.search(r'\w+\s*=\s*Flask\([^)]*\)', line):
            match = re.search(r'(\w+)\s*=\s*Flask\([^)]*\)', line)
            if match:
                app_name = match.group(1)
                continue

        elif '@app.route(' in line:
            match = re.search(r'@app\.route\(([^)]+)\)', line)
            if match:
                route_args = match.group(1)
                methods_match = re.search(r'methods\s*=\s*\[([^\]]+)\]', route_args)
                if methods_match:
                    methods = methods_match.group(1).replace("'", "").replace('"', "").split(',')
                    method = methods[0].strip().upper()
                    route_path = re.sub(r',\s*methods\s*=\s*\[.*\]', '', route_args)
                else:
                    method = 'GET'
                    route_path = route_args

                if method == 'GET':
                    line = f'@get({route_path})'
                else:
                    line = f'@app.route({route_path}, methods=["{method}"])'

        elif re.search(r'if\s+__name__\s*==\s*[\'"]__main__[\'"]\s*:', line):
            converted_lines.append(line)
            converted_lines.append('    hej.run()')
            has_run_call = True
            continue

        elif 'app.run(' in line:
            if not has_run_call:
                line = '    hej.run()'
                has_run_call = True
            else:
                continue

        converted_lines.append(line)

    result = '\n'.join(converted_lines)

    if app_name and app_name != 'app':
        result = result.replace(f'@{app_name}.route(', '@get(')
        result = result.replace(f'{app_name}.run(', 'hej.run(')

    if not has_run_call:
        result += '\n\nif __name__ == \'__main__\':\n    hej.run()'

    return result

def main():
    if len(sys.argv) < 2:
        print("Usage: hej <command> [options]")
        print("Commands:")
        print("  <filename>    Run a specific Python file")
        print("  dev           Auto-detect and run Hej application")
        print("  convert       Convert Flask app to Hej format")
        print("  --version     Show version information")
        sys.exit(1)

    command = sys.argv[1]

    if command == '--version' or command == '-v':
        try:
            import hej
            print(f"hej {hej.__version__}")
        except:
            print("hej 0.1.0")
        sys.exit(0)

    elif command == 'convert':
        if len(sys.argv) < 3:
            print("Usage: hej convert <flask_file> [output_file]")
            sys.exit(1)

        flask_file = sys.argv[2]
        output_file = sys.argv[3] if len(sys.argv) > 3 else flask_file.replace('.py', '_hej.py')

        if not os.path.isfile(flask_file):
            print(f"Error: File '{flask_file}' not found")
            sys.exit(1)

        try:
            with open(flask_file, 'r', encoding='utf-8') as f:
                content = f.read()

            converted_content = convert_flask_to_hej(content)

            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(converted_content)

            print(f"Converted Flask app saved to: {output_file}")

        except Exception as e:
            print(f"Error converting file: {e}")
            sys.exit(1)
        sys.exit(0)

    elif command == 'dev':
        app_file = find_hej_app_files()
        if not app_file:
            print("Error: Could not find a Hej application file.")
            print("Make sure you have a Python file that imports 'hej' and calls run()")
            sys.exit(1)

        print(f"Found Hej application: {app_file}")
        filename = app_file

    else:
        filename = command
        if not os.path.isfile(filename):
            print(f"Error: File '{filename}' not found")
            sys.exit(1)

    runpy.run_path(filename, run_name='__main__')


if __name__ == '__main__':
    main()
