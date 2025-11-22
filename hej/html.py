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

class CSSBuilder:
    def __init__(self, selector=None, rules=None):
        self.blocks = []
        if selector and rules:
            self.blocks.append(f"{selector} {{\n{self._format_rules(rules)}\n}}")

    def _format_rules(self, rules):
        if isinstance(rules, dict):
            return '\n'.join(f"    {k}: {v};" for k, v in rules.items())
        return rules

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
    def __getattr__(self, name: str):
        html_elements = {'body', 'html', 'head', 'div', 'span', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 
                        'a', 'button', 'input', 'form', 'table', 'tr', 'td', 'th', 'ul', 'ol', 'li',
                        'img', 'video', 'audio', 'canvas', 'svg', 'path', 'circle', 'rect', 'nav'}
        
        pseudo_selectors = {'hover', 'focus', 'visited', 'link', 'before', 'after', 'first-child', 
                           'last-child', 'nth-child', 'disabled', 'checked', 'required', 'invalid', 'valid'}
        
        combined_class_modifiers = {'active', 'disabled', 'selected', 'current', 'open', 'closed'}
        
        if '__' in name:
            parts = name.split('__')
            
            def build_selector(parts_list):
                if len(parts_list) == 1:
                    part = parts_list[0]
                    if part in html_elements:
                        return part
                    else:
                        return f'.{part.replace("_", "-")}'
                
                if len(parts_list) == 2:
                    first, second = parts_list
                    
                    if first in html_elements:
                        base_sel = first
                    else:
                        base_sel = f'.{first.replace("_", "-")}'
                    
                    if second in pseudo_selectors:
                        return f'{base_sel}:{second}'
                    elif second in html_elements:
                        return f'{base_sel} {second}'
                    elif second in combined_class_modifiers and first not in html_elements:
                        return f'{base_sel}.{second.replace("_", "-")}'
                    else:
                        return f'{base_sel} .{second.replace("_", "-")}'
                
                if len(parts_list) == 3:
                    first, second, third = parts_list
                    
                    if first in html_elements:
                        base_sel = first
                    else:
                        base_sel = f'.{first.replace("_", "-")}'
                    
                    if second in html_elements:
                        child_sel = second
                    else:
                        child_sel = f'.{second.replace("_", "-")}'
                    
                    if third in pseudo_selectors:
                        return f'{base_sel} {child_sel}:{third}'
                    elif third in html_elements:
                        return f'{base_sel} {child_sel} {third}'
                    elif third in combined_class_modifiers and first not in html_elements and second not in html_elements:
                        return f'{base_sel} {child_sel}.{third.replace("_", "-")}'
                    else:
                        return f'{base_sel} {child_sel} .{third.replace("_", "-")}'
                
                first = parts_list[0]
                rest = parts_list[1:]
                
                if first in html_elements:
                    base_sel = first
                else:
                    base_sel = f'.{first.replace("_", "-")}'
                
                remaining = build_selector(rest)
                if remaining.startswith('.'):
                    if first in html_elements:
                        return f'{base_sel} {remaining}'
                    else:
                        return f'{base_sel}{remaining}'
                else:
                    return f'{base_sel} {remaining}'
            
            selector = build_selector(parts)
            
            def nested_selector(rules=None, **kwargs):
                if rules is None:
                    rules = kwargs
                return CSSBuilder(selector, rules)
            return nested_selector
        
        if name in html_elements:
            def element_selector(rules=None, **kwargs):
                if rules is None:
                    rules = kwargs
                return CSSBuilder(name, rules)
            return element_selector
        else:
            def class_selector(rules=None, **kwargs):
                if rules is None:
                    rules = kwargs
                selector = name.replace('_', '-')
                if not selector.startswith('.'):
                    selector = '.' + selector
                return CSSBuilder(selector, rules)
            return class_selector

css = CSSBlockBuilder()

