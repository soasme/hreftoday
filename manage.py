# -*- coding: utf-8 -*-

import os
from app.application import create_app
from app.core import db
from app import models
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand

app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)

port = int(os.environ.get('PORT', 5000))
manager.add_command("runserver", Server(host='0.0.0.0', port=port))
manager.add_command('db', MigrateCommand)

@manager.command
def collectstatic():
    print "hello world"


if __name__ == "__main__":
    manager.run()
