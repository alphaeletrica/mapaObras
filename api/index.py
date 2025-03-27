from backend.app import create_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.test import EnvironBuilder

app = create_app()

def handler(event, context):
    with app.app_context():
        # Converte o evento do Vercel para ambiente WSGI
        builder = EnvironBuilder(
            path=event['path'],
            method=event['httpMethod'],
            headers=event.get('headers', {}),
            data=event.get('body', '')
        )
        
        env = builder.get_environ()
        
        # Cria uma resposta dummy para capturar a saída
        def start_response(status, headers, exc_info=None):
            pass
        
        # Executa a aplicação
        response = app(env, start_response)
        
        return {
            'statusCode': 200,
            'headers': dict(headers),
            'body': response[0].decode('utf-8') if response else ''
        }