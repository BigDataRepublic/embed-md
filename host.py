
from flask import Flask
import lfunction

app = Flask(__name__)

@app.route("/<markdown>")
def render(markdown):
    return lfunction.render({
        'pathParameters': {
            'markdown': markdown
        }
    }, None)['message']


if __name__ == "__main__":
    app.debug = True
    app.run()
