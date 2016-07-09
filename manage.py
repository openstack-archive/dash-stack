#!../venv/bin/python
import os
from dash import create_app, db
from dash.models import User, Role
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

dash = create_app(os.getenv('DASH_STACK_CONFIG') or 'default')
manager = Manager(dash)
migrate = Migrate(dash, db)


def make_shell_context():
    return dict(dash=dash, db=db, User=User, Role=Role)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()