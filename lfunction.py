import base64
import markdown
import markdown.extensions.extra
from urllib.parse import unquote

import json
import zlib


def lambda_handler(evt, context):
    path = evt['path']
    if path.startswith("/oembed"):
        return render_oembed(evt, context)
    elif path.startswith("/m/"):
        return render_html(evt, context)
    elif path == '/':
        return render_editor(evt, context)

    return {
        'statusCode': 404,
        'body': '<html><body style="text-align:center; font-size: 500; font-family: cursive">404<br />not found</body></html>'
    }


def render_markdown(inputValue, max_height, max_width):
    height = 600
    width = 600

    if max_height is not None and max_height < height:
        height = max_height
    if max_width is not None and max_width < width:
        width = max_width

    markdownSource = zlib.decompress(base64.urlsafe_b64decode(inputValue), wbits=15).decode('utf-8')
    markdownHtml = markdown.markdown(markdownSource, extensions=['extra'])
    markdownHtml = markdownHtml.replace("<table>", '<table class="pure-table" height=' + str(height) + ' width=' + str(width) + '>')
    return '''<!doctype html>

        <html lang="en">
        <head>
          <meta charset="utf-8">
          <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/pure/1.0.0/pure-min.css">
          <link rel="alternate" type="application/json+oembed" href="https://md.bigdatarepublic.nl/oembed?url=https%3A%2F%2Fmd.bigdatarepublic.nl%2F''' + inputValue + '''&format=json" title="oEmbed" />
        </head><body>''' + markdownHtml + '''</body></html>'''


def render_html(evt, context):
    return {
        'statusCode': 200,
        'headers': {
            "Content-Type": "text/html"
        },
        'body': render_markdown(evt['pathParameters']['markdown'], None, None)
    }


def render_oembed(evt, context):
    markdownInput = unquote(evt['queryStringParameters']['url']).split("/")[-1]
    formatting = evt['queryStringParameters'].get('format', '')
    max_height = evt['queryStringParameters'].get('maxheight', None)
    max_width = evt['queryStringParameters'].get('maxwidth', None)

    if formatting == 'xml':
        return {
            'statusCode': 501,
            'body': 'XML is not supported'
        }
    return {
        'statusCode': 200,
        'headers': {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        'body': json.dumps({
            "version": "1.0",
            "url": evt['queryStringParameters']['url'],
            "type": "rich",
            "html": render_markdown(markdownInput, max_height, max_width),
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
