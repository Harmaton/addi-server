from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from routes.imap_route import bp as imap_bp
    from routes.smtp_routes import bp as smtp_bp
    # TODO: Uncomment and update the import once the ai_addy module is created
    # from routes.ai_addy import bp as ai_addy_bp

    app.register_blueprint(imap_bp)
    app.register_blueprint(smtp_bp)
    # app.register_blueprint(ai_addy_bp)

    return app