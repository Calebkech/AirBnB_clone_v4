# app/__init__.py
from flask import Flask, render_template
from .models import db
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
from .models import Users

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    migrate = Migrate(app, db)

    from .routes import main
    from .auth import auth  # Import the auth Blueprint

    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')  # Register the auth Blueprint with a URL prefix

    # Initialize LoginManager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(str(user_id))

    # Error handling
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    return app
