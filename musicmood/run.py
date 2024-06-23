from app import create_app, db
from config import config

app = create_app()

if __name__ == '__main__':
    print("DEBUG mode:", config.DEBUG)
    with app.app_context():
        db.create_all()
    app.run(debug=config.DEBUG)

