from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from server.routes import imap_routes, smtp_routes, ai_routes
    app.register_blueprint(imap_routes.bp)
    app.register_blueprint(smtp_routes.bp)
    app.register_blueprint(ai_routes.bp)

    return app