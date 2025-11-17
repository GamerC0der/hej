import hej

@get('/')
def home():
    return 'Hello, World!'

if __name__ == '__main__':
    hej.run(debug=True)