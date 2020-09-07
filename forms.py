from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length, Regexp, EqualTo
from wtforms.fields.html5 import EmailField

# Form classes which get imported into our markup/server code
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=4, max=15), Regexp('\w+$', message="Username must contain only letters, numbers or underscores.")])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField("Remember me")

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=4, max=15, message="Username must be between 4 and 15 characters long."), Regexp('\w+$', message="Username must contain only letters, numbers or underscores.")])
    email = EmailField("Email", validators=[InputRequired(), Email(message="Invalid email."), Length(max=50)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=80), EqualTo("confirm", message="Passwords must match!")])
    confirm = PasswordField("Confirm Password")