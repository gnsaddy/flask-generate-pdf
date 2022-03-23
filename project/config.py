import os


class BaseConfig:
    """Base configuration"""
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_LOCAL_URL')
    MYSQL_DATABASE_CHARSET = 'utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_PRE_PING = True
    SECRET_KEY = 'pythonsecretforflaskpdf'


class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_LOCAL_URL')
    MYSQL_DATABASE_CHARSET = 'utf8mb4'


class TestingConfig(BaseConfig):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL')
    MYSQL_DATABASE_CHARSET = 'utf8mb4'


class StagingConfig(BaseConfig):
    """Staging configuration"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_STAGE_URL')
    MYSQL_DATABASE_CHARSET = 'utf8mb4'


class ProductionConfig(BaseConfig):
    """Production configuration"""
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_PROD_URL')
    MYSQL_DATABASE_CHARSET = 'utf8mb4'
