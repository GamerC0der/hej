import http.server
import socketserver
import threading
import urllib.parse
from typing import Callable, Dict

class App:
    def __init__(self):
        self.routes = {}
        self.server = None
        self.not_found_handler = None

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

    def run(self, host='127.0.0.1', port=5000, debug=False):
        class Handler(http.server.BaseHTTPRequestHandler):
            def __init__(self, *args, app=None, **kwargs):
                self.app = app
                super().__init__(*args, **kwargs)

            def handle_request(self, method):
                path = urllib.parse.urlparse(self.path).path
                if (method, path) in self.app.routes:
                    try:
                        result = self.app.routes[(method, path)]()
                        self.send_response(200)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                        self.wfile.write(str(result).encode())
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
            server_thread.join()
        except KeyboardInterrupt:
            if self.server:
                self.server.shutdown()
            print('Server stopped')
