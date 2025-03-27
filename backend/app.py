from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Configuração segura para PostgreSQL
    db_url = os.getenv('DATABASE_URL', '').replace('postgres://', 'postgresql://')
    if not db_url:
        raise RuntimeError("DATABASE_URL não configurada")
    
    app.config.update({
        'SQLALCHEMY_DATABASE_URI': db_url,
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'SQLALCHEMY_ENGINE_OPTIONS': {
            'pool_pre_ping': True,
            'pool_recycle': 300,
            'pool_size': 5,
            'max_overflow': 10
        }
    })
    
    CORS(app)
    db.init_app(app)
    
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            app.logger.error(f"Erro ao inicializar banco: {str(e)}")
            raise

    from backend.routes import tecnico_bp
    app.register_blueprint(tecnico_bp)
    
    return app