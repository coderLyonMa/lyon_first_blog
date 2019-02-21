from flask_wtf import FlaskForm
from ..models import Role
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, \
    SelectField
from wtforms.validators import DataRequired, Length, Email, Regexp
from flask_pagedown.fields import PageDownField


class NameForm(FlaskForm):
    name = StringField('Enter your name', validators=[DataRequired()])
    submit = SubmitField('Submit')


class EditProfileForm(FlaskForm):
    name = StringField('Your name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')


class EditProfileAdminForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-aZ-z][A-aZ-z0-9_.]*$', 0,
               'Usernames must only have letters, numbers, dots or '
               'underscores')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role', coerce=int)
    name = StringField('Real Name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in user')


class PostForm(FlaskForm):
    post = PageDownField("What's on your mind?", validators=[DataRequired()])
    submit = SubmitField('Submit')


class EditPostForm(FlaskForm):
    body = PageDownField("Edit your post.", validators=[DataRequired()])
    submit = SubmitField('Submit')