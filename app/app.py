from flask import Flask
from .extensions import *
from .resources import api_bp


def create_app(setting_module: str | None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)

    api.init_app(app)
    cors.init_app(app)
    jwt.init_app(app)
    mi.init_app(app)
    principal.init_app(app)
    sql.init_app(app)
    ma.init_app(app)

    app.config.from_object(setting_module)
    app.url_map.strict_slashes = False

    if app.config.get('TESTING', True):
        print(" * Running in testing mode")
        app.config.from_envvar('APP_TESTING_SETTINGS', silent=False)
    elif app.config.get('DEVELOPMENT', True):
        print(" * Running in development mode")
        app.config.from_envvar('APP_DEVELOPMENT_SETTINGS', silent=False)
    else:
        print(" * Running in production mode")
        app.config.from_envvar('APP_PRODUCTION_SETTINGS', silent=False)

    app.register_blueprint(api_bp)

    return app
