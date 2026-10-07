from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.login_message_category = "warning"

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    db.init_app(app)
    login_manager.init_app(app)
    from .routes import register_routes
    register_routes(app)
    with app.app_context():
        db.create_all()
        from .schema_sync import synchronize_schema
        synchronize_schema(db)
        from .seed import seed_database
        seed_database()
    return app
