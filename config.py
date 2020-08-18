#This file connects to the init
class Config(object):
    DEBUG = False
    TESTING = False

    # secret module from python will create a good secret key
    # ad8uyrfhsvybrqf
    SECRET_KEY = "20b86a02362baa0490e1065d3b10309a"
    SQLALCHEMY_DATABASE_URI = "postgres://msuzhkkhtynoop:7bf7d1ef90a81857f808fe9b81780097ebf13e36a80bcdbb3ed06c12f507c226@ec2-54-75-229-28.eu-west-1.compute.amazonaws.com:5432/dcdvif1ia36hn8"
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