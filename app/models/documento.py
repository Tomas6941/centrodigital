from datetime import datetime
from app.extensions import db


class Documento(db.Model):
    __tablename__ = 'documentos'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text)
    archivo_path = db.Column(db.String(255), nullable=False)
    subido_por_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    subido_por = db.relationship('User', backref='documentos')
