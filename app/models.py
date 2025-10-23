from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'app_usuario'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    rol = db.Column(db.String(20), nullable=False)  # admin, rrhh, jefe_cultivo
    finca_id = db.Column(db.Integer, db.ForeignKey('app_finca.id'))  # Finca asignada (None para admin)
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    finca = db.relationship('Finca', backref='usuarios_asignados')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<Usuario {self.username}>'

class Finca(db.Model):
    __tablename__ = 'app_finca'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    ubicacion = db.Column(db.String(200))
    descripcion = db.Column(db.Text)
    activa = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    areas = db.relationship('Area', backref='finca', lazy=True)
    
    def __repr__(self):
        return f'<Finca {self.nombre}>'

class Area(db.Model):
    __tablename__ = 'app_area'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    finca_id = db.Column(db.Integer, db.ForeignKey('app_finca.id'), nullable=False)
    supervisor_id = db.Column(db.Integer, db.ForeignKey('app_supervisor.id'))  # Supervisor asignado
    activa = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relaciones
    supervisor = db.relationship('Supervisor', backref='area_asignada', uselist=False)
    codigos = db.relationship('Codigo', backref='area', lazy=True)
    
    def __repr__(self):
        return f'<Area {self.nombre}>'

class Supervisor(db.Model):
    __tablename__ = 'app_supervisor'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(120))
    clave_acceso = db.Column(db.String(50), unique=True, nullable=False)
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_ultimo_acceso = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<Supervisor {self.nombre} {self.apellido}>'

class Codigo(db.Model):
    __tablename__ = 'app_codigo'
    
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20), nullable=False)
    nombre_persona = db.Column(db.String(100), nullable=False)
    apellido_persona = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20))
    area_id = db.Column(db.Integer, db.ForeignKey('app_area.id'))  # Área asignada
    finca_id = db.Column(db.Integer, db.ForeignKey('app_finca.id'), nullable=False)  # Finca del código
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relación con finca
    finca = db.relationship('Finca', backref='codigos')
    
    # Constraint único: código debe ser único dentro de cada finca
    __table_args__ = (db.UniqueConstraint('codigo', 'finca_id', name='_codigo_finca_uc'),)
    
    def __repr__(self):
        return f'<Codigo {self.codigo} (Finca {self.finca_id})>'
