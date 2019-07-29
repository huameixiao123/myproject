from flask import Flask

from exts import db
from views import bp
# from flask_wtf import CSRFProtect
from flask_ckeditor import CKEditor

def create_app():
    app = Flask(__name__)
    app.config.from_object("config")
    app.register_blueprint(bp)
    # CSRFProtect(app)
    ck_editor = CKEditor(app)
    db.init_app(app)
    return app

app = create_app()

if __name__ == '__main__':
    app.run()
