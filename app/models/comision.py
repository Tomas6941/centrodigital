from app.extensions import db


class ComisionCargo(db.Model):
    __tablename__ = 'comision_cargos'

    id = db.Column(db.Integer, primary_key=True)
    cargo = db.Column(db.String(200), nullable=False)
    tipo = db.Column(db.String(30), nullable=False, default='secretaria')  # presidencia | secretaria | equipo
    integrantes = db.Column(db.Text, nullable=True)
    orden = db.Column(db.Integer, default=0)
