import os
import sys
import json
import time
import glob
import ast
import runpy
import http.server
import socketserver
import threading
import urllib.parse
from typing import Callable, Dict, Any

class HTMLElement:
    def __init__(self, tag: str, *children, **attrs):
        self.tag = tag
        self.attrs = attrs
        self.children = list(children)

    def __str__(self):
        attr_map = {'class_': 'class', 'for_': 'for'}
        attrs_str = ''.join(f' {attr_map.get(k, k)}="{v}"' for k, v in self.attrs.items())
        content = ''.join(str(child) for child in self.children)
        return f'<{self.tag}{attrs_str}>{content}</{self.tag}>'

    def __call__(self, *children, **attrs):
        self.children.extend(children)
        self.attrs.update(attrs)
        return self

class ScriptBuilder:
    def __init__(self, code=None):
        self.blocks = [code] if code else []

    def _process_blocks(self, blocks):
        result = []
        for block in blocks:
            if isinstance(block, ScriptBuilder):
                result.extend(block.blocks)
            elif callable(block):
                result.extend(block().blocks if isinstance(block(), ScriptBuilder) else [str(block())])
            else:
                result.append(str(block))
        return result

    def __call__(self, *blocks):
        return ScriptBuilder('\n'.join(self.blocks + self._process_blocks(blocks)))

    def _add_event_handler(self, event_code, blocks):
        return ScriptBuilder('\n'.join([event_code] + self._process_blocks(blocks) + ['});']))

    def when_dom_ready(self, *blocks):
        return self._add_event_handler("document.addEventListener('DOMContentLoaded', function() {", blocks)

    def on_click(self, selector, *blocks):
        return self._add_event_handler(f"document.querySelector('{selector}').addEventListener('click', function() {{", blocks)

    def alert(self, message):
        return ScriptBuilder(f"alert('{message}');")

    def __str__(self):
        return '\n'.join(self.blocks)

class CSSBuilder:
    def __init__(self, selector=None, rules=None):
        self.blocks = []
        self._mixins = {}
        if selector and rules:
            self.blocks.append(f"{selector} {{\n{self._format_rules(rules)}\n}}")

    def _format_rules(self, rules):
        if isinstance(rules, dict):
            return '\n'.join(f"    {k}: {v};" for k, v in rules.items())
        return str(rules)

    def _process_blocks(self, blocks, indent=""):
        result = []
        for block in blocks:
            if isinstance(block, CSSBuilder):
                for b in block.blocks:
                    result.append(indent + b.replace('\n', '\n' + indent))
            elif isinstance(block, dict):
                result.append(indent + self._format_rules(block))
            else:
                result.append(indent + str(block))
        return result

    def __call__(self, *blocks):
        return CSSBuilder('\n'.join(self.blocks + [str(block) for block in blocks if not isinstance(block, (CSSBuilder, dict))] +
                                   [self._format_rules(block) for block in blocks if isinstance(block, dict)] +
                                   [b for block in blocks if isinstance(block, CSSBuilder) for b in block.blocks]))

    def __getattr__(self, selector: str):
        def selector_method(rules=None, **kwargs):
            if rules is None:
                rules = kwargs
            selector_str = f"{selector.split('__')[0]}:{selector.split('__')[1]}" if '__' in selector else selector
            return CSSBuilder(selector_str, rules)
        return selector_method

    def nest(self, selector, *blocks):
        return CSSBuilder(f"{selector} {{\n" + '\n'.join(self._process_blocks(blocks, '    ')) + "\n}")

    def mixin(self, name, rules=None, **kwargs):
        self._mixins[name] = rules or kwargs
        return self

    def use_mixin(self, name):
        return CSSBuilder(rules=self._mixins.get(name, {}))

    def media(self, query, *blocks):
        return CSSBuilder(f"@media {query} {{\n" + '\n'.join(self._process_blocks(blocks, '    ')) + "\n}")

    def keyframes(self, name, *frames):
        frames_str = []
        for frame in frames:
            if isinstance(frame, dict) and len(frame) == 1:
                key, rules = next(iter(frame.items()))
                frames_str.extend([f"    {key} {{", f"        {self._format_rules(rules)}", "    }"])
        return CSSBuilder(f"@keyframes {name} {{\n" + '\n'.join(frames_str) + "\n}")

    def variable(self, name, value):
        return CSSBuilder(rules={f'--{name}': value})

    def __add__(self, other):
        if isinstance(other, CSSBuilder):
            return CSSBuilder('\n'.join(self.blocks + other.blocks))
        return self

    def __str__(self):
        return '\n'.join(self.blocks)

class HTMLBuilder:
    def tailwind_css(self):
        return HTMLElement('link', rel='stylesheet', href='/static/css/tailwind.css')

    def __getattr__(self, tag: str):
        if tag == 'script':
            def script_builder(*children, **attrs):
                sb = ScriptBuilder()
                for child in children:
                    if isinstance(child, ScriptBuilder):
                        sb.blocks.extend(child.blocks)
                    elif callable(child):
                        result = child()
                        if isinstance(result, ScriptBuilder):
                            sb.blocks.extend(result.blocks)
                    else:
                        sb.blocks.append(str(child))
                return HTMLElement(tag, sb, **attrs)
            return script_builder
        elif tag == 'style':
            def style_builder(*children, **attrs):
                cb = CSSBuilder()
                for child in children:
                    if isinstance(child, CSSBuilder):
                        cb.blocks.extend(child.blocks)
                    elif callable(child):
                        result = child()
                        if isinstance(result, CSSBuilder):
                            cb.blocks.extend(result.blocks)
                    else:
                        cb.blocks.append(str(child))
                return HTMLElement(tag, cb, **attrs)
            return style_builder
        return lambda *children, **attrs: HTMLElement(tag, *children, **attrs)

html = HTMLBuilder()


class CSSBlockBuilder:
    HTML_ELEMENTS = {'body', 'html', 'head', 'div', 'span', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                     'a', 'button', 'input', 'form', 'table', 'tr', 'td', 'th', 'ul', 'ol', 'li',
                     'img', 'video', 'audio', 'canvas', 'svg', 'path', 'circle', 'rect', 'nav'}

    PSEUDO_SELECTORS = {'hover', 'focus', 'visited', 'link', 'before', 'after', 'first-child',
                       'last-child', 'nth-child', 'disabled', 'checked', 'required', 'invalid', 'valid'}

    def _build_selector(self, parts):
        selectors = []
        for part in parts:
            if part in self.HTML_ELEMENTS:
                selectors.append(part)
            elif part in self.PSEUDO_SELECTORS:
                selectors.append(f':{part}')
            else:
                selectors.append(f'.{part.replace("_", "-")}')
        return ' '.join(selectors)

    def __getattr__(self, name: str):
        parts = name.split('__')
        selector = self._build_selector(parts)
        return lambda rules=None, **kwargs: CSSBuilder(selector, rules or kwargs)

css = CSSBlockBuilder()