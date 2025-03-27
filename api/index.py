from backend.app import create_app
from flask import request

app = create_app()

async def handler(event, context):
    with app.test_request_context(
        path=event['path'],
        method=event['httpMethod'],
        headers=event.get('headers', {}),
        data=event.get('body', '')
    ):
        response = await app.full_dispatch_request()
        return {
            'statusCode': response.status_code,
            'headers': dict(response.headers),
            'body': response.get_data(as_text=True)
        }