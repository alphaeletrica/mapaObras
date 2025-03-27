from backend.app import create_app
from vercel_storage import wsgi_handler  # Importe o handler correto

app = create_app()

def handler(request):
    with app.app_context():
        response = wsgi_handler(app, request)
        return response