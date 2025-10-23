#!/usr/bin/env python3
"""
Script para encontrar las credenciales correctas de SQL Server
"""

import os
import sys
import subprocess
from pathlib import Path

def test_credentials(ip, port, username, password, database):
    """Prueba credenciales específicas"""
    
    try:
        import pymssql
        
        conn = pymssql.connect(
            server=ip,
            port=port,
            user=username,
            password=password,
            database=database,
            timeout=10
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT @@VERSION")
        version = cursor.fetchone()[0]
        conn.close()
        
        print(f"✅ ¡Credenciales correctas encontradas!")
        print(f"📊 Usuario: {username}")
        print(f"📊 Contraseña: {password}")
        print(f"📊 Versión: {version.split('\\n')[0]}")
        return True
        
    except Exception as e:
        print(f"❌ Error con {username}:{password}: {e}")
        return False

def find_working_credentials():
    """Busca las credenciales que funcionan"""
    
    print("🔍 Buscando credenciales correctas de SQL Server...")
    print("=" * 60)
    
    # IPs que funcionan (del diagnóstico anterior)
    working_ips = [
        '181.198.42.195',
        '181.198.42.194', 
        '192.168.4.184',
        'localhost',
        '127.0.0.1'
    ]
    
    # Credenciales a probar
    credentials_to_test = [
        {'username': 'sa', 'password': '6509'},
        {'username': 'sa', 'password': r'$DataWareHouse$'},
        {'username': 'sa', 'password': 'DataWareHouse'},
        {'username': 'sa', 'password': 'admin'},
        {'username': 'sa', 'password': '123456'},
        {'username': 'sa', 'password': 'password'},
        {'username': 'sa', 'password': 'sa'},
        {'username': 'sa', 'password': ''},
        {'username': 'admin', 'password': '6509'},
        {'username': 'admin', 'password': r'$DataWareHouse$'},
        {'username': 'admin', 'password': 'admin'},
        {'username': 'root', 'password': '6509'},
        {'username': 'root', 'password': r'$DataWareHouse$'},
    ]
    
    # Puerto que funciona
    port = 5010
    database = 'Rend_Cultivo'
    
    for ip in working_ips:
        print(f"\n🌐 Probando IP: {ip}")
        print("-" * 40)
        
        for cred in credentials_to_test:
            print(f"🔑 Probando {cred['username']}:{cred['password']}...")
            
            if test_credentials(ip, port, cred['username'], cred['password'], database):
                return {
                    'ip': ip,
                    'port': port,
                    'username': cred['username'],
                    'password': cred['password'],
                    'database': database
                }
    
    return None

def create_working_config(working_config):
    """Crea la configuración que funciona"""
    
    print(f"\n🔧 Creando configuración con credenciales correctas...")
    
    config_content = f'''# app/config_sqlserver.py
import os
from pathlib import Path

basedir = Path(__file__).parent.parent

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Configuración para SQL Server
    SQL_SERVER_CONFIG = {{
        'server': '{working_config['ip']}',  # IP del servidor SQL Server
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
    import shutil
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
            with db.engine.connect() as connection:
                connection.execute(db.text("SELECT 1"))
            print("✅ ¡Conexión Flask/SQLAlchemy exitosa!")
            return True
            
    except Exception as e:
        print(f"❌ Error en conexión Flask: {e}")
        return False

def main():
    """Función principal"""
    
    print("🚀 Script para encontrar credenciales correctas de SQL Server")
    print("=" * 70)
    
    # Buscar credenciales que funcionan
    working_config = find_working_credentials()
    
    if not working_config:
        print("\n❌ No se encontraron credenciales que funcionen.")
        print("🔧 Posibles soluciones:")
        print("   - Verifica que SQL Server esté configurado correctamente")
        print("   - Verifica que el usuario 'sa' esté habilitado")
        print("   - Verifica que la contraseña sea correcta")
        print("   - Verifica que la base de datos 'Rend_Cultivo' exista")
        return False
    
    # Crear configuración
    create_working_config(working_config)
    
    # Probar con Flask
    if test_flask_connection():
        print("\n🎉 ¡Configuración completada exitosamente!")
        print("🚀 Puedes ejecutar: python main.py")
        return True
    else:
        print("\n⚠️  Credenciales encontradas pero Flask no pudo conectar.")
        print("🔧 Verifica que las dependencias estén instaladas.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
