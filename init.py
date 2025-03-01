from flask import Flask
from config import Config
from services.server_service import ServerService

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize WireGuard server
    try:
        ServerService().initialize_server()
    except Exception as e:
        app.logger.error(f"Server initialization failed: {str(e)}")
    
    # Register blueprints
    from controllers.client_controller import client_bp
    app.register_blueprint(client_bp)
    
    return app