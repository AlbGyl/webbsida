from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from BRF.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Användarnamn', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Epost', validators=[DataRequired(), Email()])
    password = PasswordField('Lösenord', validators=[DataRequired()])
    confirm_password = PasswordField('Bekräfta lösenord', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Anmäl mig')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Det användarnamnet är taget. Välj ett annat.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Den e-postadressen är redan taget. Välj ett annat.')


class LoginForm(FlaskForm):
    email = StringField('Epost',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Lösenord', validators=[DataRequired()])
    remember = BooleanField('Kom ihåg mig')
    submit = SubmitField('Logga in')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')
