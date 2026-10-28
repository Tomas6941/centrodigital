from datetime import datetime
from app.extensions import db

class PresupuestoMovimiento(db.Model):
    __tablename__ = 'presupuesto_movimientos'
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(10), nullable=False)  # ingreso o egreso
    concepto = db.Column(db.String(200), nullable=False)
    monto = db.Column(db.Numeric(10, 2), nullable=False)
    fecha = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    comprobante_path = db.Column(db.String(255))
    observacion = db.Column(db.Text)
    cargado_por_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    cargado_por = db.relationship('User', backref='movimientos_cargados')
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Movimiento {self.tipo} {self.monto}>'
