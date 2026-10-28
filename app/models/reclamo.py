from datetime import datetime
from app.extensions import db

class Reclamo(db.Model):
    __tablename__ = 'reclamos'
    id = db.Column(db.Integer, primary_key=True)
    autor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    asunto = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    estado = db.Column(db.String(20), default='recibido')  # recibido, en proceso, resuelto, cerrado
    respuesta = db.Column(db.Text)
    respondido_por_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    respondido_por = db.relationship('User', foreign_keys=[respondido_por_id])
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_respuesta = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<Reclamo {self.asunto}>'
