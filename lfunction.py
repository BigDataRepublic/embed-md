
import base64
import markdown
import markdown.extensions.extra

def render(evt, context):
    markdownSource = base64.urlsafe_b64decode(evt['pathParameters']['markdown']).decode("utf-8")
    markdownHtml = markdown.markdown(markdownSource, extensions=['extra'])
    return {
        'message': '''<!doctype html>

        <html lang="en">
        <head>
          <meta charset="utf-8">
          <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/foundation/6.5.1/css/foundation.min.css">
        </head><body>''' + markdownHtml + '''</body></html>'''
    }

try:
    export.handler = render
except Exception as e:
    pass
