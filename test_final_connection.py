#!/usr/bin/env python3
"""
Script para probar la conexión final con la configuración correcta del servidor
"""

import os
import sys
from pathlib import Path

def test_final_connection():
    """Prueba la conexión con la configuración final del servidor"""
    
    print("🚀 Probando conexión final con la configuración del servidor...")
    print("=" * 70)
    
    # Configuración del servidor
    server = '181.198.42.195'
    port = '5010'
    username = 'sa'
    password = '6509'
    database = 'Rend_Cultivo'
    
    print(f"📊 Servidor: {server}:{port}")
    print(f"📊 Usuario: {username}")
    print(f"📊 Base de datos: {database}")
    print(f"📊 Contraseña: {'*' * len(password)}")
    
    try:
        import pymssql
        
        print(f"\n🔌 Conectando a SQL Server...")
        conn = pymssql.connect(
            server=server,
            port=port,
            user=username,
            password=password,
            database=database,
            timeout=10
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT @@VERSION")
        version = cursor.fetchone()[0]
        
        print(f"✅ ¡Conexión exitosa!")
        print(f"📊 Versión: {version.split('\\n')[0]}")
        
        # Probar consulta a la base de datos
        cursor.execute("SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME LIKE 'app_%'")
        table_count = cursor.fetchone()[0]
        print(f"📊 Tablas con prefijo 'app_': {table_count}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def test_flask_connection():
    """Prueba la conexión usando Flask/SQLAlchemy"""
    
    print(f"\n🧪 Probando conexión con Flask/SQLAlchemy...")
    
    try:
        # Importar la aplicación Flask
        sys.path.append('app')
        from app import create_app
        from app.models import db
        
        app = create_app()
        
        with app.app_context():
            # Probar la conexión
            with db.engine.connect() as connection:
                result = connection.execute(db.text("SELECT 1"))
                print("✅ ¡Conexión Flask/SQLAlchemy exitosa!")
                return True
            
    except Exception as e:
        print(f"❌ Error en conexión Flask: {e}")
        return False

def main():
    """Función principal"""
    
    print("🚀 Script de prueba de conexión final")
    print("=" * 50)
    
    # Probar conexión directa
    if not test_final_connection():
        print("\n❌ No se pudo conectar directamente a SQL Server.")
        print("🔧 Verifica que:")
        print("   - El servidor esté funcionando")
        print("   - Las credenciales sean correctas")
        print("   - El puerto esté abierto")
        return False
    
    # Probar conexión Flask
    if test_flask_connection():
        print("\n🎉 ¡Configuración completada exitosamente!")
        print("🚀 Puedes ejecutar: python main.py")
        return True
    else:
        print("\n⚠️  Conexión directa funciona pero Flask no pudo conectar.")
        print("🔧 Verifica que las dependencias estén instaladas.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
