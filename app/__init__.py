from flask import Flask
from config import Config
from app.extensions import db, migrate

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Setup middleware
    from app.middleware import setup_logging, setup_request_id
    from app.middleware.security import setup_security_headers, setup_cors
    
    setup_logging(app)
    setup_request_id(app)
    setup_security_headers(app)
    setup_cors(app)

    # Register error handlers
    from app.errors import register_error_handlers
    register_error_handlers(app)

    # Register Blueprints
    from app.routes.main import main_bp
    from app.routes.health import health_bp
    from app.routes.api import api_v1_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(health_bp)
    app.register_blueprint(api_v1_bp)

    # Import models so Flask-Migrate can detect them
    from app import models

    app.logger.info('Application initialized successfully')

    return app
