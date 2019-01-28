from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField("Log in")

class UserForm(FlaskForm):
	currentpwd = PasswordField('Current Password', validators=[DataRequired()])
	password = PasswordField('New Password', 
		validators=[DataRequired(), Length(min=10, max=100)])
	confirm_password = PasswordField('Confirm New Password', 
		validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField("Change Password")



class AddForm(FlaskForm):
	pass

class EditForm(FlaskForm):
	pass