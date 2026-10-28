from datetime import datetime
from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app.extensions import db
from app.models import PresupuestoMovimiento
from app.utils.decorators import roles_required
from app.utils.helpers import save_file
from . import bp

@bp.route('/')
@login_required
def index():
    movimientos = PresupuestoMovimiento.query.order_by(PresupuestoMovimiento.fecha.desc()).all()
    ingresos = sum(m.monto for m in movimientos if m.tipo == 'ingreso')
    egresos = sum(m.monto for m in movimientos if m.tipo == 'egreso')
    saldo = ingresos - egresos
    return render_template('presupuesto/index.html', movimientos=movimientos, ingresos=ingresos, egresos=egresos, saldo=saldo)

@bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
@roles_required('admin', 'tesorero')
def nuevo():
    if request.method == 'POST':
        tipo = request.form.get('tipo')
        concepto = request.form.get('concepto')
        monto = request.form.get('monto')
        fecha = request.form.get('fecha')
        observacion = request.form.get('observacion')
        file = request.files.get('comprobante')
        
        comprobante = save_file(file) if file else None
        
        movimiento = PresupuestoMovimiento(
            tipo=tipo,
            concepto=concepto,
            monto=monto,
            fecha=datetime.strptime(fecha, '%Y-%m-%d').date(),
            observacion=observacion,
            comprobante_path=comprobante,
            cargado_por_id=current_user.id
        )
        db.session.add(movimiento)
        db.session.commit()
        flash('Movimiento registrado correctamente', 'success')
        return redirect(url_for('presupuesto.index'))
    return render_template('presupuesto/nuevo.html')
