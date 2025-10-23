from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import db, Usuario

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = Usuario.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['rol'] = user.rol
            flash(f'Bienvenido, {user.username}!', 'success')
            return redirect(url_for('dashboard.index'))
        else:
            flash('Credenciales incorrectas', 'error')
    
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada exitosamente', 'info')
    return redirect(url_for('auth.login'))
