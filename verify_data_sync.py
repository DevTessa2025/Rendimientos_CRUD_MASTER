#!/usr/bin/env python3
"""
Script para verificar que los datos se están guardando en SQL Server
"""

import sys
from pathlib import Path

def verify_data_sync():
    """Verifica que los datos se están guardando en SQL Server"""
    
    print("🔍 Verificando sincronización de datos con SQL Server...")
    print("=" * 60)
    
    try:
        # Importar la aplicación Flask
        sys.path.append('app')
        from app import create_app
        from app.models import db, Usuario, Finca, Area, Supervisor, Codigo
        from sqlalchemy import text
        
        app = create_app()
        
        with app.app_context():
            print("✅ Conexión a SQL Server establecida")
            
            # Verificar usuarios
            usuarios = Usuario.query.all()
            print(f"\n👥 USUARIOS ({len(usuarios)} registros):")
            for usuario in usuarios:
                print(f"   - {usuario.username} ({usuario.email}) - Rol: {usuario.rol} - Activo: {usuario.activo}")
            
            # Verificar fincas
            fincas = Finca.query.all()
            print(f"\n🏡 FINCAS ({len(fincas)} registros):")
            for finca in fincas:
                print(f"   - {finca.nombre} - Ubicación: {finca.ubicacion} - Activa: {finca.activa}")
            
            # Verificar áreas
            areas = Area.query.all()
            print(f"\n🌱 ÁREAS ({len(areas)} registros):")
            for area in areas:
                supervisor_nombre = area.supervisor.nombre if area.supervisor else "Sin supervisor"
                print(f"   - {area.nombre} - Finca: {area.finca.nombre} - Supervisor: {supervisor_nombre}")
            
            # Verificar supervisores
            supervisores = Supervisor.query.all()
            print(f"\n👨‍💼 SUPERVISORES ({len(supervisores)} registros):")
            for supervisor in supervisores:
                print(f"   - {supervisor.nombre} - Clave: {supervisor.clave_acceso} - Activo: {supervisor.activo}")
            
            # Verificar códigos
            codigos = Codigo.query.all()
            print(f"\n🔢 CÓDIGOS ({len(codigos)} registros):")
            for codigo in codigos[:10]:  # Mostrar solo los primeros 10
                area_nombre = codigo.area.nombre if codigo.area else "Sin área"
                print(f"   - {codigo.codigo} - Persona: {codigo.nombre_persona} - Área: {area_nombre}")
            
            if len(codigos) > 10:
                print(f"   ... y {len(codigos) - 10} códigos más")
            
            # Verificar tablas directamente en SQL Server
            print(f"\n📊 VERIFICACIÓN DIRECTA EN SQL SERVER:")
            
            # Contar registros en cada tabla
            tables_info = [
                ("app_usuario", "Usuarios"),
                ("app_finca", "Fincas"),
                ("app_area", "Áreas"),
                ("app_supervisor", "Supervisores"),
                ("app_codigo", "Códigos")
            ]
            
            for table_name, display_name in tables_info:
                try:
                    result = db.session.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
                    count = result.fetchone()[0]
                    print(f"   - {display_name}: {count} registros")
                except Exception as e:
                    print(f"   - {display_name}: Error - {e}")
            
            print(f"\n✅ Verificación completada")
            return True
                
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_data_creation():
    """Prueba creando datos de ejemplo"""
    
    print("\n🧪 Probando creación de datos...")
    print("=" * 50)
    
    try:
        # Importar la aplicación Flask
        sys.path.append('app')
        from app import create_app
        from app.models import db, Finca
        from datetime import datetime
        
        app = create_app()
        
        with app.app_context():
            # Crear una finca de prueba
            finca_prueba = Finca(
                nombre="Finca de Prueba",
                ubicacion="Ubicación de Prueba",
                descripcion="Finca creada para probar sincronización",
                activa=True,
                fecha_creacion=datetime.now()
            )
            
            db.session.add(finca_prueba)
            db.session.commit()
            
            print("✅ Finca de prueba creada exitosamente")
            print(f"   - ID: {finca_prueba.id}")
            print(f"   - Nombre: {finca_prueba.nombre}")
            print(f"   - Ubicación: {finca_prueba.ubicacion}")
            
            return True
                
    except Exception as e:
        print(f"❌ Error creando datos de prueba: {e}")
        return False

def main():
    """Función principal"""
    
    print("🚀 Script de verificación de sincronización de datos")
    print("=" * 70)
    
    # Verificar datos existentes
    if verify_data_sync():
        print("\n🎉 ¡Datos verificados exitosamente!")
        
        # Probar creación de datos
        if test_data_creation():
            print("\n🎉 ¡Creación de datos funcionando!")
            print("✅ La aplicación está guardando datos en SQL Server correctamente")
        else:
            print("\n⚠️  Hay problemas con la creación de datos")
    else:
        print("\n❌ Hay problemas con la sincronización de datos")

if __name__ == "__main__":
    main()
