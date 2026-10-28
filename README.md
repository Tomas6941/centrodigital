# Centro de Estudiantes Digital - Lista Azul Liberal Proa

Sistema web para la gestión del Centro de Estudiantes de la Escuela Proa Rebeca Guber.

## Tecnologías

- **Backend:** Flask (Python)
- **Frontend:** HTML, CSS, JavaScript, Jinja2
- **Base de datos:** SQLite (desarrollo) / PostgreSQL (producción)
- **Autenticación:** Flask-Login

## Instalación

1. Crear entorno virtual:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Configurar variables de entorno:
```bash
copy .env.example .env
```

4. Inicializar base de datos:
```bash
python init_db.py
```

5. Ejecutar aplicación:
```bash
python run.py
```

La aplicación estará en `http://localhost:5000`

## Usuario Admin Inicial

- **Email:** tgonzalezzalazar@escuelasproa.edu.ar
- **Contraseña:** admin123

**IMPORTANTE:** Cambiar la contraseña después del primer ingreso.

## Funcionalidades

- Login/registro con roles (admin, tesorero, profesor, alumno)
- Presupuesto del centro con ingresos/egresos y comprobantes
- Banco de proyectos con postulación y evaluación
- Actas del centro
- Reclamos y quejas con seguimiento
- Votaciones con presupuesto participativo
- Panel de administración para gestión de usuarios

## Roles

- **admin:** Acceso total al sistema
- **tesorero:** Gestión de presupuesto
- **profesor:** Solo lectura
- **alumno:** Postular proyectos, crear reclamos, votar
