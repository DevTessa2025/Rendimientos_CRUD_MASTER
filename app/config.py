import os
from pathlib import Path

# Obtener la ruta absoluta del directorio del proyecto
basedir = Path(__file__).parent.parent

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Configuración para SQL Server
    SQL_SERVER_CONFIG = {
        'server': '181.198.42.195',
        'port': '5010',
        'database': 'Rend_Cultivo',
        'username': 'sa',
        'password': '6509',
        'driver': 'ODBC Driver 17 for SQL Server'
    }
    
    # URL de conexión para SQL Server usando pymssql (más compatible)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or (
        f"mssql+pymssql://{SQL_SERVER_CONFIG['username']}:{SQL_SERVER_CONFIG['password']}"
        f"@{SQL_SERVER_CONFIG['server']}:{SQL_SERVER_CONFIG['port']}/{SQL_SERVER_CONFIG['database']}"
    )
    
    # Fallback a SQLite para desarrollo local
    SQLALCHEMY_DATABASE_URI_LOCAL = f'sqlite:///{basedir}/instance/agricultura.db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
