from flask import Flask

from app.api import api_bp
from app.extensions import (
    DB_MIGRATER,
    JWT,
    SQL_DB,
)
from config import Base


def create_app(config = None):
    if config is None:
        config = Base

    app = Flask(__name__)
    app.config.from_object(config)

    SQL_DB.init_app(app)
    DB_MIGRATER.init_app(app, SQL_DB)
    JWT.init_app(app)

    app.register_blueprint(api_bp, url_prefix='/api')

    return app
