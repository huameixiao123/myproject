from flask import Flask
from app.exts import db
from app.views import bp


def create_app():
    app = Flask(__name__)
    app.config.from_object("config")
    app.register_blueprint(bp)
    db.init_app(app)
    return app
