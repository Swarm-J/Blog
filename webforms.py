from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, TextAreaField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Email, Length, EqualTo
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditorField
from flask_wtf.file import FileField

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

class NamerForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=50)])
    submit = SubmitField("Submit")

class UserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(max=50)])
    name = StringField("Name", validators=[DataRequired(), Length(max=50)])
    email = EmailField("Email", validators=[DataRequired(), Email(), Length(max=100)])
    about_author = TextAreaField("About Author", validators=[Length(max=500)]) 
    password_hash = PasswordField("Password", validators=[DataRequired(), 
                                EqualTo('password_hash2', message='Passwords Must Match!'), 
                                Length(min=10)])
    password_hash2 = PasswordField("Confirm Password", validators=[DataRequired()])
    profile_pic = FileField("Profile Pic")

    submit = SubmitField("Submit")

class PasswordForm(FlaskForm):
    # email = EmailField("What's Your Email", validators=[DataRequired(), Length(max=50)])
    current_password = PasswordField("Current Password", validators=[DataRequired(), Length(max=50)])

    submit = SubmitField("Submit")

class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = CKEditorField("Content", validators=[DataRequired()])
    slug = StringField("Slug", validators=[DataRequired()])
    
    submit = SubmitField("Submit")


class PasswordForm2(FlaskForm):
    current_password = PasswordField("Current Password", validators=[DataRequired(), Length(max=50)])
    new_password = PasswordField("New Password", validators=[DataRequired(), EqualTo('new_password2', message='Passwords Must Match!'), Length(min=10)])
    new_password2 = PasswordField("Confirm Password", validators=[DataRequired(), Length(min=10)])

    submit = SubmitField("Submit")

class SearchForm(FlaskForm):
    searched = StringField("Searched", validators=[DataRequired()])
    submit = SubmitField("Submit")