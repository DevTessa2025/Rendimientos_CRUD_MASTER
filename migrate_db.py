#!/usr/bin/env python3
"""
Script para recrear la base de datos con el nuevo esquema
que incluye finca_id en los códigos para evitar duplicados entre fincas.
"""

import os
import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

from app import create_app, db
from app.models import Usuario, Finca, Area, Supervisor, Codigo

def recreate_database():
    """Recrear la base de datos con el nuevo esquema."""
    print("🔄 Recreando base de datos con nuevo esquema...")
    
    # Crear la aplicación
    app = create_app()
    
    with app.app_context():
        # Eliminar todas las tablas
        db.drop_all()
        print("✅ Tablas existentes eliminadas")
        
        # Crear todas las tablas con el nuevo esquema
        db.create_all()
        print("✅ Nuevas tablas creadas con esquema actualizado")
        
        # Crear usuario admin por defecto
        admin = Usuario(
            username='admin',
            email='admin@agricultura.com',
            rol='admin',
            activo=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Crear una finca de ejemplo
        finca_ejemplo = Finca(
            nombre='Finca Ejemplo',
            ubicacion='Ubicación de ejemplo',
            activa=True
        )
        db.session.add(finca_ejemplo)
        
        db.session.commit()
        print("✅ Usuario admin y finca de ejemplo creados")
        
        print("\n🎉 Base de datos recreada exitosamente!")
        print("📋 Credenciales de acceso:")
        print("   Email: admin@agricultura.com")
        print("   Password: admin123")
        print("\n🔧 Cambios implementados:")
        print("   - Los códigos ahora son únicos por finca")
        print("   - Se agregó finca_id a la tabla codigo")
        print("   - Los usuarios RRHH/Jefe solo ven códigos de su finca asignada")

if __name__ == '__main__':
    recreate_database()
