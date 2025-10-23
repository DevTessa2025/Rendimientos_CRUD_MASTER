from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import db, Codigo, Area, Usuario

codigos_bp = Blueprint('codigos', __name__)

@codigos_bp.route('/codigos')
def listar_codigos():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    # Filtrar códigos según el rol
    if session['rol'] == 'admin':
        codigos = Codigo.query.all()
    else:
        usuario = Usuario.query.get(session['user_id'])
        if usuario and usuario.finca_id:
            codigos = Codigo.query.filter_by(finca_id=usuario.finca_id).all()
        else:
            codigos = []
    
    return render_template('codigos/listar.html', codigos=codigos)

@codigos_bp.route('/codigos/crear', methods=['GET', 'POST'])
def crear_codigo():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    if session['rol'] not in ['admin', 'rrhh', 'jefe_cultivo']:
        flash('No tienes permisos para realizar esta acción', 'error')
        return redirect(url_for('codigos.listar_codigos'))
    
    if request.method == 'POST':
        # Verificar si es creación en rango
        if 'rango_codigos' in request.form and request.form['rango_codigos']:
            # Crear códigos en rango (ej: 001-010)
            rango = request.form['rango_codigos']
            area_id = request.form.get('area_id')  # Usar get() para evitar KeyError
            
            print(f"DEBUG - Rango: {rango}")
            print(f"DEBUG - Area ID recibido: '{area_id}'")
            print(f"DEBUG - Form data: {dict(request.form)}")
            
            # Obtener finca_id del usuario
            if session['rol'] == 'admin':
                # Admin debe seleccionar finca
                finca_id = request.form.get('finca_id')
                if not finca_id:
                    flash('Debe seleccionar una finca para crear los códigos', 'error')
                    return redirect(url_for('codigos.listar_codigos'))
            else:
                usuario = Usuario.query.get(session['user_id'])
                finca_id = usuario.finca_id
                if not finca_id:
                    flash('No tienes una finca asignada', 'error')
                    return redirect(url_for('codigos.listar_codigos'))
            
            # Permitir crear códigos sin área asignada (se asignará después)
            if area_id == '':
                area_id = None
            
            codigos_creados = 0
            codigos_existentes = 0
            
            try:
                if '-' in rango:
                    inicio, fin = rango.split('-')
                    inicio = int(inicio.strip())
                    fin = int(fin.strip())
                    
                    for i in range(inicio, fin + 1):
                        codigo_str = f"{i:03d}"
                        
                        # Verificar si el código ya existe en esta finca
                        existe = Codigo.query.filter_by(codigo=codigo_str, finca_id=finca_id).first()
                        
                        if not existe:
                            codigo = Codigo(
                                codigo=codigo_str,
                                nombre_persona=f"Persona {codigo_str}",
                                apellido_persona="Cosechador",
                                telefono="",
                                area_id=area_id,
                                finca_id=finca_id
                            )
                            db.session.add(codigo)
                            codigos_creados += 1
                        else:
                            codigos_existentes += 1
                    
                    db.session.commit()
                    
                    mensaje = f'{codigos_creados} códigos creados exitosamente'
                    if codigos_existentes > 0:
                        mensaje += f' ({codigos_existentes} códigos ya existían y fueron omitidos)'
                    
                    flash(mensaje, 'success' if codigos_creados > 0 else 'warning')
                else:
                    flash('Formato de rango incorrecto. Use: 001-010', 'error')
            except ValueError:
                flash('Formato de rango incorrecto. Use números: 001-010', 'error')
            except Exception as e:
                db.session.rollback()
                flash(f'Error al crear códigos: {str(e)}', 'error')
        else:
            # Creación individual
            try:
                # Obtener finca_id del usuario
                if session['rol'] == 'admin':
                    finca_id = request.form.get('finca_id')
                    if not finca_id:
                        flash('Debe seleccionar una finca para crear el código', 'error')
                        return redirect(url_for('codigos.listar_codigos'))
                else:
                    usuario = Usuario.query.get(session['user_id'])
                    finca_id = usuario.finca_id
                    if not finca_id:
                        flash('No tienes una finca asignada', 'error')
                        return redirect(url_for('codigos.listar_codigos'))
                
                # Verificar si el código ya existe en esta finca
                existe = Codigo.query.filter_by(codigo=request.form['codigo'], finca_id=finca_id).first()
                
                if existe:
                    flash(f'El código {request.form["codigo"]} ya existe en esta finca. Por favor use otro código.', 'error')
                else:
                    # Permitir crear códigos sin área asignada
                    area_id = request.form.get('area_id')
                    if area_id == '':
                        area_id = None
                    
                    codigo = Codigo(
                        codigo=request.form['codigo'],
                        nombre_persona=request.form['nombre_persona'],
                        apellido_persona=request.form['apellido_persona'],
                        telefono=request.form['telefono'],
                        area_id=area_id,
                        finca_id=finca_id
                    )
                    db.session.add(codigo)
                    db.session.commit()
                    
                    mensaje = 'Código creado exitosamente'
                    if not area_id:
                        mensaje += '. Recuerda asignar el código a un área posteriormente.'
                    flash(mensaje, 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'Error al crear código: {str(e)}', 'error')
        
        return redirect(url_for('codigos.listar_codigos'))
    
    areas = Area.query.filter_by(activa=True).all()
    
    # Obtener fincas para admins
    fincas = []
    if session['rol'] == 'admin':
        from app.models import Finca
        fincas = Finca.query.filter_by(activa=True).all()
    
    return render_template('codigos/crear.html', areas=areas, fincas=fincas)

@codigos_bp.route('/codigos/asignar-area', methods=['GET', 'POST'])
def asignar_area_codigos():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    if session['rol'] not in ['admin', 'rrhh', 'jefe_cultivo']:
        flash('No tienes permisos para realizar esta acción', 'error')
        return redirect(url_for('codigos.listar_codigos'))
    
    if request.method == 'POST':
        area_id = request.form.get('area_id')
        codigos_seleccionados = request.form.getlist('codigos[]')
        
        if not area_id:
            flash('Debe seleccionar un área', 'error')
            return redirect(url_for('codigos.asignar_area_codigos'))
        
        if not codigos_seleccionados:
            flash('Debe seleccionar al menos un código', 'error')
            return redirect(url_for('codigos.asignar_area_codigos'))
        
        # Asignar los códigos seleccionados al área
        for codigo_id in codigos_seleccionados:
            codigo = Codigo.query.get(codigo_id)
            if codigo:
                codigo.area_id = area_id
        
        db.session.commit()
        flash(f'{len(codigos_seleccionados)} códigos asignados al área seleccionada', 'success')
        return redirect(url_for('codigos.listar_codigos'))
    
    # Filtrar áreas y códigos según el rol
    if session['rol'] == 'admin':
        areas = Area.query.filter_by(activa=True).all()
        codigos_sin_area = Codigo.query.filter_by(area_id=None).all()
    else:
        usuario = Usuario.query.get(session['user_id'])
        if usuario and usuario.finca_id:
            areas = Area.query.filter_by(finca_id=usuario.finca_id, activa=True).all()
            codigos_sin_area = Codigo.query.filter_by(finca_id=usuario.finca_id, area_id=None).all()
        else:
            areas = []
            codigos_sin_area = []
    
    return render_template('codigos/asignar_area.html', areas=areas, codigos_sin_area=codigos_sin_area)

@codigos_bp.route('/codigos/gestionar-asignaciones')
def gestionar_asignaciones_codigos():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    if session['rol'] not in ['admin', 'rrhh', 'jefe_cultivo']:
        flash('No tienes permisos para realizar esta acción', 'error')
        return redirect(url_for('codigos.listar_codigos'))
    
    # Filtrar áreas según el rol
    if session['rol'] == 'admin':
        areas = Area.query.filter_by(activa=True).all()
    else:
        usuario = Usuario.query.get(session['user_id'])
        areas = Area.query.filter_by(finca_id=usuario.finca_id, activa=True).all()
    
    # Obtener códigos por área
    codigos_por_area = {}
    for area in areas:
        codigos = Codigo.query.filter_by(area_id=area.id, activo=True).all()
        codigos_por_area[area.id] = {
            'area': area,
            'codigos': codigos,
            'total': len(codigos)
        }
    
    # Códigos sin área
    codigos_sin_area = Codigo.query.filter_by(area_id=None).all()
    
    return render_template('codigos/gestionar_asignaciones.html',
                         codigos_por_area=codigos_por_area,
                         codigos_sin_area=codigos_sin_area)

@codigos_bp.route('/codigos/asignar-codigo', methods=['GET', 'POST'])
def asignar_codigo_area():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    if session['rol'] not in ['admin', 'rrhh', 'jefe_cultivo']:
        flash('No tienes permisos para realizar esta acción', 'error')
        return redirect(url_for('codigos.listar_codigos'))
    
    if request.method == 'POST':
        codigo_id = request.form['codigo_id']
        area_id = request.form['area_id']
        
        codigo = Codigo.query.get(codigo_id)
        area = Area.query.get(area_id)
        
        if codigo and area:
            # Verificar que el área pertenece a la finca del usuario
            if session['rol'] != 'admin':
                usuario = Usuario.query.get(session['user_id'])
                if area.finca_id != usuario.finca_id:
                    flash('No puedes asignar códigos a áreas de otras fincas', 'error')
                    return redirect(url_for('codigos.asignar_codigo_area'))
            
            codigo.area_id = area_id
            db.session.commit()
            flash(f'Código {codigo.codigo} asignado al área {area.nombre}', 'success')
            return redirect(url_for('codigos.listar_codigos'))
        else:
            flash('Error al asignar código', 'error')
    
    # Filtrar códigos y áreas según el rol
    if session['rol'] == 'admin':
        codigos_sin_area = Codigo.query.filter_by(area_id=None, activo=True).all()
        areas = Area.query.filter_by(activa=True).all()
    else:
        usuario = Usuario.query.get(session['user_id'])
        codigos_sin_area = Codigo.query.filter_by(area_id=None, activo=True).all()
        areas = Area.query.filter_by(finca_id=usuario.finca_id, activa=True).all()
    
    return render_template('codigos/asignar_codigo_area.html', 
                         codigos_sin_area=codigos_sin_area, 
                         areas=areas)
