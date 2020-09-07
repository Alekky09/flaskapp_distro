#This file connects to the init
class Config(object):
    DEBUG = False
    TESTING = False

    # secret module from python will create a good secret key
    # ad8uyrfhsvybrqf
    # Fill in SECRET_KEY and the DATABASE_URI before starting
    SECRET_KEY = "11"
    SQLALCHEMY_DATABASE_URI = "11"
    SQLALCHEMY_TRACK_MODIFICATIONS = "False"

    #It will only send cookies if the connection is https secure
    SESSION_COOKIE_SECURE = False


# ProductionConfig is gonna inherit all the attributes from (Config)
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