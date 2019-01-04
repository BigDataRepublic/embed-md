
from flask import Flask
import lfunction
from flask import request
import json

app = Flask(__name__)

@app.route("/")
def index():
    return lfunction.lambda_handler({'path': '/'}, None)['body']

@app.route("/<markdown>")
def html(markdown):
    return lfunction.lambda_handler({'path': '/' + markdown, 'pathParameters': {'markdown': markdown}}, None)['body']

@app.route("/oembed")
def render():
    return json.dumps(lfunction.lambda_handler({
        'path': '/oembed',
        'queryStringParameters': request.args
    }, None)['body'])


if __name__ == "__main__":
    app.debug = True
    app.run()
