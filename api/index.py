from backend.app import create_app
from flask import Request, Response
import os

app = create_app()

def handler(event, context):
    # Converte o evento do Vercel para requisição Flask
    request = Request({
        'REQUEST_METHOD': event['httpMethod'],
        'PATH_INFO': event['path'],
        'QUERY_STRING': event.get('queryStringParameters', ''),
        'wsgi.input': event.get('body', ''),
        'CONTENT_TYPE': event.get('headers', {}).get('content-type', ''),
        'SERVER_NAME': 'vercel',
        'SERVER_PORT': '443'
    })

    with app.app_context():
        response = app.full_dispatch_request()
        return {
            'statusCode': response.status_code,
            'headers': dict(response.headers),
            'body': response.get_data(as_text=True)
        }