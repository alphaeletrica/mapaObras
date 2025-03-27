from backend.app import create_app
from flask import request
import asyncio

app = create_app()

async def handler(event, context):
    with app.app_context():
        # Converte o evento do Vercel para requisição Flask
        path = event['path']
        method = event['httpMethod']
        headers = event.get('headers', {})
        body = event.get('body', '')
        
        with app.test_request_context(path=path, method=method, 
                                    headers=headers, data=body):
            response = app.full_dispatch_request()
            return {
                'statusCode': response.status_code,
                'headers': dict(response.headers),
                'body': response.get_data(as_text=True)
            }