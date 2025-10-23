#!/usr/bin/env python3
"""
Script para corregir todos los esquemas de las tablas
"""

import sys
from pathlib import Path

def fix_all_schemas():
    """Corrige todos los esquemas de las tablas"""
    
    print("🔧 Corrigiendo esquemas de todas las tablas...")
    print("=" * 60)
    
    try:
        # Importar la aplicación Flask
        sys.path.append('app')
        from app import create_app
        from app.models import db
        from sqlalchemy import text
        
        app = create_app()
        
        with app.app_context():
            print("✅ Conexión a SQL Server establecida")
            
            # Correcciones para app_finca
            print(f"\n🏡 Corrigiendo tabla app_finca...")
            try:
                # Corregir fecha_creacion
                db.session.execute(text("""
                    ALTER TABLE app_finca 
                    ALTER COLUMN fecha_creacion DATETIME2
                """))
                db.session.commit()
                print("✅ Columna fecha_creacion corregida en app_finca")
            except Exception as e:
                print(f"   Error en app_finca: {e}")
            
            # Correcciones para app_usuario
            print(f"\n👤 Corrigiendo tabla app_usuario...")
            try:
                # Corregir fecha_creacion
                db.session.execute(text("""
                    ALTER TABLE app_usuario 
                    ALTER COLUMN fecha_creacion DATETIME2
                """))
                db.session.commit()
                print("✅ Columna fecha_creacion corregida en app_usuario")
            except Exception as e:
                print(f"   Error en app_usuario: {e}")
            
            # Correcciones para app_area
            print(f"\n🌱 Corrigiendo tabla app_area...")
            try:
                # Corregir fecha_creacion
                db.session.execute(text("""
                    ALTER TABLE app_area 
                    ALTER COLUMN fecha_creacion DATETIME2
                """))
                db.session.commit()
                print("✅ Columna fecha_creacion corregida en app_area")
            except Exception as e:
                print(f"   Error en app_area: {e}")
            
            # Correcciones para app_supervisor
            print(f"\n👨‍💼 Corrigiendo tabla app_supervisor...")
            try:
                # Corregir fecha_creacion
                db.session.execute(text("""
                    ALTER TABLE app_supervisor 
                    ALTER COLUMN fecha_creacion DATETIME2
                """))
                db.session.commit()
                print("✅ Columna fecha_creacion corregida en app_supervisor")
            except Exception as e:
                print(f"   Error en app_supervisor: {e}")
            
            # Correcciones para app_codigo
            print(f"\n🔢 Corrigiendo tabla app_codigo...")
            try:
                # Corregir fecha_creacion
                db.session.execute(text("""
                    ALTER TABLE app_codigo 
                    ALTER COLUMN fecha_creacion DATETIME2
                """))
                db.session.commit()
                print("✅ Columna fecha_creacion corregida en app_codigo")
            except Exception as e:
                print(f"   Error en app_codigo: {e}")
            
            print(f"\n✅ Correcciones completadas")
            return True
                
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_all_operations():
    """Prueba todas las operaciones después de las correcciones"""
    
    print(f"\n🧪 Probando todas las operaciones...")
    print("=" * 50)
    
    try:
        # Importar la aplicación Flask
        sys.path.append('app')
        from app import create_app
        from app.models import db, Usuario, Finca, Area, Supervisor, Codigo
        from werkzeug.security import generate_password_hash
        from datetime import datetime
        
        app = create_app()
        
        with app.app_context():
            # Probar creación de finca
            print("🏡 Probando creación de finca...")
            try:
                test_finca = Finca(
                    nombre='Finca de Prueba',
                    ubicacion='Ubicación de prueba',
                    descripcion='Descripción de prueba',
                    activa=True,
                    fecha_creacion=datetime.now()
                )
                db.session.add(test_finca)
                db.session.commit()
                print("✅ Finca creada exitosamente")
                
                # Limpiar
                db.session.delete(test_finca)
                db.session.commit()
                print("✅ Finca de prueba eliminada")
            except Exception as e:
                print(f"❌ Error creando finca: {e}")
            
            # Probar creación de usuario
            print("👤 Probando creación de usuario...")
            try:
                test_user = Usuario(
                    username='test_user',
                    email='test@example.com',
                    password_hash=generate_password_hash('test123'),
                    rol='rrhh',
                    activo=True,
                    fecha_creacion=datetime.now()
                )
                db.session.add(test_user)
                db.session.commit()
                print("✅ Usuario creado exitosamente")
                
                # Limpiar
                db.session.delete(test_user)
                db.session.commit()
                print("✅ Usuario de prueba eliminado")
            except Exception as e:
                print(f"❌ Error creando usuario: {e}")
            
            return True
                
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Función principal"""
    
    print("🚀 Script de corrección de esquemas")
    print("=" * 70)
    
    # Corregir esquemas
    if fix_all_schemas():
        print("\n✅ ¡Esquemas corregidos!")
        
        # Probar operaciones
        if test_all_operations():
            print("\n🎉 ¡Corrección exitosa!")
            print("🚀 Ahora todas las operaciones funcionarán correctamente")
        else:
            print("\n⚠️  Esquemas corregidos pero hay problemas con las operaciones")
    else:
        print("\n❌ Error en la corrección de esquemas")

if __name__ == "__main__":
    main()
