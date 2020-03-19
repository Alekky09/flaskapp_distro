from flask import Flask
from flask_bootstrap import Bootstrap

# Start the app
app = Flask(__name__)
# Start Bootstrap
Bootstrap(app)



if app.config["ENV"] == "production":
    app.config.from_object("config.ProductionConfig")

elif app.config["ENV"] == "development":
    app.config.from_object("config.DevelopmentConfig")

else:
    app.config.from_object("config.TestingConfig")


from app import views