import os
from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.extensions import db
from app.models import ComisionCargo, Documento
from app.utils.decorators import roles_required
from . import bp


@bp.route('/comision')
@login_required
def comision():
    cargos = ComisionCargo.query.order_by(ComisionCargo.orden.asc(), ComisionCargo.id.asc()).all()
    if not cargos:
        datos = [
            {'cargo': 'Presidente', 'tipo': 'presidencia', 'integrantes': 'Tomás González Zalazar', 'orden': 1},
            {'cargo': 'Vicepresidente', 'tipo': 'presidencia', 'integrantes': 'Santiago González Zalazar', 'orden': 2},
            {'cargo': 'Secretarios General', 'tipo': 'secretaria', 'integrantes': 'Genaro Gilardotti y Facundo Bazan', 'orden': 3},
            {'cargo': 'Secretario de Prensa, Difusión y Tecnología', 'tipo': 'secretaria', 'integrantes': 'Genaro Gilardotti y Juan Abdala', 'orden': 4},
            {'cargo': 'Encargado en Finanzas', 'tipo': 'secretaria', 'integrantes': 'Simón Leonel Campos y Ariadny Valeria Diaz Rodriguez', 'orden': 5},
            {'cargo': 'Encargado en Deportes y Recreación', 'tipo': 'secretaria', 'integrantes': 'Juan Pablo Juncos y Maximo Lujan Guzzi', 'orden': 6},
            {'cargo': 'Encargado en Cultura y Eventos', 'tipo': 'secretaria', 'integrantes': 'Lorenzo Martínez y Miranda Von Eberan Plutman', 'orden': 7},
            {'cargo': 'Encargado en Actas', 'tipo': 'secretaria', 'integrantes': 'Elías Gabriel Arce Martínez y Tobias Hürst Altamirano', 'orden': 8},
            {'cargo': 'Organizador de los Equipos de trabajo', 'tipo': 'equipo', 'integrantes': 'Stefano Sarzotti', 'orden': 9},
            {'cargo': 'Comunicación y Diseño', 'tipo': 'equipo', 'integrantes': '', 'orden': 10},
            {'cargo': 'Proyectos y Participación', 'tipo': 'equipo', 'integrantes': 'Lautaro Valentín Allende', 'orden': 11},
            {'cargo': 'Convivencia y Ciberseguridad', 'tipo': 'equipo', 'integrantes': '', 'orden': 12},
        ]
        for d in datos:
            db.session.add(ComisionCargo(**d))
        db.session.commit()
        cargos = ComisionCargo.query.order_by(ComisionCargo.orden.asc(), ComisionCargo.id.asc()).all()
    return render_template('institucional/comision.html', cargos=cargos)


@bp.route('/comision/editar/<int:id>', methods=['POST'])
@login_required
@roles_required('admin')
def editar_comision(id):
    cargo = ComisionCargo.query.get_or_404(id)
    cargo.integrantes = request.form.get('integrantes') or ''
    db.session.commit()
    flash('Integrantes actualizados correctamente', 'success')
    return redirect(url_for('institucional.comision'))


@bp.route('/documentos')
@login_required
def documentos():
    docs = Documento.query.order_by(Documento.fecha_creacion.desc()).all()
    return render_template('institucional/documentos.html', docs=docs)


@bp.route('/documentos/nuevo', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def nuevo_documento():
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        descripcion = request.form.get('descripcion')
        archivo = request.files.get('archivo')
        if not titulo or not archivo or archivo.filename == '':
            flash('Completá el título y seleccioná un archivo', 'warning')
            return redirect(url_for('institucional.nuevo_documento'))
        filename = secure_filename(archivo.filename)
        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        path = os.path.join(upload_folder, filename)
        archivo.save(path)
        doc = Documento(
            titulo=titulo,
            descripcion=descripcion,
            archivo_path=filename,
            subido_por_id=current_user.id
        )
        db.session.add(doc)
        db.session.commit()
        flash('Documento subido correctamente', 'success')
        return redirect(url_for('institucional.documentos'))
    return render_template('institucional/nuevo_documento.html')


@bp.route('/ayuda')
@login_required
def ayuda():
    faqs = [
        {'pregunta': '¿Cómo postulo un proyecto?', 'respuesta': 'Desde Banco de Proyectos > Postular proyecto, completando todos los campos.'},
        {'pregunta': '¿Cómo veo el presupuesto?', 'respuesta': 'Desde Presupuesto podés ver ingresos, egresos y saldo actual.'},
        {'pregunta': '¿Cómo participo en votaciones?', 'respuesta': 'Cuando hay una votación activa, aparece en Votaciones con la opción "Votar".'},
        {'pregunta': '¿Cómo presento un reclamo?', 'respuesta': 'Desde Reclamos > Nuevo reclamo (solo alumnos).'},
        {'pregunta': '¿Cómo cambio mi contraseña?', 'respuesta': 'Desde Mi perfil > Cambiar contraseña.'},
    ]
    return render_template('institucional/ayuda.html', faqs=faqs)
