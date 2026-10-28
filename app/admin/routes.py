from datetime import datetime
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.extensions import db
from app.models import User, Role
from app.utils.decorators import roles_required
from . import bp

@bp.route('/')
@login_required
@roles_required('admin', 'tesorero')
def index():
    return render_template('admin/index.html')

@bp.route('/usuarios')
@login_required
@roles_required('admin')
def usuarios():
    users = User.query.all()
    roles = Role.query.all()
    cursos = ['Primer año', 'Segundo año', 'Tercer año', 'Cuarto año', 'Quinto año', 'Sexto año']
    return render_template('admin/usuarios.html', users=users, roles=roles, cursos=cursos)

@bp.route('/usuarios/crear', methods=['POST'])
@login_required
@roles_required('admin')
def crear_usuario():
    nombre = request.form.get('nombre')
    apellido = request.form.get('apellido')
    email = request.form.get('email')
    curso = request.form.get('curso')
    rol_id = request.form.get('rol_id')
    password = request.form.get('password')
    
    if User.query.filter_by(email=email).first():
        flash('Ya existe un usuario con ese email', 'danger')
        return redirect(url_for('admin.usuarios'))
    
    user = User(nombre=nombre, apellido=apellido, email=email, curso=curso, rol_id=rol_id)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    flash('Usuario creado correctamente', 'success')
    return redirect(url_for('admin.usuarios'))
