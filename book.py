from flask import Flask

import config
from exts import db
from views import bp
from flask_wtf import CSRFProtect


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    app.register_blueprint(bp)
    # CSRFProtect(app)
    db.init_app(app)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
