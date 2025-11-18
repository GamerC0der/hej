import hej

@get('/')
def home():
    return html.html(
        html.head(
            html.title('Hej'),
            html.style("""
                body {
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 40px;
                    text-align: center;
                }
                h1 {
                    margin-bottom: 40px;
                }
                .buttons {
                    display: flex;
                    gap: 20px;
                    justify-content: center;
                }
                button {
                    padding: 10px 20px;
                    font-size: 16px;
                    cursor: pointer;
                }
            """)
        ),
        html.body(
            html.h1('Hej, World!'),
            html.div(
                html.button('Download Hej'),
                html.button('View Docs', onclick="window.location.href='/docs'"),
                class_='buttons'
            )
        )
    ) 

@get('/docs')
def docs():
    return html.html(
        html.head(
            html.title('Hej Docs'),
            html.style("""
                body { font-family: Arial; padding: 20px; }
                .step { background: #f5f5f5; padding: 15px; margin: 20px 0; }
                .code { background: #f0f0f0; padding: 10px; font-family: monospace; }
                h1 { text-align: center; margin-bottom: 30px; }
            """)
        ),
        html.body(
            html.h1('Build Your First Website with Hej'),
            html.div(
                html.h2('Step 1: Create Your App File'),
                html.p('Create a new Python file called app.py:'),
                html.pre('import hej', class_='code'),
                class_='step'
            ),
            html.div(
                html.h2('Step 2: Add a Home Route'),
                html.p('Use the @get decorator to create your first page:'),
                html.pre('@get(\'/\')\ndef home():\n    return html.html(\n        html.head(html.title(\'My Site\')),\n        html.body(html.h1(\'Welcome!\'))\n    )', class_='code'),
                class_='step'
            ),
            html.div(
                html.h2('Step 3: Build HTML with the html Builder'),
                html.p('The html object lets you create HTML elements:'),
                html.pre('html.div(\n    html.h1(\'My Title\'),\n    html.p(\'Some text here\'),\n    html.button(\'Click Me\')\n)', class_='code'),
                html.p('Add attributes with keyword arguments:'),
                html.pre('html.button(\'Click Me\', onclick=\'alert("Hello!")\', class_=\'btn\')', class_='code'),
                class_='step'
            ),
            html.div(
                html.h2('Step 4: Add More Routes'),
                html.p('Create additional pages:'),
                html.pre('@get(\'/about\')\ndef about():\n    return html.html(\n        html.head(html.title(\'About\')),\n        html.body(\n            html.h1(\'About Us\'),\n            html.p(\'We build awesome websites!\')\n        )\n    )', class_='code'),
                class_='step'
            ),
            html.div(
                html.h2('Step 5: Add CSS Styling'),
                html.p('Add styles directly in your HTML:'),
                html.pre('html.style("""\n    body { font-family: Arial; }\n    .btn { padding: 10px; }\n""")', class_='code'),
                class_='step'
            ),
            html.div(
                html.h2('Step 6: Run Your Site'),
                html.p('Add this at the end of your file:'),
                html.pre('if __name__ == \'__main__\':\n    hej.run()', class_='code'),
                html.div(
                    html.p('Run with: python app.py'),
                    class_='note'
                ),
                class_='step'
            ),
            html.div(
                html.h2('Step 7: Add JavaScript'),
                html.p('Use the blocks builder for client-side code:'),
                html.pre('html.script(\n    blocks.when_dom_ready(\n        blocks.alert(\'Page loaded!\')\n    )\n)', class_='code'),
                class_='step'
            ),
            html.div(
                html.h2('Complete Example'),
                html.pre('import hej\n\n@get(\'/\')\ndef home():\n    return html.html(\n        html.head(\n            html.title(\'My Site\'),\n            html.style("""\n                body { font-family: Arial; text-align: center; padding: 50px; }\n            """)\n        ),\n        html.body(\n            html.h1(\'Welcome to My Site!\'),\n            html.p(\'This is my first Hej website.\')\n        )\n    )\n\nif __name__ == \'__main__\':\n    hej.run()', class_='code'),
                class_='step'
            )
        )
    )

@not_found
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

if __name__ == '__main__':
    hej.run(debug=True)