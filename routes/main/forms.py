import pathlib
import re

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from models import User


class RegistrationForm(FlaskForm):
    """ Define the registartion form """
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=12)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        """ Validates that a username is a username """
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'That username is taken. Please choose a different one.')

    def validate_email(self, email):
        """ Validates that an email is an email """
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'That email is taken. Please choose a different one.')

    def validate_password(self, password):
        """ Validates that password is of correct complexity """
        regex = re.compile('[@_!#$%^&*()<>?/\\|}{~:]')
        lower_letter_flag = False
        upper_letter_flag = False
        number_flag = False
        special_char_flag = False
        if bool(re.match('^(?=.*[a-z])', password.data)):
            lower_letter_flag = True
        if bool(re.match('^(?=.*[A-Z])', password.data)):
            upper_letter_flag = True
        if bool(re.match('^(?=.*[0-9])', password.data)):
            number_flag = True
        if regex.search(password.data):
            special_char_flag = True
        if not lower_letter_flag:
            raise ValidationError(
                'Password weak. Password must have atleast 1 lowercase letter.')
        if not upper_letter_flag:
            raise ValidationError(
                'Password weak. Password must have atleast 1 uppercase letter.')
        if not number_flag:
            raise ValidationError(
                'Password weak. Password must have atleast 1 number.')
        if not special_char_flag:
            raise ValidationError('Password weak. Password must have atleast\
                1 special character. Ex: [@_!#$%^&*()<>?/\\|}{~:]')

        with open(str(pathlib.Path(__file__).parent.resolve().parent.resolve().parent.resolve()) +
                  "\\CommonPassword.txt") as myfile:
            if password.data in myfile.read():
                raise ValidationError(
                    'Password weak. The password you have chosen is\
                        commonly used or has been compromised please use another password')


class LoginForm(FlaskForm):
    """ Defines a login form """
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountDetailsForm(FlaskForm):
    """ Defines a user account details form """
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    motto = StringField('Motto', validators=[Length(min=0, max=40)])
    bio = TextAreaField('Bio', validators=[Length(min=0, max=400)])
    picture = FileField('Update Profile Picture', validators=[
                        FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        """ Validates that a username is a username """
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    'That username is taken. Please choose a different one.')


class UpdateAccountSecurityForm(FlaskForm):
    """ Defines a update account security form """
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Update')

    def validate_email(self, email):
        """ Validates that an email is an email """
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    'That email is taken. Please choose a different one.')


class ResetPasswordForm(FlaskForm):
    """ Defines a update password form """
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=12)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

    def validate_password(self, password):
        """ Validates that password is of correct complexity """
        regex = re.compile('[@_!#$%^&*()<>?/\\|}{~:]')
        lower_letter_flag = False
        upper_letter_flag = False
        number_flag = False
        special_char_flag = False
        if bool(re.match('^(?=.*[a-z])', password.data)):
            lower_letter_flag = True
        if bool(re.match('^(?=.*[A-Z])', password.data)):
            upper_letter_flag = True
        if bool(re.match('^(?=.*[0-9])', password.data)):
            number_flag = True
        if regex.search(password.data):
            special_char_flag = True
        if not lower_letter_flag:
            raise ValidationError(
                'Password weak. Password must have atleast 1 lowercase letter.')
        if not upper_letter_flag:
            raise ValidationError(
                'Password weak. Password must have atleast 1 uppercase letter.')
        if not number_flag:
            raise ValidationError(
                'Password weak. Password must have atleast 1 number.')
        if not special_char_flag:
            raise ValidationError('Password weak. Password must have atleast\
               1 special character. Ex: [@_!#$%^&*()<>?/\\|}{~:]')

        with open(str(pathlib.Path(__file__).parent.resolve().parent.resolve().parent.resolve()) +
                  "\\CommonPassword.txt") as myfile:
            if password.data in myfile.read():
                raise ValidationError(
                    'Password weak. The password you have chosen is\
                        commonly used or has been compromised please use another password')
