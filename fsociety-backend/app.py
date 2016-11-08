from flask import Flask, abort, json, request
from flask_cors import CORS, cross_origin
from util.flask_common import (
    jsonify,
    enable_json_error,
    ensure_param
)
import re
# Twitter data fetcher
from twitter import *
from util.twitter import (
    clean,
    get_paragraph
)

# Dummy data fetcher
from dummy_data import dummy_data
# Reddit data fetcher
from f_aggr import GetArticleText
# Reuters data fetcher
#from search.src.scripts.semantic_search import get_ids
#from util.reuters import get_reuters_paragraph

# Default paragraph count
DEFAULT_COUNT = 5

app = Flask(__name__)
CORS(app)

# Load Twitter credentials
config = {}
execfile("/app/fsociety-backend/config.py", config)

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
"""
@app.route('/api/v1/paragraph/reuters', methods=['POST'])
@ensure_param('query')
@jsonify
def paragraph_reuters():
    paragraph_count = DEFAULT_COUNT
    if 'paragraph_count' in request.form:
        paragraph_count = int(request.form['paragraph_count'])

    query = request.form['query']
    # Fetch query from topic modelling
    data_ids = get_ids(query)
    # cleaned_data = clean(data['statuses'])

    return {
        'data': get_reuters_paragraph(data_ids, paragraph_count),
        'query': query,
        'paragraph_count': paragraph_count
    }
"""
@app.route('/api/v1/paragraph/reddit', methods=['POST'])
@ensure_param('query')
@jsonify
def paragraph_reddit():
    paragraph_count = DEFAULT_COUNT
    if 'paragraph_count' in request.form:
        paragraph_count = int(request.form['paragraph_count'])

    query = request.form['query']
    # Fetch query from topic modelling
    data = GetArticleText(query, paragraph_count)
    print data

    return {
        'data': data,
        'query': query,
        'paragraph_count': paragraph_count
    }

@app.errorhandler(400)
def page_not_found(error):
    return json.jsonify({'error': error.description}), error.code

if __name__ == "__main__":
    app.run()
