from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello world! This is to test fsociety'


@app.route('/api/v1/data', methods=['POST'])
def preprocess_data():
    return 'Preprocess should work here'


@app.route('/api/v1/paragraph', methods=['GET'])
def paragraph():
    return 'this should work for paragraph'


if __name__ == "__main__":
    app.run()