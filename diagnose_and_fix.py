#!/usr/bin/env python3
"""
Script de diagnóstico y reparación automática para SQL Server
"""

import os
import sys
import subprocess
import socket
from pathlib import Path

def test_network_connectivity():
    """Prueba la conectividad de red"""
    
    print("🌐 Diagnóstico de conectividad de red...")
    print("=" * 50)
    
    # IPs a probar
    ips_to_test = [
        '181.198.42.195',
        '181.198.42.194', 
        '192.168.4.184',
        'localhost',
        '127.0.0.1'
    ]
    
    working_ips = []
    
    for ip in ips_to_test:
        print(f"\n🔍 Probando conectividad a {ip}...")
        try:
            # Ping test
            result = subprocess.run(['ping', '-n', '1', ip], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print(f"✅ Ping exitoso a {ip}")
                working_ips.append(ip)
            else:
                print(f"❌ Ping falló a {ip}")
        except Exception as e:
            print(f"❌ Error en ping a {ip}: {e}")
    
    return working_ips

def test_port_connectivity(ip, port):
    """Prueba la conectividad a un puerto específico"""
    
    print(f"\n🔌 Probando puerto {port} en {ip}...")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((ip, port))
        sock.close()
        
        if result == 0:
            print(f"✅ Puerto {port} abierto en {ip}")
            return True
        else:
            print(f"❌ Puerto {port} cerrado en {ip}")
            return False
    except Exception as e:
        print(f"❌ Error probando puerto {port} en {ip}: {e}")
        return False

def test_sql_server_connection(ip, port, username, password, database):
    """Prueba la conexión a SQL Server"""
    
    print(f"\n🧪 Probando conexión SQL Server a {ip}:{port}...")
    
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
        
        print(f"✅ ¡Conexión SQL Server exitosa!")
        print(f"📊 Versión: {version.split('\\n')[0]}")
        return True
        
    except Exception as e:
        print(f"❌ Error SQL Server: {e}")
        return False

def check_sql_server_services():
    """Verifica los servicios de SQL Server"""
    
    print(f"\n🔧 Verificando servicios de SQL Server...")
    
    try:
        # Verificar servicios de SQL Server
        result = subprocess.run(['sc', 'query', 'MSSQLSERVER'], 
                              capture_output=True, text=True)
        
        if 'RUNNING' in result.stdout:
            print("✅ Servicio SQL Server (MSSQLSERVER) está ejecutándose")
            return True
        else:
            print("❌ Servicio SQL Server (MSSQLSERVER) no está ejecutándose")
            return False
            
    except Exception as e:
        print(f"❌ Error verificando servicios: {e}")
        return False

def create_working_config(ip, port):
    """Crea la configuración que funciona"""
    
    print(f"\n🔧 Creando configuración para {ip}:{port}...")
    
    config_content = f'''# app/config_sqlserver.py
import os
from pathlib import Path

basedir = Path(__file__).parent.parent

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Configuración para SQL Server
    SQL_SERVER_CONFIG = {{
        'server': '{ip}',  # IP del servidor SQL Server
        'port': '{port}',              # Puerto del servidor
        'database': 'Rend_Cultivo',
        'username': 'sa',
        'password': '6509',
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

def main():
    """Función principal de diagnóstico"""
    
    print("🚀 Script de diagnóstico y reparación automática")
    print("=" * 60)
    
    # Paso 1: Verificar servicios
    if not check_sql_server_services():
        print("\n🔧 Intentando iniciar servicio SQL Server...")
        try:
            subprocess.run(['net', 'start', 'MSSQLSERVER'], check=True)
            print("✅ Servicio SQL Server iniciado")
        except:
            print("❌ No se pudo iniciar el servicio SQL Server")
            print("🔧 Verifica que SQL Server esté instalado correctamente")
            return False
    
    # Paso 2: Probar conectividad de red
    working_ips = test_network_connectivity()
    
    if not working_ips:
        print("\n❌ No hay conectividad de red a ninguna IP")
        print("🔧 Verifica tu conexión a internet y configuración de red")
        return False
    
    # Paso 3: Probar puertos
    ports_to_test = [5010, 1433, 1434]
    working_combinations = []
    
    for ip in working_ips:
        for port in ports_to_test:
            if test_port_connectivity(ip, port):
                working_combinations.append((ip, port))
    
    if not working_combinations:
        print("\n❌ No se encontraron puertos abiertos")
        print("🔧 Verifica que SQL Server esté configurado para escuchar en estos puertos")
        return False
    
    # Paso 4: Probar conexiones SQL Server
    for ip, port in working_combinations:
        if test_sql_server_connection(ip, port, 'sa', '6509', 'Rend_Cultivo'):
            print(f"\n🎉 ¡Configuración exitosa encontrada!")
            print(f"📊 IP: {ip}")
            print(f"📊 Puerto: {port}")
            
            # Crear configuración
            create_working_config(ip, port)
            
            print(f"\n🚀 Puedes ejecutar: python main.py")
            return True
    
    print("\n❌ No se pudo conectar a SQL Server con ninguna configuración")
    print("🔧 Verifica que:")
    print("   - SQL Server esté funcionando")
    print("   - Las credenciales sean correctas")
    print("   - La base de datos 'Rend_Cultivo' exista")
    print("   - El usuario 'sa' tenga permisos")
    
    return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
