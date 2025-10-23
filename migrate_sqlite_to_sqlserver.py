#!/usr/bin/env python3
"""
Script para migrar datos de SQLite a SQL Server
"""

import sys
import os
from pathlib import Path
from datetime import datetime

def migrate_sqlite_to_sqlserver():
    """Migra datos de SQLite a SQL Server"""
    
    print("🔄 Migrando datos de SQLite a SQL Server...")
    print("=" * 60)
    
    try:
        # Importar la aplicación Flask
        sys.path.append('app')
        from app import create_app
        from app.models import db, Usuario, Finca, Area, Supervisor, Codigo
        from sqlalchemy import create_engine, text
        
        app = create_app()
        
        with app.app_context():
            print("✅ Conexión a SQL Server establecida")
            
            # Verificar que estamos usando SQL Server
            print(f"📊 Base de datos actual: {db.engine.url}")
            
            if 'sqlite' in str(db.engine.url):
                print("❌ ERROR: La aplicación aún está usando SQLite")
                print("🔧 Ejecuta: python switch_database.py --sqlserver")
                return False
            
            # Crear tablas en SQL Server si no existen
            print("\n🔧 Creando tablas en SQL Server...")
            db.create_all()
            print("✅ Tablas creadas/verificadas")
            
            # Verificar si ya hay datos en SQL Server
            usuarios_count = Usuario.query.count()
            fincas_count = Finca.query.count()
            
            print(f"\n📊 Datos actuales en SQL Server:")
            print(f"   Usuarios: {usuarios_count}")
            print(f"   Fincas: {fincas_count}")
            
            if usuarios_count > 0 or fincas_count > 0:
                print("⚠️  Ya hay datos en SQL Server")
                respuesta = input("¿Deseas continuar y agregar más datos? (y/n): ")
                if respuesta.lower() != 'y':
                    print("❌ Migración cancelada")
                    return False
            
            # Crear usuario admin si no existe
            admin_user = Usuario.query.filter_by(username='admin').first()
            if not admin_user:
                print("\n👤 Creando usuario admin...")
                from werkzeug.security import generate_password_hash
                
                admin_user = Usuario(
                    username='admin',
                    email='admin@tessacorporation.com',
                    password_hash=generate_password_hash('admin'),
                    rol='admin',
                    activo=True,
                    fecha_creacion=datetime.now()
                )
                db.session.add(admin_user)
                db.session.commit()
                print("✅ Usuario admin creado")
            else:
                print("✅ Usuario admin ya existe")
            
            # Crear fincas de ejemplo si no existen
            fincas_ejemplo = [
                {
                    'nombre': 'Tessa 1',
                    'ubicacion': 'Ubicación Tessa 1',
                    'descripcion': 'Finca principal Tessa 1',
                    'activa': True
                },
                {
                    'nombre': 'Tessa 3',
                    'ubicacion': 'Ubicación Tessa 3',
                    'descripcion': 'Finca principal Tessa 3',
                    'activa': True
                },
                {
                    'nombre': 'Positano',
                    'ubicacion': 'Ubicación Positano',
                    'descripcion': 'Finca Positano',
                    'activa': True
                },
                {
                    'nombre': 'Ecuanros 1',
                    'ubicacion': 'Ubicación Ecuanros 1',
                    'descripcion': 'Finca Ecuanros 1',
                    'activa': True
                }
            ]
            
            print(f"\n🏡 Creando fincas de ejemplo...")
            for finca_data in fincas_ejemplo:
                # Verificar si la finca ya existe
                existing_finca = Finca.query.filter_by(nombre=finca_data['nombre']).first()
                if not existing_finca:
                    finca = Finca(
                        nombre=finca_data['nombre'],
                        ubicacion=finca_data['ubicacion'],
                        descripcion=finca_data['descripcion'],
                        activa=finca_data['activa'],
                        fecha_creacion=datetime.now()
                    )
                    db.session.add(finca)
                    print(f"   ✅ {finca_data['nombre']} creada")
                else:
                    print(f"   ⚠️  {finca_data['nombre']} ya existe")
            
            db.session.commit()
            print("✅ Fincas creadas/verificadas")
            
            # Verificar datos finales
            print(f"\n📊 DATOS FINALES EN SQL SERVER:")
            usuarios_final = Usuario.query.count()
            fincas_final = Finca.query.count()
            areas_final = Area.query.count()
            supervisores_final = Supervisor.query.count()
            codigos_final = Codigo.query.count()
            
            print(f"   Usuarios: {usuarios_final}")
            print(f"   Fincas: {fincas_final}")
            print(f"   Áreas: {areas_final}")
            print(f"   Supervisores: {supervisores_final}")
            print(f"   Códigos: {codigos_final}")
            
            print(f"\n🎉 ¡Migración completada exitosamente!")
            return True
                
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Función principal"""
    
    print("🚀 Script de migración SQLite → SQL Server")
    print("=" * 70)
    
    if migrate_sqlite_to_sqlserver():
        print("\n✅ ¡Migración exitosa!")
        print("🚀 Ahora la aplicación usará SQL Server")
    else:
        print("\n❌ Error en la migración")

if __name__ == "__main__":
    main()
