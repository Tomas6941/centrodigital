from datetime import datetime
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Proyecto
from app.utils.decorators import roles_required
from . import bp

@bp.route('/')
@login_required
def index():
    if current_user.has_role('admin'):
        proyectos = Proyecto.query.order_by(Proyecto.fecha_postulacion.desc()).all()
    else:
        proyectos = Proyecto.query.filter_by(postulante_id=current_user.id).order_by(Proyecto.fecha_postulacion.desc()).all()
    return render_template('proyectos/index.html', proyectos=proyectos)

@bp.route('/postular', methods=['GET', 'POST'])
@login_required
@roles_required('alumno')
def postular():
    cursos = ['Primer año', 'Segundo año', 'Tercer año', 'Cuarto año', 'Quinto año', 'Sexto año']
    if request.method == 'POST':
        proyecto = Proyecto(
            titulo=request.form.get('titulo'),
            descripcion=request.form.get('descripcion'),
            objetivo=request.form.get('objetivo'),
            monto_estimado=request.form.get('monto_estimado'),
            curso=request.form.get('curso'),
            postulante_id=current_user.id
        )
        db.session.add(proyecto)
        db.session.commit()
        flash('Proyecto postulado correctamente', 'success')
        return redirect(url_for('proyectos.index'))
    return render_template('proyectos/postular.html', cursos=cursos)

@bp.route('/evaluar/<int:id>', methods=['POST'])
@login_required
@roles_required('admin')
def evaluar(id):
    proyecto = Proyecto.query.get_or_404(id)
    accion = request.form.get('accion')
    motivo = request.form.get('motivo')
    if accion == 'aprobar':
        proyecto.estado = 'aprobado'
    elif accion == 'rechazar':
        proyecto.estado = 'rechazado'
    elif accion == 'evaluacion':
        proyecto.estado = 'en evaluación'
    proyecto.motivo = motivo
    proyecto.evaluado_por_id = current_user.id
    proyecto.fecha_evaluacion = datetime.utcnow()
    db.session.commit()
    flash('Proyecto evaluado correctamente', 'success')
    return redirect(url_for('proyectos.index'))
