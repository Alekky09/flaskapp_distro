from app import app
from flask import render_template, redirect, url_for, flash, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from sqlalchemy.exc import IntegrityError

from db_classes import User, Order, db
from forms import LoginForm, RegisterForm, UploadForm

import xlrd


#Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message_category = "error"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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
    # Initialize form for uploading spreadsheets
    form = UploadForm()

    # Selecting the user and their orders
    username = db.session.query(User.username).filter_by(id=current_user.get_id()).first()   
    rows = db.session.query(Order).filter_by(user_id=current_user.get_id()).all()

    # Sorting the orders by their level of completion
    orders = []
    dikt = {
        0: [],
        1: [],
        2: [],
        3: []
    }
    for i in range(len(rows)):
        row = rows[i]
        j = row.is_completed + row.is_signed + row.is_paid
        dikt[j].append(row)

    orders = dikt[0] + dikt[1] + dikt[2] + dikt[3]

    # If a new excel file is submitted
    if form.validate_on_submit():
        
        # Put the file object(stream) into a var
        xls_object = form.xml_file.data.stream
        
        # Open it as a workbook
        workbook = xlrd.open_workbook(file_contents=xls_object.read())

        sheet = workbook.sheet_by_index(0)

        # Row, column, starting from 0
        # Take values from the cells
        # Fix excel turning number into floats
        if isinstance(sheet.cell_value(3, 5), float):
            work_order_id = str(int(sheet.cell_value(3, 5)))
        else:
            work_order_id = str(sheet.cell_value(3, 5))

        work_order_date = sheet.cell_value(3, 10)
        address = sheet.cell_value(6, 1)
        person_in_charge = sheet.cell_value(6, 8)
        description = sheet.cell_value(13, 4)

        # Make a new Order object
        new_order = Order(\
            user_id=current_user.get_id(),\
            work_order_id=work_order_id,\
            work_order_date=work_order_date,\
            address=address,\
            person_in_charge=person_in_charge,\
            description=description)
        
        order_exists = db.session.query(Order)\
            .filter_by(user_id=current_user.get_id(), work_order_id=work_order_id)\
            .first()

        # If the order doesnt exist already
        if not order_exists:               
            # Save it to the database table
            db.session.add(new_order)
            db.session.commit()

        else:
            flash("Order already exists!", "error")

        return redirect(url_for('index'))

    return render_template("index.html", form=form, orders=orders, username=username)

# Route for updating order completion fields
@app.route("/update", methods=["POST"])
@login_required
def update():

    # Query for the order selected
    order = Order.query.filter_by(id=request.form["order_id"]).first()

    # Checking which field is being updated
    # == operand will return True if left and right are equal
    if request.form["checkbox"] == "is_completed":
        order.is_completed = request.form["is_checked"] == "true"
    
    elif request.form["checkbox"] == "is_signed":
        order.is_signed = request.form["is_checked"] == "true"
    
    else:
        order.is_paid = request.form["is_checked"] == "true"
        
    db.session.commit()

    # Return the updated data to the template
    return jsonify({"is_completed" : order.is_completed, "is_signed" : order.is_signed, "is_paid" : order.is_paid})

# Route for updating the financing data fields
@app.route("/finance", methods=["POST"])
@login_required
def finance():

    # Query for the order selected
    order = Order.query.filter_by(id=request.form["order_id"]).first()

    # Check which type of finance has been updated
    if request.form["type"] == "income-number":
        order.income = int(request.form["number"])
    elif request.form["type"] == "expenses-number":
        order.expenses = int(request.form["number"])
    else:
        flash("Invalid number!", "error")

    # Calculate total finances for the order
    order.total = order.income - order.expenses

    db.session.commit()

    return jsonify({"value" : request.form["number"], "total" : order.total})


@app.route("/login", methods = ["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("index"))
    
    form = LoginForm()

    # If the form is submitted
    if form.validate_on_submit():
        # Search for the user
        user = User.query.filter_by(username=form.username.data).first()

        if user:
            if check_password_hash(user.password, form.password.data):
                #Log in the user
                login_user(user, remember=form.remember.data)
                flash("Welcome!", "success")
                #Then redirect
                return redirect(url_for("index"))

        flash("Invalid username and/or password!", "error")

    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():

    logout_user()
    flash("See you next time!", "success")
    # Redirect user to login form
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():

    if current_user.is_authenticated:
        return redirect(url_for("index"))
    
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
            flash("You have successfully registered!", "success")
            return redirect(url_for("login"))

        except IntegrityError:
            flash ("Username/email already taken!", "error")

    return render_template("register.html", form=form)