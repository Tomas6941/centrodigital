from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Comunicado
from app.utils.decorators import roles_required
from . import bp


@bp.route('/')
@login_required
def index():
    comunicados = Comunicado.query.order_by(Comunicado.destacado.desc(), Comunicado.fecha_creacion.desc()).all()
    return render_template('comunicados/index.html', comunicados=comunicados)


@bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def nuevo():
    if request.method == 'POST':
        comunicado = Comunicado(
            titulo=request.form.get('titulo'),
            contenido=request.form.get('contenido'),
            destacado=bool(request.form.get('destacado')),
            autor_id=current_user.id
        )
        db.session.add(comunicado)
        db.session.commit()
        flash('Comunicado publicado correctamente', 'success')
        return redirect(url_for('comunicados.index'))
    return render_template('comunicados/nuevo.html')
