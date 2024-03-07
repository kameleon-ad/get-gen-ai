import os


class Config:
    TESTING = False


class DevConfig(Config):
    SECRET_KEY = os.getenv('SECRET_KEY')
    POSTGRES_HOST = os.getenv('POSTGRES_HOST')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT')
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_DATABASE = os.getenv('POSTGRES_DATABASE')

    AUTH_ENDPOINT = os.getenv('AUTH_ENDPOINT')

    SQLALCHEMY_DATABASE_URI = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DATABASE}'


class ProdConfig(Config):
    SECRET_KEY = os.getenv('SECRET_KEY')
    POSTGRES_HOST = os.getenv('POSTGRES_HOST')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT')
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_DATABASE = os.getenv('POSTGRES_DATABASE')

    AUTH_ENDPOINT = os.getenv('AUTH_ENDPOINT')

    SQLALCHEMY_DATABASE_URI = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DATABASE}'


class TestConfig(Config):
    TESTING = True
    AUTH_ENDPOINT = ''
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
