from backend.app import create_app
from werkzeug.wsgi import DispatcherMiddleware

app = create_app()

def handler(event, context):
    with app.app_context():
        from werkzeug.test import EnvironBuilder
        
        builder = EnvironBuilder(
            path=event['path'],
            method=event['httpMethod'],
            headers=event.get('headers', {}),
            data=event.get('body', '')
        )
        
        env = builder.get_environ()
        response = app(env, lambda *args: None)
        
        return {
            'statusCode': response.status_code,
            'headers': dict(response.headers),
            'body': response.data.decode('utf-8')
        }