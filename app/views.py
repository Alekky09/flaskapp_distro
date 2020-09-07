from app import app
from flask import render_template, redirect, url_for, flash, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from db_classes import User
from forms import LoginForm, RegisterForm


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
    return render_template("index.html")


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