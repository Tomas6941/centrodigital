from datetime import datetime
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Reclamo
from app.utils.decorators import roles_required
from . import bp

@bp.route('/')
@login_required
def index():
    if current_user.has_role('admin'):
        reclamos = Reclamo.query.order_by(Reclamo.fecha_creacion.desc()).all()
    else:
        reclamos = Reclamo.query.filter_by(autor_id=current_user.id).order_by(Reclamo.fecha_creacion.desc()).all()
    return render_template('reclamos/index.html', reclamos=reclamos)

@bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
@roles_required('alumno')
def nuevo():
    if request.method == 'POST':
        reclamo = Reclamo(
            autor_id=current_user.id,
            asunto=request.form.get('asunto'),
            descripcion=request.form.get('descripcion')
        )
        db.session.add(reclamo)
        db.session.commit()
        flash('Reclamo enviado correctamente', 'success')
        return redirect(url_for('reclamos.index'))
    return render_template('reclamos/nuevo.html')

@bp.route('/responder/<int:id>', methods=['POST'])
@login_required
@roles_required('admin')
def responder(id):
    reclamo = Reclamo.query.get_or_404(id)
    reclamo.respuesta = request.form.get('respuesta')
    reclamo.estado = request.form.get('estado')
    reclamo.respondido_por_id = current_user.id
    reclamo.fecha_respuesta = datetime.utcnow()
    db.session.commit()
    flash('Reclamo actualizado correctamente', 'success')
    return redirect(url_for('reclamos.index'))
