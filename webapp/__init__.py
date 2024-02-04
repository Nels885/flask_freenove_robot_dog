import os
import subprocess
import click
import jinja2
from flask import Flask, Blueprint

from constance import config
from constance.settings import CONFIG, CONFIG_FIELDSETS

from .utils import get_state_info, get_sys_info, get_today_date
from .api import api_bp
from .routes import main_bp


class WebApp(object):

    def __init__(self, app: Flask = None):
        if app:
            self.init_app(app)

    def init_app(self, app: Flask):
        self.app = app

        my_loader = jinja2.ChoiceLoader([
            jinja2.FileSystemLoader(['templates']),
            app.jinja_loader,
        ])
        self.app.jinja_loader = my_loader

        self.blueprint = self.create_blueprint()
        self.register_blueprint(self.blueprint)
        self.register_blueprint(api_bp)
        self.register_blueprint(main_bp)

        self.context_processor(get_today_date)
        self.context_processor(get_state_info)
        self.context_processor(get_sys_info)
        return self

    def register_blueprint(self, blueprint: Blueprint):
        self.app.register_blueprint(blueprint)

    def context_processor(self, function: any):
        self.app.context_processor(function)

    def create_blueprint(self, name="webapp", url_prefix="/"):
        blueprint = Blueprint(
            name,
            __name__,
            url_prefix=url_prefix,
            template_folder=f"templates/{name}",
            static_folder=f"static/{name}",
        )
        return blueprint


def create_app(database_uri=None):

    # Initialisze l'application Flask
    app = Flask(__name__)

    # Config options - Make sure you created a 'settings.py' file.
    app.config.from_object(os.environ.get('APP_SETTINGS', 'settings'))
    # To get one variable, tape app.config['MY_VARIABLE']

    WebApp(app)

    config.init_app(app)

    return app

app = create_app()
