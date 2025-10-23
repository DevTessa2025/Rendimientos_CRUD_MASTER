from flask import Flask
from app.config import config
from app.models import db

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Inicializar extensiones
    db.init_app(app)
    
    # Registrar blueprints
    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.usuarios import usuarios_bp
    from app.routes.fincas import fincas_bp
    from app.routes.areas import areas_bp
    from app.routes.supervisores import supervisores_bp
    from app.routes.codigos import codigos_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(fincas_bp)
    app.register_blueprint(areas_bp)
    app.register_blueprint(supervisores_bp)
    app.register_blueprint(codigos_bp)
    
    return app
