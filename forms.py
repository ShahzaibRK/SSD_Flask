from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, Length, Email, Regexp

# Name fields: letters, spaces, hyphen only (simple validation)
name_regex = r"^[A-Za-z\s\-']+$"

class PersonForm(FlaskForm):
    fname = StringField('First Name', validators=[
        DataRequired(),
        Length(min=1, max=100),
        Regexp(name_regex, message="First name must contain only letters, spaces, hyphens or apostrophes")
    ])
    lname = StringField('Last Name', validators=[
        DataRequired(),
        Length(min=1, max=100),
        Regexp(name_regex, message="Last name must contain only letters, spaces, hyphens or apostrophes")
    ])
    email = EmailField('Email', validators=[DataRequired(), Email(), Length(max=200)])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=128)])
    submit = SubmitField('Login')
