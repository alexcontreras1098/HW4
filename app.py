from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "hello world"

@app.route('/Alex')
def Alex():
    return "heyo mi amigo"


if __name__ == '__main__':
    app.run(debug=True)
