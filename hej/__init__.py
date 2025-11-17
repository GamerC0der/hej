"""
Hej Framework - A Python library for websites
"""

__version__ = "0.1.0"
__author__ = "Matthew"

import sys
import builtins
from .hej import App

app = App()

def get(path: str):
    return app.get(path)

def not_found(func):
    return app.not_found(func)

def run(host='127.0.0.1', port=5000, debug=False):
    app.run(host=host, port=port, debug=debug)

builtins.get = get
builtins.not_found = not_found

current_module = sys.modules[__name__]
current_module.run = run

__all__ = ['get', 'not_found', 'run', 'app', 'App']

