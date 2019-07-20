
from flask_migrate import MigrateCommand, Migrate
from flask_script import Manager
from exts import db
from book import create_app


app = create_app()


manage = Manager(app)

Migrate(app, db)
manage.add_command("db", MigrateCommand)



if __name__ == '__main__':
    manage.run()
