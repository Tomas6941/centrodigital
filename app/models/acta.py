from datetime import datetime
from app.extensions import db

class Acta(db.Model):
    __tablename__ = 'actas'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    contenido = db.Column(db.Text)
    archivo_path = db.Column(db.String(255))
    publicado_por_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    publicado_por = db.relationship('User')
    publicado_en = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Acta {self.titulo}>'
