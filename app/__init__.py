import os
from flask import Flask, render_template
from .extensions import db, login_manager, migrate
from config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Crear carpetas necesarias
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(app.root_path, 'static', 'img'), exist_ok=True)

    # Inicializar extensiones
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Debes iniciar sesión para acceder a esta página.'
    login_manager.login_message_category = 'warning'

    # Registrar blueprints
    from .auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from .admin import bp as admin_bp
    app.register_blueprint(admin_bp)

    from .presupuesto import bp as presupuesto_bp
    app.register_blueprint(presupuesto_bp)

    from .proyectos import bp as proyectos_bp
    app.register_blueprint(proyectos_bp)

    from .actas import bp as actas_bp
    app.register_blueprint(actas_bp)

    from .reclamos import bp as reclamos_bp
    app.register_blueprint(reclamos_bp)

    from .votaciones import bp as votaciones_bp
    app.register_blueprint(votaciones_bp)

    from .comunicados import bp as comunicados_bp
    app.register_blueprint(comunicados_bp)

    from .calendario import bp as calendario_bp
    app.register_blueprint(calendario_bp)

    from .institucional import bp as institucional_bp
    app.register_blueprint(institucional_bp)

    from .main import bp as main_bp
    app.register_blueprint(main_bp)

    # Error handlers
    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(e):
        return render_template('errors/500.html'), 500

    return app
