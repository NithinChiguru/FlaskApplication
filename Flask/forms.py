from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, EmailField, DateField, TimeField
from wtforms.validators import InputRequired


class LoginForm(Form):
    username = StringField('UserName', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')


class RegistrationForm(Form):
    username = StringField('Username', validators=[InputRequired()])
    password = StringField('Password', validators=[InputRequired()])
    reenterpassword = StringField('Re-Password', validators=[InputRequired()])
    phonenumber = StringField('Phone No', validators=[InputRequired()])
    email = EmailField('E-Mail', validators=[InputRequired()])
    submit = SubmitField('Signup')


class ForgotForm(Form):
    username = StringField('Username', validators=[InputRequired()])
    email = EmailField('E-Mail', validators=[InputRequired()])


class ConcertsForm(Form):
    username = StringField('Username', validators=[InputRequired()])
    email = EmailField('E-Mail', validators=[InputRequired()])
    phone = StringField('Phone No', validators=[InputRequired()])
    date = DateField('Date', validators=[InputRequired()])
    time = TimeField('Time', validators=[InputRequired()])
    message = StringField('Message', validators=[InputRequired()])

class FeedbackForm(Form):
    username = StringField('Username', validators=[InputRequired()])
    email = EmailField('E-Mail', validators=[InputRequired()])
    phonenumber = StringField('Phone No', validators=[InputRequired()])
    feedback = StringField('Message', validators=[InputRequired()])