from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.widgets import TextArea
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


class WotdForm(FlaskForm):
	wotd = 		StringField('Word of the day', validators=[DataRequired()])
	romaji = 	StringField('Romaji', validators=[DataRequired()])
	defn = 		StringField('Definition', validators=[DataRequired()])
	date = 		StringField('Date', validators=[DataRequired()])
	# Not required, but nice to have
	uid = StringField('UID') # Speficically for Edit Form
	example = 			StringField('Examples or Trivia', widget=TextArea())
    # https://wtforms.readthedocs.io/en/stable/fields.html#wtforms.fields.SelectField
	classification = 	SelectField('Category',
		choices=[
			('None', 'None'),
			('Verb', 'Verb'),
			('Noun', 'Noun'),
			('Adjective', 'Adjective'),
			('Set Phrase', 'Set Phrase')
		])
	submit = SubmitField("Save")