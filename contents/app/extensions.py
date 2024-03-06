import logging
import os
from logging.handlers import RotatingFileHandler

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

DB_MIGRATER = Migrate()
SQL_DB = SQLAlchemy()

os.makedirs("logs", exist_ok=True)
app_log_handler = RotatingFileHandler('logs/app.log', maxBytes=1000000, backupCount=30, encoding="UTF-8")

LOGGER = logging.getLogger('contents-server')
LOGGER.setLevel(logging.DEBUG)
LOGGER.addHandler(app_log_handler)
