from flask import render_template
from flask_login import login_required, current_user
from datetime import datetime
from app.models import PresupuestoMovimiento, Votacion, Reclamo, Proyecto, Comunicado, Evento
from . import bp


@bp.route('/')
@bp.route('/dashboard')
@login_required
def dashboard():
    ingresos = sum(m.monto for m in PresupuestoMovimiento.query.filter_by(tipo='ingreso').all())
    egresos = sum(m.monto for m in PresupuestoMovimiento.query.filter_by(tipo='egreso').all())
    saldo = ingresos - egresos

    ahora = datetime.utcnow()
    votaciones_abiertas = Votacion.query.filter(
        Votacion.activa == True,
        Votacion.fecha_inicio <= ahora,
        Votacion.fecha_fin >= ahora
    ).order_by(Votacion.fecha_fin.asc()).all()

    ultimos_reclamos = Reclamo.query.order_by(Reclamo.fecha_creacion.desc()).limit(3).all()
    ultimos_proyectos = Proyecto.query.order_by(Proyecto.fecha_postulacion.desc()).limit(3).all()
    comunicados = Comunicado.query.order_by(Comunicado.destacado.desc(), Comunicado.fecha_creacion.desc()).limit(3).all()
    proximos_eventos = Evento.query.order_by(Evento.fecha.asc(), Evento.hora.asc()).limit(4).all()

    return render_template('dashboard.html',
                           saldo=saldo,
                           ingresos=ingresos,
                           egresos=egresos,
                           votaciones_abiertas=votaciones_abiertas,
                           ultimos_reclamos=ultimos_reclamos,
                           ultimos_proyectos=ultimos_proyectos,
                           comunicados=comunicados,
                           proximos_eventos=proximos_eventos)