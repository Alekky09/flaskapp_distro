from app import app
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

# Initialize database
db = SQLAlchemy(app)

# Database classes
class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

# For creating tables uncomment this and run
# db.create_all()