from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import db, Usuario, Finca

usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route('/usuarios')
def listar_usuarios():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    if session['rol'] != 'admin':
        flash('No tienes permisos para ver usuarios', 'error')
        return redirect(url_for('dashboard.index'))
    
    usuarios = Usuario.query.all()
    return render_template('usuarios/listar.html', usuarios=usuarios)

@usuarios_bp.route('/usuarios/crear', methods=['GET', 'POST'])
def crear_usuario():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    if session['rol'] != 'admin':
        flash('No tienes permisos para crear usuarios', 'error')
        return redirect(url_for('usuarios.listar_usuarios'))
    
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
        return redirect(url_for('usuarios.listar_usuarios'))
    
    return render_template('usuarios/crear.html')

@usuarios_bp.route('/usuarios/<int:usuario_id>/asignar', methods=['GET', 'POST'])
def asignar_usuario_finca(usuario_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    if session['rol'] != 'admin':
        flash('No tienes permisos para asignar usuarios', 'error')
        return redirect(url_for('usuarios.listar_usuarios'))
    
    usuario = Usuario.query.get_or_404(usuario_id)
    
    if request.method == 'POST':
        usuario.finca_id = request.form['finca_id'] if request.form['finca_id'] else None
        db.session.commit()
        flash(f'Usuario {usuario.username} asignado exitosamente', 'success')
        return redirect(url_for('usuarios.listar_usuarios'))
    
    fincas = Finca.query.filter_by(activa=True).all()
    return render_template('usuarios/asignar.html', usuario=usuario, fincas=fincas)
