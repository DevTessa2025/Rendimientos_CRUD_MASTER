#!/usr/bin/env python3
"""
Script para configurar SQL Server sin crear tablas
"""

import sys
from pathlib import Path

def setup_sqlserver():
    """Configura SQL Server sin crear tablas"""
    
    print("🔧 Configurando SQL Server...")
    print("=" * 50)
    
    try:
        # Importar la aplicación Flask
        sys.path.append('app')
        from app import create_app
        from app.models import db, Usuario, Finca
        from sqlalchemy import text
        
        app = create_app()
        
        with app.app_context():
            print("✅ Conexión a SQL Server establecida")
            print(f"📊 Base de datos: {db.engine.url}")
            
            # Verificar que estamos usando SQL Server
            if 'sqlite' in str(db.engine.url):
                print("❌ ERROR: Aún está usando SQLite")
                return False
            elif 'mssql' in str(db.engine.url):
                print("✅ CORRECTO: Usando SQL Server")
            else:
                print(f"❓ Driver: {db.engine.url.drivername}")
            
            # Verificar datos existentes
            print(f"\n📊 DATOS EXISTENTES:")
            
            try:
                # Contar usuarios
                result = db.session.execute(text("SELECT COUNT(*) FROM app_usuario"))
                usuarios_count = result.fetchone()[0]
                print(f"   Usuarios: {usuarios_count}")
            except Exception as e:
                print(f"   Usuarios: Error - {e}")
            
            try:
                # Contar fincas
                result = db.session.execute(text("SELECT COUNT(*) FROM app_finca"))
                fincas_count = result.fetchone()[0]
                print(f"   Fincas: {fincas_count}")
            except Exception as e:
                print(f"   Fincas: Error - {e}")
            
            try:
                # Contar áreas
                result = db.session.execute(text("SELECT COUNT(*) FROM app_area"))
                areas_count = result.fetchone()[0]
                print(f"   Áreas: {areas_count}")
            except Exception as e:
                print(f"   Áreas: Error - {e}")
            
            try:
                # Contar supervisores
                result = db.session.execute(text("SELECT COUNT(*) FROM app_supervisor"))
                supervisores_count = result.fetchone()[0]
                print(f"   Supervisores: {supervisores_count}")
            except Exception as e:
                print(f"   Supervisores: Error - {e}")
            
            try:
                # Contar códigos
                result = db.session.execute(text("SELECT COUNT(*) FROM app_codigo"))
                codigos_count = result.fetchone()[0]
                print(f"   Códigos: {codigos_count}")
            except Exception as e:
                print(f"   Códigos: Error - {e}")
            
            # Verificar usuario admin
            try:
                result = db.session.execute(text("SELECT username, email, rol FROM app_usuario WHERE username = 'admin'"))
                admin_user = result.fetchone()
                if admin_user:
                    print(f"\n👤 Usuario admin: {admin_user.username} ({admin_user.email}) - Rol: {admin_user.rol}")
                else:
                    print(f"\n❌ Usuario admin no encontrado")
            except Exception as e:
                print(f"   Usuario admin: Error - {e}")
            
            # Verificar fincas
            try:
                result = db.session.execute(text("SELECT id, nombre, ubicacion FROM app_finca"))
                fincas = result.fetchall()
                print(f"\n🏡 Fincas en SQL Server:")
                for finca in fincas:
                    print(f"   - ID: {finca.id}, Nombre: {finca.nombre}, Ubicación: {finca.ubicacion}")
            except Exception as e:
                print(f"   Fincas: Error - {e}")
            
            print(f"\n✅ Configuración completada")
            return True
                
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Función principal"""
    
    print("🚀 Script de configuración de SQL Server")
    print("=" * 70)
    
    if setup_sqlserver():
        print("\n✅ ¡Configuración exitosa!")
        print("🚀 La aplicación ahora usa SQL Server")
    else:
        print("\n❌ Error en la configuración")

if __name__ == "__main__":
    main()
