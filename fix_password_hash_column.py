#!/usr/bin/env python3
"""
Script para corregir el tamaño de la columna password_hash
"""

import sys
from pathlib import Path

def fix_password_hash_column():
    """Corrige el tamaño de la columna password_hash"""
    
    print("🔧 Corrigiendo columna password_hash...")
    print("=" * 50)
    
    try:
        # Importar la aplicación Flask
        sys.path.append('app')
        from app import create_app
        from app.models import db
        from sqlalchemy import text
        
        app = create_app()
        
        with app.app_context():
            print("✅ Conexión a SQL Server establecida")
            
            # Verificar el tamaño actual de la columna
            print("\n📊 Verificando esquema actual...")
            try:
                result = db.session.execute(text("""
                    SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH 
                    FROM INFORMATION_SCHEMA.COLUMNS 
                    WHERE TABLE_NAME = 'app_usuario' AND COLUMN_NAME = 'password_hash'
                """))
                column_info = result.fetchone()
                if column_info:
                    print(f"   Columna: {column_info[0]}")
                    print(f"   Tipo: {column_info[1]}")
                    print(f"   Longitud: {column_info[2]}")
                else:
                    print("   Columna password_hash no encontrada")
            except Exception as e:
                print(f"   Error verificando esquema: {e}")
            
            # Corregir el tamaño de la columna
            print(f"\n🔧 Corrigiendo tamaño de columna...")
            try:
                # Cambiar a VARCHAR(500) para acomodar hashes largos
                db.session.execute(text("""
                    ALTER TABLE app_usuario 
                    ALTER COLUMN password_hash VARCHAR(500)
                """))
                db.session.commit()
                print("✅ Columna password_hash corregida a VARCHAR(500)")
            except Exception as e:
                print(f"   Error corrigiendo columna: {e}")
                # Intentar con NVARCHAR si VARCHAR falla
                try:
                    db.session.execute(text("""
                        ALTER TABLE app_usuario 
                        ALTER COLUMN password_hash NVARCHAR(500)
                    """))
                    db.session.commit()
                    print("✅ Columna password_hash corregida a NVARCHAR(500)")
                except Exception as e2:
                    print(f"   Error con NVARCHAR: {e2}")
            
            # Verificar el cambio
            print(f"\n📊 Verificando cambio...")
            try:
                result = db.session.execute(text("""
                    SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH 
                    FROM INFORMATION_SCHEMA.COLUMNS 
                    WHERE TABLE_NAME = 'app_usuario' AND COLUMN_NAME = 'password_hash'
                """))
                column_info = result.fetchone()
                if column_info:
                    print(f"   Columna: {column_info[0]}")
                    print(f"   Tipo: {column_info[1]}")
                    print(f"   Longitud: {column_info[2]}")
                    if int(column_info[2]) >= 500:
                        print("✅ Columna corregida exitosamente")
                    else:
                        print("⚠️  Columna aún es pequeña")
                else:
                    print("   No se pudo verificar el cambio")
            except Exception as e:
                print(f"   Error verificando cambio: {e}")
            
            return True
                
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_user_creation():
    """Prueba crear un usuario después de la corrección"""
    
    print(f"\n🧪 Probando creación de usuario...")
    print("=" * 50)
    
    try:
        # Importar la aplicación Flask
        sys.path.append('app')
        from app import create_app
        from app.models import db, Usuario
        from werkzeug.security import generate_password_hash
        from datetime import datetime
        
        app = create_app()
        
        with app.app_context():
            # Crear usuario de prueba
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
            
            print("✅ Usuario de prueba creado exitosamente")
            print(f"   Usuario: {test_user.username}")
            print(f"   Email: {test_user.email}")
            print(f"   Rol: {test_user.rol}")
            
            # Limpiar usuario de prueba
            db.session.delete(test_user)
            db.session.commit()
            print("✅ Usuario de prueba eliminado")
            
            return True
                
    except Exception as e:
        print(f"❌ Error creando usuario: {e}")
        return False

def main():
    """Función principal"""
    
    print("🚀 Script de corrección de columna password_hash")
    print("=" * 70)
    
    # Corregir columna
    if fix_password_hash_column():
        print("\n✅ ¡Columna corregida!")
        
        # Probar creación de usuario
        if test_user_creation():
            print("\n🎉 ¡Corrección exitosa!")
            print("🚀 Ahora puedes crear usuarios sin problemas")
        else:
            print("\n⚠️  Corrección aplicada pero hay problemas con la creación")
    else:
        print("\n❌ Error en la corrección")

if __name__ == "__main__":
    main()
