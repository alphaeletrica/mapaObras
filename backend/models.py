from backend.app import db

class Tecnico(db.Model):
    __tablename__ = 'tecnicos'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cidade = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.String(2), nullable=False)
    empresa = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    raio_cobertura = db.Column(db.Integer, default=400)
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}