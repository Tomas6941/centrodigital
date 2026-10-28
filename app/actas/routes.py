from datetime import datetime
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Acta
from app.utils.decorators import roles_required
from app.utils.helpers import save_file
from . import bp

@bp.route('/')
@login_required
def index():
    actas = Acta.query.order_by(Acta.fecha.desc()).all()
    return render_template('actas/index.html', actas=actas)

@bp.route('/nueva', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def nueva():
    if request.method == 'POST':
        file = request.files.get('archivo')
        archivo = save_file(file) if file else None
        acta = Acta(
            titulo=request.form.get('titulo'),
            fecha=datetime.strptime(request.form.get('fecha'), '%Y-%m-%d').date(),
            contenido=request.form.get('contenido'),
            archivo_path=archivo,
            publicado_por_id=current_user.id
        )
        db.session.add(acta)
        db.session.commit()
        flash('Acta publicada correctamente', 'success')
        return redirect(url_for('actas.index'))
    return render_template('actas/nueva.html')
