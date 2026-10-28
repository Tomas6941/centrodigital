from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.extensions import db
from app.models import User
from . import bp


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password) and user.activo:
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
        flash('Email o contraseña incorrectos', 'danger')
    return render_template('auth/login.html')


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada correctamente', 'success')
    return redirect(url_for('auth.login'))


@bp.route('/perfil')
@login_required
def perfil():
    return render_template('auth/perfil.html')


@bp.route('/cambiar-contrasena', methods=['GET', 'POST'])
@login_required
def cambiar_contrasena():
    if request.method == 'POST':
        actual = request.form.get('actual')
        nueva = request.form.get('nueva')
        confirmar = request.form.get('confirmar')

        if not current_user.check_password(actual):
            flash('La contraseña actual es incorrecta', 'danger')
            return redirect(url_for('auth.cambiar_contrasena'))

        if not nueva or len(nueva) < 6:
            flash('La nueva contraseña debe tener al menos 6 caracteres', 'warning')
            return redirect(url_for('auth.cambiar_contrasena'))

        if nueva != confirmar:
            flash('Las contraseñas no coinciden', 'warning')
            return redirect(url_for('auth.cambiar_contrasena'))

        current_user.set_password(nueva)
        db.session.commit()
        flash('Contraseña actualizada correctamente', 'success')
        return redirect(url_for('auth.perfil'))

    return render_template('auth/cambiar_contrasena.html')


@bp.route('/recuperar', methods=['GET', 'POST'])
def recuperar():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        User.query.filter_by(email=email).first()
        flash('Si el correo existe, se enviaron las instrucciones para recuperar la contraseña.', 'info')
        return redirect(url_for('auth.login'))

    return render_template('auth/recuperar.html')
