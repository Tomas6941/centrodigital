from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from datetime import date
from app.extensions import db
from app.models import Evento
from app.utils.decorators import roles_required
from . import bp


@bp.route('/')
@login_required
def index():
    eventos = Evento.query.order_by(Evento.fecha.asc(), Evento.hora.asc()).all()
    return render_template('calendario/index.html', eventos=eventos)


@bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def nuevo():
    if request.method == 'POST':
        fecha_str = request.form.get('fecha')
        hora_str = request.form.get('hora')
        evento = Evento(
            titulo=request.form.get('titulo'),
            descripcion=request.form.get('descripcion'),
            fecha=date.fromisoformat(fecha_str) if fecha_str else date.today(),
            hora=None,
            lugar=request.form.get('lugar'),
            tipo=request.form.get('tipo') or 'general',
            creado_por_id=current_user.id
        )
        if hora_str:
            from datetime import time
            evento.hora = time.fromisoformat(hora_str)
        db.session.add(evento)
        db.session.commit()
        flash('Evento agregado al calendario', 'success')
        return redirect(url_for('calendario.index'))
    return render_template('calendario/nuevo.html')
