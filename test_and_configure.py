#!/usr/bin/env python3
"""
Script para probar conexión a SQL Server y configurar la aplicación automáticamente
"""

import os
import sys
import shutil
from pathlib import Path

def test_sql_server_connection():
    """Prueba la conexión a SQL Server con diferentes configuraciones"""
    
    print("🔌 Probando conexión a SQL Server...")
    print("=" * 50)
    
    # Configuraciones a probar
    configs = [
        {
            'name': 'Configuración Flutter (181.198.42.195:5010)',
            'server': '181.198.42.195',
            'port': '5010',
            'username': 'sa',
            'password': '6509',
            'database': 'Rend_Cultivo'
        },
        {
            'name': 'Configuración alternativa (181.198.42.194:5010)',
            'server': '181.198.42.194',
            'port': '5010',
            'username': 'sa',
            'password': '6509',
            'database': 'Rend_Cultivo'
        },
        {
            'name': 'Configuración localhost (localhost:1433)',
            'server': 'localhost',
            'port': '1433',
            'username': 'sa',
            'password': '6509',
            'database': 'Rend_Cultivo'
        }
    ]
    
    for config in configs:
        print(f"\n1️⃣ Probando {config['name']}...")
        try:
            import pymssql
            
            conn = pymssql.connect(
                server=config['server'],
                port=config['port'],
                user=config['username'],
                password=config['password'],
                database=config['database'],
                timeout=10
            )
            
            cursor = conn.cursor()
            cursor.execute("SELECT @@VERSION")
            version = cursor.fetchone()[0]
            conn.close()
            
            print(f"✅ ¡Conexión exitosa!")
            print(f"📊 Servidor: {config['server']}:{config['port']}")
            print(f"📊 Base de datos: {config['database']}")
            print(f"📊 Versión: {version.split('\\n')[0]}")
            
            return config
            
        except Exception as e:
            print(f"❌ Error: {e}")
            continue
    
    return None

def create_config_file(working_config):
    """Crea el archivo de configuración con la configuración que funciona"""
    
    print(f"\n🔧 Creando configuración con {working_config['name']}...")
    
    config_content = f'''# app/config_sqlserver.py
import os
from pathlib import Path

basedir = Path(__file__).parent.parent

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Configuración para SQL Server
    SQL_SERVER_CONFIG = {{
        'server': '{working_config['server']}',  # IP del servidor SQL Server
        'port': '{working_config['port']}',              # Puerto del servidor
        'database': '{working_config['database']}',
        'username': '{working_config['username']}',
        'password': '{working_config['password']}',
        'driver': 'ODBC Driver 17 for SQL Server'
    }}
    
    # URL de conexión para SQL Server usando pymssql
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or (
        f"mssql+pymssql://{{SQL_SERVER_CONFIG['username']}}:{{SQL_SERVER_CONFIG['password']}}"
        f"@{{SQL_SERVER_CONFIG['server']}}:{{SQL_SERVER_CONFIG['port']}}/{{SQL_SERVER_CONFIG['database']}}"
    )
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {{
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}}
'''
    
    # Escribir el archivo de configuración
    config_path = Path('app/config_sqlserver.py')
    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(config_content)
    
    print(f"✅ Archivo de configuración creado: {config_path}")
    
    # Copiar a config.py
    shutil.copy(config_path, 'app/config.py')
    print("✅ Configuración aplicada a app/config.py")

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
            db.engine.execute("SELECT 1")
            print("✅ ¡Conexión Flask/SQLAlchemy exitosa!")
            return True
            
    except Exception as e:
        print(f"❌ Error en conexión Flask: {e}")
        return False

def main():
    """Función principal"""
    
    print("🚀 Script de configuración automática de SQL Server")
    print("=" * 60)
    
    # Paso 1: Probar conexiones
    working_config = test_sql_server_connection()
    
    if not working_config:
        print("\n❌ No se pudo conectar con ninguna configuración.")
        print("🔧 Verifica que:")
        print("   - SQL Server esté funcionando")
        print("   - El puerto esté abierto")
        print("   - Las credenciales sean correctas")
        print("   - El firewall permita la conexión")
        return False
    
    # Paso 2: Crear configuración
    create_config_file(working_config)
    
    # Paso 3: Probar con Flask
    if test_flask_connection():
        print("\n🎉 ¡Configuración completada exitosamente!")
        print("🚀 Puedes ejecutar: python main.py")
        return True
    else:
        print("\n⚠️  Configuración creada pero Flask no pudo conectar.")
        print("🔧 Verifica que las dependencias estén instaladas.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
