# -*- coding: utf-8 -*-

import os
from app.application import create_app
from flask_script import Manager, Server

app = create_app()
manager = Manager(app)

port = int(os.environ.get('PORT', 5000))
manager.add_command("runserver", Server(host='0.0.0.0', port=port))

@manager.command
def collectstatic():
    print "hello world"


if __name__ == "__main__":
    manager.run()
