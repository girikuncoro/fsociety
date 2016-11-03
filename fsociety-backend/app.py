from flask import Flask, abort, json, request
from util.flask_common import (
    jsonify,
    enable_json_error,
    ensure_param
)
from dummy_data import dummy_data

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello world! This is to test fsociety'

@app.route('/api/v1/data', methods=['POST'])
@ensure_param('raw_content')
def preprocess_data():
    return 'Preprocess should work here'

@app.route('/api/v1/paragraph', methods=['POST'])
@ensure_param('query')
@jsonify
def paragraph():
    paragraph_count = 15  # default count
    if 'paragraph_count' in request.form:
        paragraph_count = request.form['paragraph_count']

    return {
        'data': dummy_data,
        'query': request.form['query'],
        'paragraph_count': paragraph_count
    }

@app.errorhandler(400)
def page_not_found(error):
    return json.jsonify({'error': error.description}), error.code

if __name__ == "__main__":
    app.run()