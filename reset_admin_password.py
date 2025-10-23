#!/usr/bin/env python3
"""
Script para resetear la contraseña del usuario admin
"""

import sys
from pathlib import Path

def reset_admin_password():
    """Resetea la contraseña del usuario admin"""
    
    print("🔧 Reseteando contraseña del usuario admin...")
    print("=" * 50)
    
    try:
        # Importar la aplicación Flask
        sys.path.append('app')
        from app import create_app
        from app.models import db, Usuario
        from werkzeug.security import generate_password_hash
        
        app = create_app()
        
        with app.app_context():
            # Buscar el usuario admin
            admin_user = Usuario.query.filter_by(username='admin').first()
            
            if admin_user:
                print(f"✅ Usuario admin encontrado: {admin_user.username}")
                print(f"📧 Email: {admin_user.email}")
                print(f"🔑 Rol: {admin_user.rol}")
                
                # Resetear contraseña a 'admin'
                new_password = 'admin'
                admin_user.password_hash = generate_password_hash(new_password)
                
                db.session.commit()
                
                print(f"✅ Contraseña reseteada a: {new_password}")
                print("🚀 Ahora puedes hacer login con:")
                print(f"   Usuario: admin")
                print(f"   Contraseña: admin")
                
                return True
            else:
                print("❌ Usuario admin no encontrado")
                return False
                
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def create_new_admin():
    """Crea un nuevo usuario admin si no existe"""
    
    print("\n🔧 Creando nuevo usuario admin...")
    print("=" * 50)
    
    try:
        # Importar la aplicación Flask
        sys.path.append('app')
        from app import create_app
        from app.models import db, Usuario
        from werkzeug.security import generate_password_hash
        
        app = create_app()
        
        with app.app_context():
            # Verificar si ya existe
            existing_admin = Usuario.query.filter_by(username='admin').first()
            if existing_admin:
                print("✅ Usuario admin ya existe")
                return True
            
            # Crear nuevo usuario admin
            new_admin = Usuario(
                username='admin',
                email='admin@tessacorporation.com',
                password_hash=generate_password_hash('admin'),
                rol='admin',
                activo=True
            )
            
            db.session.add(new_admin)
            db.session.commit()
            
            print("✅ Nuevo usuario admin creado:")
            print(f"   Usuario: admin")
            print(f"   Contraseña: admin")
            print(f"   Email: admin@tessacorporation.com")
            print(f"   Rol: admin")
            
            return True
                
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Función principal"""
    
    print("🚀 Script de reseteo de contraseña admin")
    print("=" * 60)
    
    # Intentar resetear contraseña
    if reset_admin_password():
        print("\n🎉 ¡Contraseña reseteada exitosamente!")
        return True
    
    # Si no funciona, crear nuevo admin
    print("\n🔄 Intentando crear nuevo usuario admin...")
    if create_new_admin():
        print("\n🎉 ¡Nuevo usuario admin creado!")
        return True
    
    print("\n❌ No se pudo resetear ni crear usuario admin")
    return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
