
from flask import Flask
import lfunction

app = Flask(__name__)

@app.route("/")
def index():
    return render('')

@app.route("/<markdown>")
def render(markdown):
    return lfunction.lambda_handler({
        'pathParameters': {
            'markdown': markdown
        }
    }, None)['body']


if __name__ == "__main__":
    app.debug = True
    app.run()
