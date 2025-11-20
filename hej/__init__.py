__version__ = "0.2.0"
__author__ = "Matthew"

import sys
import builtins
from .hej import App, html, blocks

app = App()

def get(path: str):
    return app.get(path)

def not_found(func):
    return app.not_found(func)

def run(host='127.0.0.1', port=5000, debug=False):
    app.run(host=host, port=port, debug=debug)

builtins.get = get
builtins.not_found = not_found
builtins.html = html
builtins.blocks = blocks

current_module = sys.modules[__name__]
current_module.run = run

__all__ = ['get', 'not_found', 'run', 'app', 'App', 'html', 'blocks']

