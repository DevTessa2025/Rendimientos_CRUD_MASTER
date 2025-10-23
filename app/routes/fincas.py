from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import db, Finca

fincas_bp = Blueprint('fincas', __name__)

@fincas_bp.route('/fincas')
def listar_fincas():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    if session['rol'] != 'admin':
        flash('No tienes permisos para ver fincas', 'error')
        return redirect(url_for('dashboard.index'))
    
    fincas = Finca.query.filter_by(activa=True).all()
    return render_template('fincas/listar.html', fincas=fincas)

@fincas_bp.route('/fincas/crear', methods=['GET', 'POST'])
def crear_finca():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    if session['rol'] != 'admin':
        flash('Solo el administrador puede crear fincas', 'error')
        return redirect(url_for('fincas.listar_fincas'))
    
    if request.method == 'POST':
        finca = Finca(
            nombre=request.form['nombre'],
            ubicacion=request.form['ubicacion'],
            descripcion=request.form['descripcion']
        )
        db.session.add(finca)
        db.session.commit()
        flash('Finca creada exitosamente', 'success')
        return redirect(url_for('fincas.listar_fincas'))
    
    return render_template('fincas/crear.html')
