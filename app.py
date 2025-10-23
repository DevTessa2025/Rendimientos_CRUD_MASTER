from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu-clave-secreta-aqui'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///agricultura.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelos de la base de datos
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    rol = db.Column(db.String(20), nullable=False)  # admin, rrhh, jefe_cultivo
    finca_id = db.Column(db.Integer, db.ForeignKey('finca.id'))  # Finca asignada (None para admin)
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relación con finca
    finca = db.relationship('Finca', backref='usuarios_asignados')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Finca(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    ubicacion = db.Column(db.String(200))
    descripcion = db.Column(db.Text)
    activa = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relación con áreas
    areas = db.relationship('Area', backref='finca', lazy=True)

class Area(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    finca_id = db.Column(db.Integer, db.ForeignKey('finca.id'), nullable=False)
    supervisor_id = db.Column(db.Integer, db.ForeignKey('supervisor.id'))
    activa = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relación con códigos
    codigos = db.relationship('Codigo', backref='area', lazy=True)

class Supervisor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(120))
    clave_acceso = db.Column(db.String(50), unique=True, nullable=False)
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_ultimo_acceso = db.Column(db.DateTime)
    
    # Relación con áreas
    areas = db.relationship('Area', backref='supervisor', lazy=True)

class Codigo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20), unique=True, nullable=False)
    nombre_persona = db.Column(db.String(100), nullable=False)
    apellido_persona = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20))
    area_id = db.Column(db.Integer, db.ForeignKey('area.id'), nullable=False)
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

# Rutas de la aplicación
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = Usuario.query.filter_by(username=username, activo=True).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['rol'] = user.rol
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('index'))
        else:
            flash('Credenciales incorrectas', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada', 'info')
    return redirect(url_for('login'))

# Rutas CRUD para Fincas
@app.route('/fincas')
def listar_fincas():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    fincas = Finca.query.all()
    return render_template('fincas/listar.html', fincas=fincas)

@app.route('/fincas/crear', methods=['GET', 'POST'])
def crear_finca():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Solo admin puede crear fincas
    if session['rol'] != 'admin':
        flash('Solo el administrador puede crear fincas', 'error')
        return redirect(url_for('listar_fincas'))
    
    if request.method == 'POST':
        finca = Finca(
            nombre=request.form['nombre'],
            ubicacion=request.form['ubicacion'],
            descripcion=request.form['descripcion']
        )
        db.session.add(finca)
        db.session.commit()
        flash('Finca creada exitosamente', 'success')
        return redirect(url_for('listar_fincas'))
    
    return render_template('fincas/crear.html')

# Rutas CRUD para Áreas
@app.route('/areas')
def listar_areas():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Filtrar por finca si no es admin
    if session['rol'] == 'admin':
        areas = Area.query.join(Finca).all()
    else:
        # Obtener finca del usuario
        usuario = Usuario.query.get(session['user_id'])
        if usuario.finca_id:
            areas = Area.query.filter(Area.finca_id == usuario.finca_id).all()
        else:
            areas = []
    
    return render_template('areas/listar.html', areas=areas)

@app.route('/areas/crear', methods=['GET', 'POST'])
def crear_area():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if session['rol'] not in ['admin', 'rrhh', 'jefe_cultivo']:
        flash('No tienes permisos para realizar esta acción', 'error')
        return redirect(url_for('listar_areas'))
    
    if request.method == 'POST':
        # Si no es admin, usar la finca asignada al usuario
        if session['rol'] == 'admin':
            finca_id = request.form['finca_id']
        else:
            usuario = Usuario.query.get(session['user_id'])
            finca_id = usuario.finca_id
        
        # Verificar si es creación múltiple
        if 'areas_multiples' in request.form and request.form['areas_multiples']:
            # Crear múltiples áreas (ej: 1,2,3,4,5,6)
            numeros_areas = request.form['areas_multiples'].split(',')
            areas_creadas = 0
            
            for num in numeros_areas:
                num = num.strip()
                if num.isdigit():
                    area = Area(
                        nombre=f"Área {num}",
                        descripcion=f"Área de cultivo número {num}",
                        finca_id=finca_id
                    )
                    db.session.add(area)
                    areas_creadas += 1
            
            db.session.commit()
            flash(f'{areas_creadas} áreas creadas exitosamente', 'success')
        else:
            # Creación individual
            area = Area(
                nombre=request.form['nombre'],
                descripcion=request.form['descripcion'],
                finca_id=finca_id
            )
            db.session.add(area)
            db.session.commit()
            flash('Área creada exitosamente', 'success')
        
        return redirect(url_for('listar_areas'))
    
    # Filtrar fincas según el rol
    if session['rol'] == 'admin':
        fincas = Finca.query.filter_by(activa=True).all()
    else:
        usuario = Usuario.query.get(session['user_id'])
        fincas = Finca.query.filter_by(id=usuario.finca_id, activa=True).all()
    
    return render_template('areas/crear.html', fincas=fincas)

# Rutas CRUD para Supervisores
@app.route('/supervisores')
def listar_supervisores():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    supervisores = Supervisor.query.all()
    return render_template('supervisores/listar.html', supervisores=supervisores)

@app.route('/supervisores/crear', methods=['GET', 'POST'])
def crear_supervisor():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if session['rol'] not in ['admin', 'rrhh', 'jefe_cultivo']:
        flash('No tienes permisos para realizar esta acción', 'error')
        return redirect(url_for('listar_supervisores'))
    
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
        return redirect(url_for('listar_supervisores'))
    
    return render_template('supervisores/crear.html')

@app.route('/supervisores/asignar-area', methods=['GET', 'POST'])
def asignar_supervisor_area():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if session['rol'] not in ['admin', 'rrhh', 'jefe_cultivo']:
        flash('No tienes permisos para realizar esta acción', 'error')
        return redirect(url_for('listar_supervisores'))
    
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
                    return redirect(url_for('asignar_supervisor_area'))
            
            area.supervisor_id = supervisor_id
            db.session.commit()
            flash(f'Supervisor {supervisor.nombre} {supervisor.apellido} asignado al área {area.nombre}', 'success')
            return redirect(url_for('listar_supervisores'))
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

@app.route('/supervisores/gestionar-asignaciones')
def gestionar_asignaciones_supervisores():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if session['rol'] not in ['admin', 'rrhh', 'jefe_cultivo']:
        flash('No tienes permisos para realizar esta acción', 'error')
        return redirect(url_for('listar_supervisores'))
    
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

# Rutas CRUD para Usuarios
@app.route('/usuarios')
def listar_usuarios():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if session['rol'] != 'admin':
        flash('No tienes permisos para ver usuarios', 'error')
        return redirect(url_for('index'))
    
    usuarios = Usuario.query.all()
    return render_template('usuarios/listar.html', usuarios=usuarios)

@app.route('/usuarios/crear', methods=['GET', 'POST'])
def crear_usuario():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if session['rol'] != 'admin':
        flash('No tienes permisos para crear usuarios', 'error')
        return redirect(url_for('listar_usuarios'))
    
    if request.method == 'POST':
        # Crear usuario SIN finca asignada inicialmente
        usuario = Usuario(
            username=request.form['username'],
            email=request.form['email'],
            rol=request.form['rol'],
            finca_id=None  # Sin finca asignada inicialmente
        )
        usuario.set_password(request.form['password'])
        db.session.add(usuario)
        db.session.commit()
        flash('Usuario creado exitosamente. Ahora puedes asignarlo a una finca.', 'success')
        return redirect(url_for('listar_usuarios'))
    
    return render_template('usuarios/crear.html')

@app.route('/usuarios/<int:usuario_id>/asignar', methods=['GET', 'POST'])
def asignar_usuario_finca(usuario_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if session['rol'] != 'admin':
        flash('No tienes permisos para asignar usuarios', 'error')
        return redirect(url_for('listar_usuarios'))
    
    usuario = Usuario.query.get_or_404(usuario_id)
    
    if request.method == 'POST':
        usuario.finca_id = request.form['finca_id'] if request.form['finca_id'] else None
        db.session.commit()
        flash(f'Usuario {usuario.username} asignado exitosamente', 'success')
        return redirect(url_for('listar_usuarios'))
    
    fincas = Finca.query.filter_by(activa=True).all()
    return render_template('usuarios/asignar.html', usuario=usuario, fincas=fincas)

# Rutas CRUD para Códigos
@app.route('/codigos')
def listar_codigos():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Para simplificar, mostrar todos los códigos por ahora
    # TODO: Implementar filtrado por finca más adelante
    codigos = Codigo.query.all()
    
    
    return render_template('codigos/listar.html', codigos=codigos)

@app.route('/codigos/crear', methods=['GET', 'POST'])
def crear_codigo():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if session['rol'] not in ['admin', 'rrhh', 'jefe_cultivo']:
        flash('No tienes permisos para realizar esta acción', 'error')
        return redirect(url_for('listar_codigos'))
    
    if request.method == 'POST':
        # Verificar si es creación en rango
        if 'rango_codigos' in request.form and request.form['rango_codigos']:
            # Crear códigos en rango (ej: 001-010)
            rango = request.form['rango_codigos']
            area_id = request.form.get('area_id')  # Usar get() para evitar KeyError
            
            print(f"DEBUG - Rango: {rango}")
            print(f"DEBUG - Area ID recibido: '{area_id}'")
            print(f"DEBUG - Form data: {dict(request.form)}")
            
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
                        
                        # Verificar si el código ya existe
                        existe = Codigo.query.filter_by(codigo=codigo_str).first()
                        
                        if not existe:
                            codigo = Codigo(
                                codigo=codigo_str,
                                nombre_persona=f"Persona {codigo_str}",
                                apellido_persona="Cosechador",
                                telefono="",
                                area_id=area_id
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
                # Verificar si el código ya existe
                existe = Codigo.query.filter_by(codigo=request.form['codigo']).first()
                
                if existe:
                    flash(f'El código {request.form["codigo"]} ya existe. Por favor use otro código.', 'error')
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
                        area_id=area_id
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
        
        return redirect(url_for('listar_codigos'))
    
    areas = Area.query.filter_by(activa=True).all()
    return render_template('codigos/crear.html', areas=areas)

@app.route('/codigos/asignar-area', methods=['GET', 'POST'])
def asignar_area_codigos():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if session['rol'] not in ['admin', 'rrhh', 'jefe_cultivo']:
        flash('No tienes permisos para realizar esta acción', 'error')
        return redirect(url_for('listar_codigos'))
    
    if request.method == 'POST':
        area_id = request.form['area_id']
        codigos_sin_area = Codigo.query.filter_by(area_id=None).all()
        
        for codigo in codigos_sin_area:
            codigo.area_id = area_id
        
        db.session.commit()
        flash(f'{len(codigos_sin_area)} códigos asignados al área seleccionada', 'success')
        return redirect(url_for('listar_codigos'))
    
    # Filtrar áreas según el rol
    if session['rol'] == 'admin':
        areas = Area.query.filter_by(activa=True).all()
    else:
        usuario = Usuario.query.get(session['user_id'])
        areas = Area.query.filter_by(finca_id=usuario.finca_id, activa=True).all()
    
    codigos_sin_area = Codigo.query.filter_by(area_id=None).count()
    
    return render_template('codigos/asignar_area.html', areas=areas, codigos_sin_area=codigos_sin_area)

@app.route('/codigos/gestionar-asignaciones')
def gestionar_asignaciones_codigos():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if session['rol'] not in ['admin', 'rrhh', 'jefe_cultivo']:
        flash('No tienes permisos para realizar esta acción', 'error')
        return redirect(url_for('listar_codigos'))
    
    # Filtrar áreas según el rol
    if session['rol'] == 'admin':
        areas = Area.query.filter_by(activa=True).all()
    else:
        usuario = Usuario.query.get(session['user_id'])
        areas = Area.query.filter_by(finca_id=usuario.finca_id, activa=True).all()
    
    # Obtener códigos por área
    codigos_por_area = {}
    for area in areas:
        codigos = Codigo.query.filter_by(area_id=area.id).all()
        codigos_por_area[area.id] = {
            'area': area,
            'codigos': codigos,
            'cantidad': len(codigos)
        }
    
    # Códigos sin área
    codigos_sin_area = Codigo.query.filter_by(area_id=None).all()
    
    return render_template('codigos/gestionar_asignaciones.html',
                         codigos_por_area=codigos_por_area,
                         codigos_sin_area=codigos_sin_area)

@app.route('/codigos/asignar-codigo', methods=['GET', 'POST'])
def asignar_codigo_area():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if session['rol'] not in ['admin', 'rrhh', 'jefe_cultivo']:
        flash('No tienes permisos para realizar esta acción', 'error')
        return redirect(url_for('listar_codigos'))
    
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
                    return redirect(url_for('asignar_codigo_area'))
            
            codigo.area_id = area_id
            db.session.commit()
            flash(f'Código {codigo.codigo} asignado al área {area.nombre}', 'success')
            return redirect(url_for('listar_codigos'))
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

@app.route('/areas/gestionar-asignaciones')
def gestionar_asignaciones_areas():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if session['rol'] not in ['admin', 'rrhh', 'jefe_cultivo']:
        flash('No tienes permisos para realizar esta acción', 'error')
        return redirect(url_for('listar_areas'))
    
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
            supervisor = Supervisor.query.get(area.supervisor_id)
        
        # Códigos asignados
        codigos = Codigo.query.filter_by(area_id=area.id, activo=True).all()
        
        areas_info.append({
            'area': area,
            'supervisor': supervisor,
            'codigos': codigos,
            'total_codigos': len(codigos)
        })
    
    return render_template('areas/gestionar_asignaciones.html', areas_info=areas_info)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Crear usuario admin por defecto si no existe
        admin_user = Usuario.query.filter_by(username='admin').first()
        if not admin_user:
            admin = Usuario(
                username='admin',
                email='admin@agricultura.com',
                rol='admin'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("Usuario admin creado: username=admin, password=admin123")
    
    app.run(debug=True)
