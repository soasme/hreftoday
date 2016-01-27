# -*- coding: utf-8 -*-

import os
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from app.application import create_app
from app.core import db
from app.commands.service import Service
from app import models



application = create_app()
manager = Manager(application)
migrate = Migrate(application, db)

port = int(os.environ.get('PORT', 5000))
manager.add_command("runserver", Server(host='0.0.0.0', port=port))
manager.add_command('db', MigrateCommand)
manager.add_command('service', Service)

@manager.command
def collectstatic():
    print "hello world"


if __name__ == "__main__":
    manager.run()
