from datetime import datetime
from app.extensions import db

class Proyecto(db.Model):
    __tablename__ = 'proyectos'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    objetivo = db.Column(db.Text, nullable=False)
    monto_estimado = db.Column(db.Numeric(10, 2), nullable=False)
    curso = db.Column(db.String(20), nullable=False)
    postulante_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    estado = db.Column(db.String(20), default='presentado')  # presentado, en evaluación, aprobado, rechazado, en ejecución, finalizado
    motivo = db.Column(db.Text)
    evaluado_por_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    evaluado_por = db.relationship('User', foreign_keys=[evaluado_por_id])
    fecha_postulacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_evaluacion = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<Proyecto {self.titulo}>'
