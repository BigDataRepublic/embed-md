import base64
import markdown
import markdown.extensions.extra
from urllib.parse import unquote

import json
import zlib
from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader(searchpath="./templates"),
    autoescape=select_autoescape(['html', 'xml'])
)


DEFAULT_HEIGHT = 10000
DEFAULT_WIDTH = 600


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


def render_markdown(inputValue, height, width):
    markdownSource = zlib.decompress(base64.urlsafe_b64decode(inputValue), wbits=15).decode('utf-8')
    markdownHtml = markdown.markdown(markdownSource, extensions=['extra'])
    markdownHtml = markdownHtml.replace("<table>", '<table class="pure-table">')
    return env.get_template('markdown_render.html').render(width=width, markdownHtml=markdownHtml, inputValue=inputValue)


def render_html(evt, context):
    return {
        'statusCode': 200,
        'headers': {
            "Content-Type": "text/html",
            "X-Robots-Tag": "noindex"
        },
        'body': render_markdown(evt['pathParameters']['markdown'], DEFAULT_HEIGHT, DEFAULT_WIDTH)
    }


def render_oembed(evt, context):
    markdownInput = unquote(evt['queryStringParameters']['url']).split("/")[-1]
    formatting = evt['queryStringParameters'].get('format', '')

    max_height = None
    max_width = None

    try:
        max_height = int(evt['queryStringParameters'].get('maxheight', None))
        max_width = int(evt['queryStringParameters'].get('maxwidth', None))
    except:
        pass

    height = DEFAULT_HEIGHT
    width = DEFAULT_WIDTH

    if max_height is not None and max_height < height:
        height = max_height
    if max_width is not None and max_width < width:
        width = max_width

    if formatting == 'xml':
        return {
            'statusCode': 501,
            'body': 'XML is not supported'
        }
    return {
        'statusCode': 200,
        'headers': {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "X-Robots-Tag": "noindex"
        },
        'body': json.dumps({
            "version": "1.0",
            "url": evt['queryStringParameters']['url'],
            "type": "rich",
            "html": render_markdown(markdownInput, height, width),
            "width": width,
            "height": height

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


def render_robots_txt(evt, context):
    with open('robots.txt') as indexFile:
        return {
            'statusCode': 200,
            'headers': {
                "Content-Type": "text/plain"
            },
            'body': indexFile.read()
        }
