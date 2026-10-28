from datetime import datetime
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Votacion, VotacionOpcion, Voto, Proyecto
from app.utils.decorators import roles_required
from . import bp

@bp.route('/')
@login_required
def index():
    votaciones = Votacion.query.order_by(Votacion.fecha_inicio.desc()).all()
    return render_template('votaciones/index.html', votaciones=votaciones)

@bp.route('/nueva', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def nueva():
    proyectos_aprobados = Proyecto.query.filter_by(estado='aprobado').all()
    if request.method == 'POST':
        votacion = Votacion(
            titulo=request.form.get('titulo'),
            descripcion=request.form.get('descripcion'),
            fecha_inicio=datetime.strptime(request.form.get('fecha_inicio'), '%Y-%m-%dT%H:%M'),
            fecha_fin=datetime.strptime(request.form.get('fecha_fin'), '%Y-%m-%dT%H:%M'),
            creada_por_id=current_user.id
        )
        db.session.add(votacion)
        db.session.flush()
        proyectos_seleccionados = request.form.getlist('proyectos')
        for pid in proyectos_seleccionados:
            opcion = VotacionOpcion(votacion_id=votacion.id, proyecto_id=pid)
            db.session.add(opcion)
        db.session.commit()
        flash('Votación creada correctamente', 'success')
        return redirect(url_for('votaciones.index'))
    return render_template('votaciones/nueva.html', proyectos=proyectos_aprobados)

@bp.route('/votar/<int:id>', methods=['GET', 'POST'])
@login_required
@roles_required('alumno')
def votar(id):
    votacion = Votacion.query.get_or_404(id)
    ahora = datetime.utcnow()
    if ahora < votacion.fecha_inicio or ahora > votacion.fecha_fin or not votacion.activa:
        flash('Esta votación no está activa', 'warning')
        return redirect(url_for('votaciones.index'))
    voto_existente = Voto.query.filter_by(votacion_id=votacion.id, votante_id=current_user.id).first()
    if voto_existente:
        flash('Ya votaste en esta votación', 'warning')
        return redirect(url_for('votaciones.index'))
    if request.method == 'POST':
        opcion_id = request.form.get('opcion')
        voto = Voto(votacion_id=votacion.id, opcion_id=opcion_id, votante_id=current_user.id)
        db.session.add(voto)
        db.session.commit()
        flash('Voto registrado correctamente', 'success')
        return redirect(url_for('votaciones.index'))
    return render_template('votaciones/votar.html', votacion=votacion)

@bp.route('/resultados/<int:id>')
@login_required
def resultados(id):
    votacion = Votacion.query.get_or_404(id)
    resultados = []
    for opcion in votacion.opciones:
        count = Voto.query.filter_by(opcion_id=opcion.id).count()
        resultados.append({'opcion': opcion, 'votos': count, 'proyecto': opcion.proyecto})
    resultados.sort(key=lambda x: x['votos'], reverse=True)
    return render_template('votaciones/resultados.html', votacion=votacion, resultados=resultados)
