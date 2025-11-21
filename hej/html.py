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

