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

    def _process_blocks(self, blocks):
        result_blocks = []
        for block in blocks:
            if isinstance(block, ScriptBuilder):
                result_blocks.extend(block.blocks)
            elif hasattr(block, '__call__'):
                result = block()
                if isinstance(result, ScriptBuilder):
                    result_blocks.extend(result.blocks)
            else:
                result_blocks.append(str(block))
        return result_blocks

    def __call__(self, *blocks):
        sb = ScriptBuilder()
        sb.blocks.extend(self.blocks)
        sb.blocks.extend(self._process_blocks(blocks))
        return sb

    def when_dom_ready(self, *blocks):
        sb = ScriptBuilder("document.addEventListener('DOMContentLoaded', function() {")
        sb.blocks.extend(self._process_blocks(blocks))
        sb.blocks.append("});")
        return sb

    def on_click(self, selector, *blocks):
        sb = ScriptBuilder(f"document.querySelector('{selector}').addEventListener('click', function() {{")
        sb.blocks.extend(self._process_blocks(blocks))
        sb.blocks.append("});")
        return sb

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
        return rules

    def _process_blocks_with_indent(self, blocks, indent="    "):
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
        cb = CSSBuilder()
        cb.blocks.extend(self.blocks)
        for block in blocks:
            if isinstance(block, CSSBuilder):
                cb.blocks.extend(block.blocks)
            elif isinstance(block, dict):
                cb.blocks.append(self._format_rules(block))
            else:
                cb.blocks.append(str(block))
        return cb

    def __getattr__(self, selector: str):
        def selector_method(rules=None, **kwargs):
            if rules is None:
                rules = kwargs
            if '__' in selector:
                parts = selector.split('__')
                base_selector = parts[0]
                pseudo = parts[1]
                return CSSBuilder(f'{base_selector}:{pseudo}', rules)
            return CSSBuilder(selector, rules)
        return selector_method

    def nest(self, selector, *blocks):
        nested = CSSBuilder()
        nested.blocks.append(f"{selector} {{")
        nested.blocks.extend(self._process_blocks_with_indent(blocks))
        nested.blocks.append("}")
        return nested

    def mixin(self, name, rules=None, **kwargs):
        if rules is None:
            rules = kwargs
        self._mixins[name] = rules
        return self

    def use_mixin(self, name):
        if name in self._mixins:
            return CSSBuilder(rules=self._mixins[name])
        return CSSBuilder()

    def media(self, query, *blocks):
        media_block = CSSBuilder()
        media_block.blocks.append(f"@media {query} {{")
        media_block.blocks.extend(self._process_blocks_with_indent(blocks))
        media_block.blocks.append("}")
        return media_block

    def keyframes(self, name, *frames):
        kf = CSSBuilder()
        kf.blocks.append(f"@keyframes {name} {{")
        for frame in frames:
            if isinstance(frame, dict) and len(frame) == 1:
                key, rules = next(iter(frame.items()))
                kf.blocks.append(f"    {key} {{")
                kf.blocks.append("        " + self._format_rules(rules))
                kf.blocks.append("    }")
        kf.blocks.append("}")
        return kf

    def variable(self, name, value):
        return CSSBuilder(rules={f'--{name}': value})

    def __add__(self, other):
        if isinstance(other, CSSBuilder):
            combined = CSSBuilder()
            combined.blocks.extend(self.blocks)
            combined.blocks.extend(other.blocks)
            return combined
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
                    elif hasattr(child, '__call__'):
                        result = child()
                        if isinstance(result, ScriptBuilder):
                            sb.blocks.extend(result.blocks)
                    else:
                        sb.blocks.append(str(child))
                return HTMLElement('script', sb, **attrs)
            return script_builder
        elif tag == 'style':
            def style_builder(*children, **attrs):
                cb = CSSBuilder()
                for child in children:
                    if isinstance(child, CSSBuilder):
                        cb.blocks.extend(child.blocks)
                    elif isinstance(child, str):
                        cb.blocks.append(child)
                    elif hasattr(child, '__call__'):
                        result = child()
                        if isinstance(result, CSSBuilder):
                            cb.blocks.extend(result.blocks)
                return HTMLElement('style', cb, **attrs)
            return style_builder
        return lambda *children, **attrs: HTMLElement(tag, *children, **attrs)

html = HTMLBuilder()

class BlockBuilder:
    def __getattr__(self, name: str):
        def block_method(*args, **kwargs):
            return getattr(ScriptBuilder(), name)(*args, **kwargs)
        return block_method

blocks = BlockBuilder()

class CSSBlockBuilder:
    HTML_ELEMENTS = {'body', 'html', 'head', 'div', 'span', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                     'a', 'button', 'input', 'form', 'table', 'tr', 'td', 'th', 'ul', 'ol', 'li',
                     'img', 'video', 'audio', 'canvas', 'svg', 'path', 'circle', 'rect', 'nav'}

    PSEUDO_SELECTORS = {'hover', 'focus', 'visited', 'link', 'before', 'after', 'first-child',
                       'last-child', 'nth-child', 'disabled', 'checked', 'required', 'invalid', 'valid'}

    COMBINED_CLASS_MODIFIERS = {'active', 'disabled', 'selected', 'current', 'open', 'closed'}

    def _build_complex_selector(self, parts):
        if len(parts) == 1:
            part = parts[0]
            return part if part in self.HTML_ELEMENTS else f'.{part.replace("_", "-")}'

        if len(parts) == 2:
            return self._build_two_part_selector(*parts)

        if len(parts) == 3:
            return self._build_three_part_selector(*parts)

        # Recursive case for more than 3 parts
        first, *rest = parts
        base_sel = first if first in self.HTML_ELEMENTS else f'.{first.replace("_", "-")}'
        remaining = self._build_complex_selector(rest)

        if remaining.startswith('.'):
            return f'{base_sel} {remaining}' if first in self.HTML_ELEMENTS else f'{base_sel}{remaining}'
        return f'{base_sel} {remaining}'

    def _build_two_part_selector(self, first, second):
        base_sel = first if first in self.HTML_ELEMENTS else f'.{first.replace("_", "-")}'

        if second in self.PSEUDO_SELECTORS:
            return f'{base_sel}:{second}'
        elif second in self.HTML_ELEMENTS:
            return f'{base_sel} {second}'
        elif second in self.COMBINED_CLASS_MODIFIERS and first not in self.HTML_ELEMENTS:
            return f'{base_sel}.{second.replace("_", "-")}'
        else:
            return f'{base_sel} .{second.replace("_", "-")}'

    def _build_three_part_selector(self, first, second, third):
        base_sel = first if first in self.HTML_ELEMENTS else f'.{first.replace("_", "-")}'
        child_sel = second if second in self.HTML_ELEMENTS else f'.{second.replace("_", "-")}'

        if third in self.PSEUDO_SELECTORS:
            return f'{base_sel} {child_sel}:{third}'
        elif third in self.HTML_ELEMENTS:
            return f'{base_sel} {child_sel} {third}'
        elif (third in self.COMBINED_CLASS_MODIFIERS and
              first not in self.HTML_ELEMENTS and second not in self.HTML_ELEMENTS):
            return f'{base_sel} {child_sel}.{third.replace("_", "-")}'
        else:
            return f'{base_sel} {child_sel} .{third.replace("_", "-")}'

    def _create_selector_function(self, selector):
        def selector_func(rules=None, **kwargs):
            if rules is None:
                rules = kwargs
            return CSSBuilder(selector, rules)
        return selector_func

    def __getattr__(self, name: str):
        if '__' in name:
            parts = name.split('__')
            selector = self._build_complex_selector(parts)
            return self._create_selector_function(selector)

        if name in self.HTML_ELEMENTS:
            return self._create_selector_function(name)

        # Class selector
        selector = f'.{name.replace("_", "-")}'
        return self._create_selector_function(selector)

css = CSSBlockBuilder()

