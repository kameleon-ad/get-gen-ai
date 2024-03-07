from flask import Flask

from app.api import api_bp
from app.extensions import (
    DB_MIGRATER,
    SQL_DB,
)


def create_app(config=None):
    if config is None:
        config = 'config.DevConfig'

    app = Flask(__name__)
    app.config.from_object(config)

    SQL_DB.init_app(app)
    DB_MIGRATER.init_app(app, SQL_DB)

    app.register_blueprint(api_bp, url_prefix='/api')

    return app
