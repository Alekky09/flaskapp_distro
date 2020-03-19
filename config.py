#This file connects to the init
class Config(object):
    DEBUG = False
    TESTING = False

    # secret module from python will create a good secret key
    # ad8uyrfhsvybrqf
    SECRET_KEY = "20b86a02362baa0490e1065d3b10309a"
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = "False"
    # Database
    DB_NAME = "production-db"
    DB_USERNAME = "root"
    DB_PASSWORD = "example"

    # Uploads folder on the server
    UPLOADS = "/home/username/app/app/static/images/uploads"

    #It will only send cookies if the connection is https secure
    SESSION_COOKIE_SECURE = True


# ProductionConfig is gonna inherit all the attributs from (Config)
class ProductionConfig(Config):
    pass

# DevelopmentConfig will inherit Config too
class DevelopmentConfig(Config):
    DEBUG = True

    DB_NAME = "development-db"
    DB_USERNAME = "root"
    DB_PASSWORD = "example"
    
    # Different folder on the development machine
    UPLOADS = "uploads"

    # On the testing machine the server won't be likely https
    SESSION_COOKIE_SECURE = False

class TestingConfig(Config):
    TESTING = True

    UPLOADS = "/home/username/projects/flask_test/app/app/static/images/uploads"

    SESSION_COOKIE_SECURE = False