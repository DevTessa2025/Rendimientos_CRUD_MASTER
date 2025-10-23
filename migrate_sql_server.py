#!/usr/bin/env python3
"""
Script para migrar la aplicación a SQL Server
Crea las tablas con prefijo app_ en la base de datos Rend_Cultivo
"""

import os
import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

from app import create_app, db
from app.models import Usuario, Finca, Area, Supervisor, Codigo

def migrate_to_sql_server():
    """Migrar a SQL Server con tablas con prefijo app_"""
    print("🔄 Iniciando migración a SQL Server...")
    print("📊 Base de datos: Rend_Cultivo")
    print("🏷️  Prefijo de tablas: app_")
    print("=" * 50)
    
    # Crear la aplicación
    app = create_app()
    
    with app.app_context():
        try:
            # Verificar conexión
            print("🔌 Verificando conexión a SQL Server...")
            db.engine.execute("SELECT 1")
            print("✅ Conexión exitosa a SQL Server")
            
            # Crear todas las tablas
            print("📋 Creando tablas con prefijo app_...")
            db.create_all()
            print("✅ Tablas creadas exitosamente")
            
            # Verificar que las tablas existen
            print("🔍 Verificando tablas creadas...")
            result = db.engine.execute("""
                SELECT TABLE_NAME 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_NAME LIKE 'app_%' 
                AND TABLE_TYPE = 'BASE TABLE'
            """)
            
            tables = [row[0] for row in result]
            print(f"📊 Tablas encontradas: {', '.join(tables)}")
            
            # Crear usuario admin si no existe
            admin_exists = Usuario.query.filter_by(username='admin').first()
            if not admin_exists:
                print("👤 Creando usuario admin...")
                admin = Usuario(
                    username='admin',
                    email='admin@agricultura.com',
                    rol='admin',
                    activo=True
                )
                admin.set_password('admin123')
                db.session.add(admin)
                db.session.commit()
                print("✅ Usuario admin creado")
            else:
                print("ℹ️  Usuario admin ya existe")
            
            # Crear finca de ejemplo si no existe
            finca_exists = Finca.query.filter_by(nombre='Finca Ejemplo').first()
            if not finca_exists:
                print("🏢 Creando finca de ejemplo...")
                finca = Finca(
                    nombre='Finca Ejemplo',
                    ubicacion='Ubicación de ejemplo',
                    descripcion='Finca creada automáticamente',
                    activa=True
                )
                db.session.add(finca)
                db.session.commit()
                print("✅ Finca de ejemplo creada")
            else:
                print("ℹ️  Finca de ejemplo ya existe")
            
            print("\n🎉 Migración completada exitosamente!")
            print("📋 Credenciales de acceso:")
            print("   Usuario: admin")
            print("   Email: admin@agricultura.com")
            print("   Password: admin123")
            print("\n🔧 Configuración:")
            print("   - Tablas creadas con prefijo 'app_'")
            print("   - Base de datos: Rend_Cultivo")
            print("   - Servidor: 181.198.42.195,5010")
            
        except Exception as e:
            print(f"❌ Error durante la migración: {str(e)}")
            print("\n🔧 Posibles soluciones:")
            print("1. Verificar que el servidor SQL Server esté accesible")
            print("2. Verificar credenciales de conexión")
            print("3. Verificar que el driver ODBC esté instalado")
            print("4. Ejecutar primero el script SQL manualmente en Azure Data Studio")
            return False
    
    return True

if __name__ == '__main__':
    print("🚀 Migración a SQL Server")
    print("=" * 50)
    
    # Verificar que se pueden instalar las dependencias
    try:
        import pyodbc
        import pymssql
        print("✅ Dependencias de SQL Server disponibles")
    except ImportError as e:
        print(f"❌ Faltan dependencias: {e}")
        print("💡 Ejecuta: pip install -r requirements.txt")
        sys.exit(1)
    
    success = migrate_to_sql_server()
    
    if success:
        print("\n🎯 Próximos pasos:")
        print("1. Ejecuta: python main.py")
        print("2. Abre: http://127.0.0.1:5000")
        print("3. Inicia sesión con las credenciales admin")
    else:
        print("\n❌ La migración falló. Revisa los errores anteriores.")
        sys.exit(1)
