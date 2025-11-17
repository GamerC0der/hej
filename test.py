import hej

@get('/')
def home():
    return 'Hello, World!'

@not_found
def custom_404():
    return '<h1> Not Found</h1><p>This page doesn\'t exist!</p>'

if __name__ == '__main__':
    hej.run(debug=True)