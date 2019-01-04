
import base64
import markdown
import markdown.extensions.extra

def lambda_handler(evt, context):
    markdownSource = ''
    try:
        markdownSource = base64.urlsafe_b64decode(evt['pathParameters']['markdown']).decode("utf-8")
    except Exception as e:
        pass
    if len(markdownSource) == 0:
        return lambda_editor()
    markdownHtml = markdown.markdown(markdownSource, extensions=['extra'])
    return {
        'statusCode': 200,
        'headers': {
            "content-type": "text/html",
            "Access-Control-Allow-Origin": "*"
        },
        'body': '''<!doctype html>

        <html lang="en">
        <head>
          <meta charset="utf-8">
          <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/foundation/6.5.1/css/foundation.min.css">
        </head><body>''' + markdownHtml + '''</body></html>'''
    }

def lambda_editor():
    with open('index.html') as indexFile:
        return {
            'statusCode': 200,
            'headers': {
                "content-type": "text/html",
                "Access-Control-Allow-Origin": "*"
            },
            'body': indexFile.read()
        }
