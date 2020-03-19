from app import app
from flask import render_template, redirect, url_for, flash, request, jsonify

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Email, Length

import os
from werkzeug.security import check_password_hash, generate_password_hash

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

import xlrd
from sqlalchemy.exc import IntegrityError

#Initialize database
db = SQLAlchemy(app)
#Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

class Order(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    work_order_id = db.Column(db.String(15), unique=True)
    work_order_date = db.Column(db.String(11))
    address = db.Column(db.String(100))
    person_in_charge = db.Column(db.String(50))
    description = db.Column(db.String(300))
    is_completed = db.Column(db.Boolean)
    is_signed = db.Column(db.Boolean)
    is_paid = db.Column(db.Boolean)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Class for the login form
class LoginForm(FlaskForm):
    username = StringField("username", validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField("password", validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField("remember me")

class RegisterForm(FlaskForm):
    username = StringField("username", validators=[InputRequired(), Length(min=4, max=15)])
    email = StringField("email", validators=[InputRequired(), Email(message="Invalid email"), Length(max=50)])
    password = PasswordField("password", validators=[InputRequired(), Length(min=8, max=80)])

class UploadForm(FlaskForm):
    xml_file = FileField("xml_file",validators=[FileRequired(), FileAllowed(["xls", "xlsx"], "Excel spreadsheets only!")])

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods = ["GET", "POST"])
@login_required
def index():
    # Upload is gonna be here
    form = UploadForm()
    
    if form.validate_on_submit():

        # Put the file object(stream) into a var
        xls_object = form.xml_file.data.stream
        
        # Open it as a workbook
        workbook = xlrd.open_workbook(file_contents=xls_object.read())

        sheet = workbook.sheet_by_index(0)

        # Row, column, starting from 0
        # Take values from the cells
        work_order_id = sheet.cell_value(3, 5)
        work_order_date = sheet.cell_value(3, 10)
        address = sheet.cell_value(6, 1)
        person_in_charge = sheet.cell_value(6, 8)
        description = sheet.cell_value(13, 4)

        # Make a new Order object
        new_order = Order(user_id=current_user.get_id(), work_order_id=work_order_id, work_order_date=work_order_date, address=address, person_in_charge=person_in_charge, description=description)
        
        # Save it to the database table
        try:
            db.session.add(new_order)
            db.session.commit()

        except IntegrityError:
            return 'Order already exists!'

    # Selecting the orders of the user for display
    orders = db.session.query(Order).filter_by(user_id=current_user.get_id()).all()
         
    return render_template("index.html", form=form, orders=orders)

@app.route("/update", methods=["POST"])
def update():
    
    order = Order.query.filter_by(id=request.form["order_id"]).first()
    
    def boolify(x):
        if x == "true":
            return True
        else:
            return False

    if request.form["checkbox"] == "is_completed":
        order.is_completed = boolify(request.form["is_checked"])
    
    elif request.form["checkbox"] == "is_signed":
        order.is_signed = boolify(request.form["is_checked"])
    
    else:
        order.is_paid = boolify(request.form["is_checked"])

    db.session.commit()

    return jsonify({"is_completed" : order.is_completed, "is_signed" : order.is_signed, "is_paid" : order.is_paid})

# @main.route("/delete")
# def delete():
#     # Deleting data from a table in sqlalchemy which is connected to the other table
#     order_ids = db.session.query(Order.id).join(Customer).filter(Customer.state == "CA")
    
#     # Seeing how many orders will get deleted and deleting them
#     # You can only delete from one table at a time

#     delete_count - db.session.query(Order).filter(Order.id.in_(order_ids.subquery())).delete(
#         synchronize_session=False
#     )
#     return str(delete_count)

@app.route("/login", methods = ["GET", "POST"])
def login():

    form = LoginForm()

    # If the form is submitted
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                #Log in the user
                login_user(user, remember=form.remember.data)
                #Then redirect
                return redirect(url_for("index"))

        return "Invalid username and/or password"


    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():

    logout_user()
    # Redirect user to login form
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():

    form = RegisterForm()

    if form.validate_on_submit():
        #Hash the password
        hashed_password = generate_password_hash(form.password.data, method="sha256")
        #Create a new user object
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        #Add the user to the db
        try:
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError:
            return "Username/email already taken!"

    return render_template("register.html", form=form)