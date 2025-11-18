import hej

@get('/')
def home():
    return html.html(
        html.head(
            html.title('Hej'),
            html.script('''
                document.addEventListener('DOMContentLoaded', function() {
                    const btn = document.querySelector('.btn');

                    btn.addEventListener('click', function() {
                        alert('Button clicked!');
                    });
                });
            ''')
        ),
        html.body(
            html.h1('Hej, World'),
            html.button('Click Me!', class_='btn')
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