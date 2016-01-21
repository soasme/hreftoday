# -*- coding: utf-8 -*-

from app.application import create_app
from flask_script import Manager

app = create_app()
manager = Manager(app)

@manager.command
def collectstatic():
    print "hello world"


if __name__ == "__main__":
    manager.run()
