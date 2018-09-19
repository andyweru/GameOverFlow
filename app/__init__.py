from flask import Flask
from flask_bootstrap import Bootstrap
from config import config_options
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

bootstrap = Bootstrap()
db = SQLAlchemy()

login_mananger = LoginManager()
login_mananger.session_protection = 'strong'
login_mananger.login_view = 'auth.login'

def create_app(config_name):

    app = Flask(__name__)
    db = SQLAlchemy()

    # Register blueprints
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Creating the app configurations
    app.config.from_object(config_options[config_name])

    # Initializing flask extensions 
    bootstrap.init_app(app)
    db.init_app(app)
    login_mananger.init_app(app)

    # Will and the views and forms

    return app