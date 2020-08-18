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

class Order(UserMixin, db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    work_order_id = db.Column(db.String(15))
    work_order_date = db.Column(db.String(11))
    address = db.Column(db.String(100))
    person_in_charge = db.Column(db.String(50))
    description = db.Column(db.String(300))
    is_completed = db.Column(db.Boolean, default=False)
    is_signed = db.Column(db.Boolean, default=False)
    is_paid = db.Column(db.Boolean, default=False)
    expenses = db.Column(db.Integer, default=0)
    income = db.Column(db.Integer, default=0)
    total = db.Column(db.Integer, default=0)

# For creating tables uncomment this and run
# db.create_all()