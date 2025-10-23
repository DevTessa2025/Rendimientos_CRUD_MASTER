#!/usr/bin/env python3
"""
Script para cambiar entre SQLite y SQL Server
"""

import os
import shutil
from pathlib import Path

def switch_to_sqlite():
    """Cambiar a SQLite para desarrollo local"""
    print("🔄 Cambiando a SQLite...")
    
    # Backup del archivo actual
    shutil.copy('app/config.py', 'app/config.py.backup')
    
    # Leer el archivo SQLite
    with open('app/config_sqlite.py', 'r') as f:
        content = f.read()
    
    # Escribir al archivo principal
    with open('app/config.py', 'w') as f:
        f.write(content)
    
    print("✅ Cambiado a SQLite")
    print("💡 Para volver a SQL Server, ejecuta: python switch_database.py --sqlserver")

def switch_to_sqlserver():
    """Cambiar a SQL Server"""
    print("🔄 Cambiando a SQL Server...")
    
    # Backup del archivo actual
    shutil.copy('app/config.py', 'app/config.py.backup')
    
    # Leer el archivo SQL Server
    with open('app/config_sqlserver.py', 'r') as f:
        content = f.read()
    
    # Escribir al archivo principal
    with open('app/config.py', 'w') as f:
        f.write(content)
    
    print("✅ Cambiado a SQL Server")
    print("💡 Para volver a SQLite, ejecuta: python switch_database.py --sqlite")

def main():
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '--sqlserver':
            switch_to_sqlserver()
        elif sys.argv[1] == '--sqlite':
            switch_to_sqlite()
        else:
            print("❌ Opción no válida")
            print("💡 Usa: --sqlite o --sqlserver")
    else:
        print("🔧 Selector de Base de Datos")
        print("=" * 40)
        print("1. SQLite (Desarrollo local)")
        print("2. SQL Server (Producción)")
        print()
        choice = input("Selecciona una opción (1 o 2): ")
        
        if choice == '1':
            switch_to_sqlite()
        elif choice == '2':
            switch_to_sqlserver()
        else:
            print("❌ Opción no válida")

if __name__ == '__main__':
    main()
