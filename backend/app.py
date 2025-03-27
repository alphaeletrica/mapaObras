from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Configuração Async
    db_url = os.environ['DATABASE_URL'].replace('postgres://', 'postgresql+asyncpg://')
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'pool_size': 5,
        'max_overflow': 10,
        'pool_timeout': 30
    }
    
    CORS(app)
    db.init_app(app)
    
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            app.logger.error(f"Erro ao conectar ao PostgreSQL: {str(e)}")
            raise

    from backend.routes import tecnico_bp
    app.register_blueprint(tecnico_bp)
    
    return app