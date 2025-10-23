from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import db, Area, Finca, Usuario

areas_bp = Blueprint('areas', __name__)

@areas_bp.route('/areas')
def listar_areas():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    # Filtrar áreas según el rol
    if session['rol'] == 'admin':
        areas = Area.query.filter_by(activa=True).all()
    else:
        usuario = Usuario.query.get(session['user_id'])
        if usuario and usuario.finca_id:
            areas = Area.query.filter_by(finca_id=usuario.finca_id, activa=True).all()
        else:
            areas = []
    
    return render_template('areas/listar.html', areas=areas)

@areas_bp.route('/areas/crear', methods=['GET', 'POST'])
def crear_area():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    if session['rol'] not in ['admin', 'rrhh', 'jefe_cultivo']:
        flash('No tienes permisos para crear áreas', 'error')
        return redirect(url_for('areas.listar_areas'))
    
    if request.method == 'POST':
        # Determinar finca_id según el rol
        if session['rol'] == 'admin':
            finca_id = request.form['finca_id']
        else:
            usuario = Usuario.query.get(session['user_id'])
            finca_id = usuario.finca_id
        
        if 'areas_multiples' in request.form and request.form['areas_multiples']:
            # Crear múltiples áreas
            areas_texto = request.form['areas_multiples']
            areas_numeros = [num.strip() for num in areas_texto.split(',')]
            
            areas_creadas = 0
            for numero in areas_numeros:
                if numero:
                    area = Area(
                        nombre=f"Área {numero}",
                        descripcion=f"Área de cultivo {numero}",
                        finca_id=finca_id
                    )
                    db.session.add(area)
                    areas_creadas += 1
            
            db.session.commit()
            flash(f'{areas_creadas} áreas creadas exitosamente', 'success')
        else:
            # Crear área individual
            area = Area(
                nombre=request.form['nombre'],
                descripcion=request.form['descripcion'],
                finca_id=finca_id
            )
            db.session.add(area)
            db.session.commit()
            flash('Área creada exitosamente', 'success')
        
        return redirect(url_for('areas.listar_areas'))
    
    # Obtener fincas para el dropdown (solo para admin)
    fincas = []
    if session['rol'] == 'admin':
        fincas = Finca.query.filter_by(activa=True).all()
    
    return render_template('areas/crear.html', fincas=fincas)

@areas_bp.route('/areas/gestionar-asignaciones')
def gestionar_asignaciones_areas():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    if session['rol'] not in ['admin', 'rrhh', 'jefe_cultivo']:
        flash('No tienes permisos para realizar esta acción', 'error')
        return redirect(url_for('areas.listar_areas'))
    
    # Filtrar áreas según el rol
    if session['rol'] == 'admin':
        areas = Area.query.filter_by(activa=True).all()
    else:
        usuario = Usuario.query.get(session['user_id'])
        areas = Area.query.filter_by(finca_id=usuario.finca_id, activa=True).all()
    
    # Obtener información completa de cada área
    areas_info = []
    for area in areas:
        # Supervisor asignado
        supervisor = None
        if area.supervisor_id:
            from app.models import Supervisor
            supervisor = Supervisor.query.get(area.supervisor_id)
        
        # Códigos asignados
        from app.models import Codigo
        codigos = Codigo.query.filter_by(area_id=area.id, activo=True).all()
        
        areas_info.append({
            'area': area,
            'supervisor': supervisor,
            'codigos': codigos,
            'total_codigos': len(codigos)
        })
    
    return render_template('areas/gestionar_asignaciones.html', areas_info=areas_info)
