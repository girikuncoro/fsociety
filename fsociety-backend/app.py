from flask import Flask, abort, json, request
from flask_cors import CORS, cross_origin
from util.flask_common import (
    jsonify,
    enable_json_error,
    ensure_param
)
import re
from twitter import *
from util.twitter import (
    clean,
    get_paragraph
)

from dummy_data import dummy_data

# Default paragraph count
DEFAULT_COUNT = 5

app = Flask(__name__)
CORS(app)

# Load Twitter credentials
config = {}
execfile("config.py", config)

twitter = Twitter(
    auth = OAuth(config["access_key"], config["access_secret"], config["consumer_key"], config["consumer_secret"]))


@app.route('/')
def hello_world():
    return 'Hello world! This is to test fsociety'

@app.route('/api/v1/data', methods=['POST'])
@ensure_param('raw_content')
def preprocess_data():
    return 'Preprocess should work here'

@app.route('/api/v1/paragraph/dummy', methods=['POST'])
@ensure_param('query')
@jsonify
def paragraph_dummy():
    paragraph_count = DEFAULT_COUNT
    if 'paragraph_count' in request.form:
        paragraph_count = request.form['paragraph_count']

    return {
        'data': dummy_data,
        'query': request.form['query'],
        'paragraph_count': paragraph_count
    }

@app.route('/api/v1/paragraph/twitter', methods=['POST'])
@ensure_param('query')
@jsonify
def paragraph_twitter():
    paragraph_count = DEFAULT_COUNT
    if 'paragraph_count' in request.form:
        paragraph_count = int(request.form['paragraph_count'])

    query = request.form['query']
    # Fetch query from Twitter search API
    data = twitter.search.tweets(
        q="{} AND -filter:retweets".format(query), count=100, lang="en")
    cleaned_data = clean(data['statuses'])

    return {
        'data': get_paragraph(
            count=paragraph_count, tweets=cleaned_data),
        'query': query,
        'paragraph_count': paragraph_count
    }

@app.route('/api/v1/paragraph/reuters', methods=['POST'])
@ensure_param('query')
@jsonify
def paragraph_reuters():
    paragraph_count = DEFAULT_COUNT
    if 'paragraph_count' in request.form:
        paragraph_count = int(request.form['paragraph_count'])

    query = request.form['query']
    # Fetch query from topic modelling
    data = twitter.search.tweets(
        q="{} AND -filter:retweets".format(query), count=100, lang="en")
    cleaned_data = clean(data['statuses'])

    return {
        'data': get_paragraph(
            count=paragraph_count, tweets=cleaned_data),
        'query': query,
        'paragraph_count': paragraph_count
    }

@app.errorhandler(400)
def page_not_found(error):
    return json.jsonify({'error': error.description}), error.code

if __name__ == "__main__":
    app.run()