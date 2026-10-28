from datetime import datetime
from app.extensions import db

class Votacion(db.Model):
    __tablename__ = 'votaciones'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text)
    fecha_inicio = db.Column(db.DateTime, nullable=False)
    fecha_fin = db.Column(db.DateTime, nullable=False)
    activa = db.Column(db.Boolean, default=True)
    creada_por_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    creada_por = db.relationship('User')
    creada_en = db.Column(db.DateTime, default=datetime.utcnow)
    opciones = db.relationship('VotacionOpcion', backref='votacion', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Votacion {self.titulo}>'

class VotacionOpcion(db.Model):
    __tablename__ = 'votacion_opciones'
    id = db.Column(db.Integer, primary_key=True)
    votacion_id = db.Column(db.Integer, db.ForeignKey('votaciones.id'), nullable=False)
    proyecto_id = db.Column(db.Integer, db.ForeignKey('proyectos.id'), nullable=False)
    proyecto = db.relationship('Proyecto')
    votos = db.relationship('Voto', backref='opcion', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Opcion {self.proyecto_id}>'

class Voto(db.Model):
    __tablename__ = 'votos'
    id = db.Column(db.Integer, primary_key=True)
    votacion_id = db.Column(db.Integer, db.ForeignKey('votaciones.id'), nullable=False)
    opcion_id = db.Column(db.Integer, db.ForeignKey('votacion_opciones.id'), nullable=False)
    votante_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    votante = db.relationship('User')
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    __table_args__ = (db.UniqueConstraint('votacion_id', 'votante_id', name='unique_voto_por_usuario'),)
    
    def __repr__(self):
        return f'<Voto {self.votante_id}>'
