from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-aZ-z][A-aZ-z0-9_.]*$', 0,
               'Usernames must only have letters, numbers, dots or '
               'underscores')])
    password = PasswordField('Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm password')
    submit = SubmitField('Sign up')


    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')


    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log in')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    password = PasswordField('New Password', validators=[
        DataRequired(), EqualTo('password2', message='passwords must match')])
    password2 = PasswordField('Confirm New Password', validators=[DataRequired()])
    submit = SubmitField('Update password')


class PasswordResetRequestForm(FlaskForm):
    email = StringField('Enter your email address', validators=[DataRequired(),
                        Length(1, 64), Email()])
    Submit = SubmitField('Send Confirmation Email')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[
        DataRequired(), EqualTo('password2', message='passwords must match')])
    password2 = PasswordField('Confirm New Password', validators=[DataRequired()])
    submit = SubmitField('Update password')


class EmailChangeForm(FlaskForm):
    password = PasswordField('Your password', validators=[DataRequired()])
    new_email = StringField('Enter your new email address', validators=[DataRequired(),
                            Length(1, 64), Email()])
    submit = SubmitField('Update Email')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email address already registered.')