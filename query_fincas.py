#!/usr/bin/env python3
"""
Script para consultar fincas desde Python/Flask
"""

import sys
from pathlib import Path

def query_fincas():
    """Consulta fincas usando Flask/SQLAlchemy"""
    
    print("🔍 Consultando fincas desde Flask/SQLAlchemy...")
    print("=" * 60)
    
    try:
        # Importar la aplicación Flask
        sys.path.append('app')
        from app import create_app
        from app.models import db, Finca, Area
        from sqlalchemy import text
        
        app = create_app()
        
        with app.app_context():
            print("✅ Conexión establecida")
            
            # Consulta básica de fincas
            fincas = Finca.query.all()
            print(f"\n📊 FINCAS ENCONTRADAS: {len(fincas)}")
            print("-" * 50)
            
            for finca in fincas:
                print(f"ID: {finca.id}")
                print(f"Nombre: {finca.nombre}")
                print(f"Ubicación: {finca.ubicacion}")
                print(f"Descripción: {finca.descripcion}")
                print(f"Activa: {finca.activa}")
                print(f"Fecha creación: {finca.fecha_creacion}")
                print("-" * 30)
            
            # Consulta con áreas
            print(f"\n📊 FINCAS CON ÁREAS:")
            print("-" * 50)
            
            for finca in fincas:
                areas = Area.query.filter_by(finca_id=finca.id).all()
                print(f"Finca: {finca.nombre}")
                print(f"Áreas: {len(areas)}")
                for area in areas:
                    print(f"  - {area.nombre}")
                print("-" * 30)
            
            return True
                
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def query_fincas_sql():
    """Consulta fincas usando SQL directo"""
    
    print(f"\n🔍 Consultando fincas con SQL directo...")
    print("=" * 60)
    
    try:
        # Importar la aplicación Flask
        sys.path.append('app')
        from app import create_app
        from app.models import db
        from sqlalchemy import text
        
        app = create_app()
        
        with app.app_context():
            # Consulta SQL directa
            query = """
            SELECT 
                f.id,
                f.nombre,
                f.ubicacion,
                f.descripcion,
                f.activa,
                f.fecha_creacion,
                COUNT(a.id) as total_areas
            FROM app_finca f
            LEFT JOIN app_area a ON f.id = a.finca_id
            GROUP BY f.id, f.nombre, f.ubicacion, f.descripcion, f.activa, f.fecha_creacion
            ORDER BY f.nombre
            """
            
            result = db.session.execute(text(query))
            fincas = result.fetchall()
            
            print(f"📊 FINCAS CON ÁREAS (SQL directo): {len(fincas)}")
            print("-" * 50)
            
            for finca in fincas:
                print(f"ID: {finca.id}")
                print(f"Nombre: {finca.nombre}")
                print(f"Ubicación: {finca.ubicacion}")
                print(f"Activa: {finca.activa}")
                print(f"Total áreas: {finca.total_areas}")
                print(f"Fecha creación: {finca.fecha_creacion}")
                print("-" * 30)
            
            return True
                
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Función principal"""
    
    print("🚀 Script de consulta de fincas")
    print("=" * 70)
    
    # Consultar fincas con Flask/SQLAlchemy
    if query_fincas():
        print("\n✅ Consulta Flask/SQLAlchemy exitosa")
    
    # Consultar fincas con SQL directo
    if query_fincas_sql():
        print("\n✅ Consulta SQL directa exitosa")
    
    print("\n🎉 ¡Consultas completadas!")

if __name__ == "__main__":
    main()
