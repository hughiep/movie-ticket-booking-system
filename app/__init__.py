# Application factory
# Create the application object as an instance of class Flask imported from the flask package.

import os
from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__)

    # Load the default configuration
    app.config.from_mapping(SECRET_KEY='dev',)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/')
    def index():
        return 'Hello, World!'
    
    from . import db
    db.init_app(app)

    from . import auth,movies
    app.register_blueprint(auth.bp)
    app.register_blueprint(movies.bp)

    return app

