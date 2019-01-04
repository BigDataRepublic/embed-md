
import base64
import markdown
import markdown.extensions.extra
from urllib.parse import unquote

import json

def render_markdown(inputValue):
    print(inputValue)
    markdownSource = base64.urlsafe_b64decode(inputValue).decode("utf-8")
    markdownHtml = markdown.markdown(markdownSource, extensions=['extra'])

    return '''<!doctype html>

        <html lang="en">
        <head>
          <meta charset="utf-8">
          <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/foundation/6.5.1/css/foundation.min.css">
        </head><body>''' + markdownHtml + '''</body></html>'''

def lambda_render(evt, context):
    return {
        'statusCode': 200,
        'headers': {
            "Content-Type": "text/html"
        },
        'body': render_markdown(evt['pathParameters']['markdown'])
    }


def lambda_handler(evt, context):
    markdownInput = unquote(evt['queryStringParameters']['url']).split("/")[-1]
    return  {
        'statusCode': 200,
        'headers': {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        'body': json.dumps({
            "version": "1.0",
            "url": evt['queryStringParameters']['url'],
            "type": "rich",
            "html": render_markdown(markdownInput),
            "width": "500",
            "height": "700"

        })
    }

def lambda_editor(evt, context):
    with open('index.html') as indexFile:
        return {
            'statusCode': 200,
            'headers': {
                "Content-Type": "text/html"
            },
            'body': indexFile.read()
        }
