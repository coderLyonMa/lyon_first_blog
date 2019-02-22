import os
from blog import create_app, db, mail
from flask_migrate import Migrate
from blog.models import User, Role, Permission, Post, Comment


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role, Permission=Permission,
                mail=mail, Post=Post, Comment=Comment)


@app.cli.command()
def test():
    """Run the unittests"""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)