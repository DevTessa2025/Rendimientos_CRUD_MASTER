#!/usr/bin/env python3
"""
Script para probar la conexión a SQL Server
"""

import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from app import create_app, db
    from app.models import Usuario, Finca, Area, Supervisor, Codigo
    
    print("🔌 Probando conexión a SQL Server...")
    print("=" * 50)
    
    app = create_app()
    
    with app.app_context():
        # Probar conexión básica
        print("1️⃣ Verificando conexión...")
        result = db.session.execute(db.text("SELECT @@VERSION"))
        version = result.fetchone()[0]
        version_line = version.split('\n')[0]
        print(f"✅ Conexión exitosa!")
        print(f"   SQL Server: {version_line}")
        
        # Verificar tablas
        print("\n2️⃣ Verificando tablas...")
        result = db.session.execute(db.text("""
            SELECT TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_NAME LIKE 'app_%' 
            AND TABLE_TYPE = 'BASE TABLE'
            ORDER BY TABLE_NAME
        """))
        
        tables = [row[0] for row in result]
        print(f"✅ Tablas encontradas: {len(tables)}")
        for table in tables:
            print(f"   - {table}")
        
        # Contar registros
        print("\n3️⃣ Contando registros...")
        print(f"   📊 Fincas: {Finca.query.count()}")
        print(f"   👤 Usuarios: {Usuario.query.count()}")
        print(f"   👨‍🌾 Supervisores: {Supervisor.query.count()}")
        print(f"   🗺️  Áreas: {Area.query.count()}")
        print(f"   🔢 Códigos: {Codigo.query.count()}")
        
        # Verificar usuario admin
        print("\n4️⃣ Verificando usuario admin...")
        admin = Usuario.query.filter_by(username='admin').first()
        if admin:
            print(f"✅ Usuario admin encontrado")
            print(f"   Email: {admin.email}")
            print(f"   Rol: {admin.rol}")
            print(f"   Activo: {admin.activo}")
        else:
            print("❌ Usuario admin no encontrado")
        
        # Verificar finca ejemplo
        print("\n5️⃣ Verificando finca ejemplo...")
        finca = Finca.query.first()
        if finca:
            print(f"✅ Finca encontrada")
            print(f"   Nombre: {finca.nombre}")
            print(f"   Ubicación: {finca.ubicacion}")
            print(f"   Activa: {finca.activa}")
        else:
            print("❌ No hay fincas registradas")
        
        print("\n" + "=" * 50)
        print("🎉 ¡Conexión exitosa a SQL Server!")
        print("\n📋 Credenciales para iniciar sesión:")
        print(f"   Email: {admin.email if admin else 'admin@agricultura.com'}")
        print("   Password: admin123")
        print("\n🚀 Ejecuta 'python main.py' para iniciar la aplicación")
        
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    print("💡 Asegúrate de haber instalado todas las dependencias:")
    print("   pip install -r requirements.txt")
    sys.exit(1)

except Exception as e:
    print(f"❌ Error de conexión: {e}")
    print("\n🔧 Posibles soluciones:")
    print("1. Verifica que el servidor SQL Server esté accesible")
    print("2. Verifica las credenciales en app/config.py")
    print("3. Verifica que el firewall permita la conexión")
    print("4. Verifica que las tablas existan en la base de datos")
    sys.exit(1)

