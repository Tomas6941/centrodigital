from datetime import datetime
from app.extensions import db


class Evento(db.Model):
    __tablename__ = 'eventos'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text)
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time)
    lugar = db.Column(db.String(150))
    tipo = db.Column(db.String(50), default='general')
    creado_por_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    creado_por = db.relationship('User', backref='eventos')
