
import base64
import markdown
import markdown.extensions.extra
from urllib.parse import unquote

import json

def lambda_handler(evt, context):
    path = evt['path']
    if path.startswith("/oembed"):
        return render_oembed(evt, context)
    elif path == '/':
        return render_editor(evt, context)
    else:
        return render_html(evt, context)
    return {
        'statusCode': 400,
        'body': 'fuuuuuuuuuuuuu'
    }

def render_markdown(inputValue):
    markdownSource = base64.urlsafe_b64decode(inputValue).decode("utf-8")
    markdownHtml = markdown.markdown(markdownSource, extensions=['extra'])
    markdownHtml = markdownHtml.replace("<table>", '<table class="pure-table">')
    return '''<!doctype html>

        <html lang="en">
        <head>
          <meta charset="utf-8">
          <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/pure/1.0.0/pure-min.css">
        </head><body>''' + markdownHtml + '''</body></html>'''

def render_html(evt, context):
    return {
        'statusCode': 200,
        'headers': {
            "Content-Type": "text/html"
        },
        'body': render_markdown(evt['pathParameters']['markdown'])
    }


def render_oembed(evt, context):
    markdownInput = unquote(evt['queryStringParameters']['url']).split("/")[-1]
    format = evt['queryStringParameters'].get('format', '')
    if format == 'xml':
        return {
            'statusCode': 501,
            'body': 'Ehm... No'
        }
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

def render_editor(evt, context):
    with open('index.html') as indexFile:
        return {
            'statusCode': 200,
            'headers': {
                "Content-Type": "text/html"
            },
            'body': indexFile.read()
        }
