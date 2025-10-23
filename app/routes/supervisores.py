from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import db, Supervisor, Area, Usuario

supervisores_bp = Blueprint('supervisores', __name__)

@supervisores_bp.route('/supervisores')
def listar_supervisores():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    if session['rol'] not in ['admin', 'rrhh', 'jefe_cultivo']:
        flash('No tienes permisos para ver supervisores', 'error')
        return redirect(url_for('dashboard.index'))
    
    supervisores = Supervisor.query.filter_by(activo=True).all()
    return render_template('supervisores/listar.html', supervisores=supervisores)

@supervisores_bp.route('/supervisores/crear', methods=['GET', 'POST'])
def crear_supervisor():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    if session['rol'] not in ['admin', 'rrhh', 'jefe_cultivo']:
        flash('No tienes permisos para crear supervisores', 'error')
        return redirect(url_for('supervisores.listar_supervisores'))
    
    if request.method == 'POST':
        supervisor = Supervisor(
            nombre=request.form['nombre'],
            apellido=request.form['apellido'],
            telefono=request.form['telefono'],
            email=request.form['email'],
            clave_acceso=request.form['clave_acceso']
        )
        db.session.add(supervisor)
        db.session.commit()
        flash('Supervisor creado exitosamente', 'success')
        return redirect(url_for('supervisores.listar_supervisores'))
    
    return render_template('supervisores/crear.html')

@supervisores_bp.route('/supervisores/asignar-area', methods=['GET', 'POST'])
def asignar_supervisor_area():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    if session['rol'] not in ['admin', 'rrhh', 'jefe_cultivo']:
        flash('No tienes permisos para realizar esta acción', 'error')
        return redirect(url_for('supervisores.listar_supervisores'))
    
    if request.method == 'POST':
        supervisor_id = request.form['supervisor_id']
        area_id = request.form['area_id']
        
        supervisor = Supervisor.query.get(supervisor_id)
        area = Area.query.get(area_id)
        
        if supervisor and area:
            # Verificar que el área pertenece a la finca del usuario
            if session['rol'] != 'admin':
                usuario = Usuario.query.get(session['user_id'])
                if area.finca_id != usuario.finca_id:
                    flash('No puedes asignar supervisores a áreas de otras fincas', 'error')
                    return redirect(url_for('supervisores.asignar_supervisor_area'))
            
            area.supervisor_id = supervisor_id
            db.session.commit()
            flash(f'Supervisor {supervisor.nombre} {supervisor.apellido} asignado al área {area.nombre}', 'success')
            return redirect(url_for('supervisores.listar_supervisores'))
        else:
            flash('Error al asignar supervisor', 'error')
    
    # Filtrar supervisores y áreas según el rol
    if session['rol'] == 'admin':
        supervisores = Supervisor.query.filter_by(activo=True).all()
        areas = Area.query.filter_by(activa=True).all()
    else:
        usuario = Usuario.query.get(session['user_id'])
        supervisores = Supervisor.query.filter_by(activo=True).all()
        areas = Area.query.filter_by(finca_id=usuario.finca_id, activa=True).all()
    
    return render_template('supervisores/asignar_area.html', supervisores=supervisores, areas=areas)

@supervisores_bp.route('/supervisores/gestionar-asignaciones')
def gestionar_asignaciones_supervisores():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    if session['rol'] not in ['admin', 'rrhh', 'jefe_cultivo']:
        flash('No tienes permisos para realizar esta acción', 'error')
        return redirect(url_for('supervisores.listar_supervisores'))
    
    # Filtrar áreas según el rol
    if session['rol'] == 'admin':
        areas = Area.query.filter_by(activa=True).all()
    else:
        usuario = Usuario.query.get(session['user_id'])
        areas = Area.query.filter_by(finca_id=usuario.finca_id, activa=True).all()
    
    # Obtener supervisores por área
    supervisores_por_area = {}
    for area in areas:
        supervisor = None
        if area.supervisor_id:
            supervisor = Supervisor.query.get(area.supervisor_id)
        
        supervisores_por_area[area.id] = {
            'area': area,
            'supervisor': supervisor
        }
    
    # Supervisores sin área
    supervisores_sin_area = Supervisor.query.filter_by(activo=True).all()
    supervisores_sin_area = [s for s in supervisores_sin_area if not any(data['supervisor'] and data['supervisor'].id == s.id for data in supervisores_por_area.values())]
    
    return render_template('supervisores/gestionar_asignaciones.html', 
                         supervisores_por_area=supervisores_por_area, 
                         supervisores_sin_area=supervisores_sin_area)
