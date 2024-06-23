from flask import Flask, render_template
from .models import db
from flask_migrate import Migrate
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    migrate = Migrate(app, db)

    with app.app_context():
        db.create_all()
        
    from .routes import main
    app.register_blueprint(main)

    # Error handling
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404
    
    return app
