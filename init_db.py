from app import create_app
from app.extensions import db
from app.models import Role, User

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()
    
    # Crear roles base
    roles = [
        Role(nombre='admin', descripcion='Administrador del centro de estudiantes'),
        Role(nombre='tesorero', descripcion='Encargado de finanzas'),
        Role(nombre='profesor', descripcion='Profesor'),
        Role(nombre='alumno', descripcion='Alumno'),
    ]
    for rol in roles:
        db.session.add(rol)
    db.session.commit()
    
    # Crear usuario admin inicial
    admin_rol = Role.query.filter_by(nombre='admin').first()
    admin = User(
        nombre='Tomás',
        apellido='González Zalazar',
        email='tgonzalezzalazar@escuelasproa.edu.ar',
        curso='Sexto año',
        rol_id=admin_rol.id,
        activo=True
    )
    admin.set_password('admin123')
    db.session.add(admin)
    db.session.commit()
    
    print('Base de datos inicializada correctamente')
    print('Roles creados: admin, tesorero, profesor, alumno')
    print('Usuario admin creado:')
    print('  Email: tgonzalezzalazar@escuelasproa.edu.ar')
    print('  Contraseña: admin123')
    print('\n¡IMPORTANTE: Cambiar la contraseña después del primer ingreso!')
