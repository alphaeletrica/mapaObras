from werkzeug.wrappers import Request, Response

def wsgi_handler(app, request):
    environ = {
        'REQUEST_METHOD': request['httpMethod'],
        'PATH_INFO': request['path'],
        'QUERY_STRING': request.get('queryStringParameters', ''),
        'SERVER_NAME': 'vercel',
        'SERVER_PORT': '443',
        'wsgi.url_scheme': 'https',
        'wsgi.input': request.get('body', ''),
        'wsgi.errors': None,
        'wsgi.version': (1, 0),
        'wsgi.multithread': False,
        'wsgi.multiprocess': False,
        'wsgi.run_once': False,
    }
    
    with app.request_context(environ):
        response = app.full_dispatch_request()
        return {
            'statusCode': response.status_code,
            'headers': dict(response.headers),
            'body': response.get_data(as_text=True)
        }