# Hej

Hej is a simple framework, similar to Flask and FastHTML, in one simple package.

## Supports

- FastHTML Style Syntax
- Templates
- Debug Mode
- CLI
- 404 Pages

& More


## Hej Framework Documentation

#### Quick Start

Create a file called `app.py` and add this code:

```python
import hej
from hej import html, get

@get('/')
def home():
    return html.html(
        html.head(
            html.title('My App')
        ),
        html.body(
            html.h1('Hello, World!'),
            html.p('Welcome to Hej Framework')
        )
    )

if __name__ == '__main__':
    hej.run()
```

Run it with:

```bash
python app.py
```

Visit `http://127.0.0.1:5000` to see your app!

### Adding Routes

Add more routes using decorators:

```python
@get('/about')
def about():
    return html.html(
        html.head(
            html.title('About')
        ),
        html.body(
            html.h1('About Page')
        )
    )
```

### Using Templates

You can return a template file name as a string:

```python
@get('/page')
def page():
    return 'example.html'
```

### 404 Handling

Handle 404 errors with a custom page:

```python
@hej.not_found
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
```
