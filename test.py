import hej

@get('/')
def home():
    return html.html(
        html.head(
            html.title('Hej')
        ),
        html.body(
            html.h1('Hej, World')
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