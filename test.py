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
                html.button('View Docs'),
                class_='buttons'
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