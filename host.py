
from flask import Flask
import lfunction
from flask import request
import json

app = Flask(__name__)

@app.route("/")
def index():
    return lfunction.lambda_editor({}, None)['body']

@app.route("/oembed")
def render():
    return json.dumps(lfunction.lambda_handler({
        # 'pathParameters': {
        #     'markdown': markdown
        # },
        'queryStringParameters': request.args
    }, None)['body'])


if __name__ == "__main__":
    app.debug = True
    app.run()
