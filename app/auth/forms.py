import re

from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from app.models.user import User


class LoginForm(FlaskForm):
    email = StringField('Email address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')

    def validate_email(self, field):
        field.data = field.data.strip().lower()


class RegistrationForm(FlaskForm):
    email = StringField('Email address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters.'),
    ])
    confirm_password = PasswordField('Confirm password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match.'),
    ])

    def validate_email(self, field):
        email = field.data.strip().lower()
        field.data = email
        if User.query.filter_by(email=email).first():
            raise ValidationError('Email already registered.')

    def validate_password(self, field):
        password = field.data
        count = sum(bool(re.search(p, password)) for p in [
            r'[A-Z]', r'[a-z]', r'[0-9]', r'[^A-Za-z0-9]'
        ])
        if count < 4:
            raise ValidationError(
                'Password must contain all of: uppercase letter, '
                'lowercase letter, digit, and symbol.'
            )


class ForgotPasswordForm(FlaskForm):
    email = StringField('Email address', validators=[DataRequired(), Email()])


class ResetPasswordForm(FlaskForm):
    password = PasswordField('New password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters.'),
    ])
    confirm_password = PasswordField('Confirm new password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match.'),
    ])

    def validate_password(self, field):
        password = field.data
        count = sum(bool(re.search(p, password)) for p in [
            r'[A-Z]', r'[a-z]', r'[0-9]', r'[^A-Za-z0-9]'
        ])
        if count < 4:
            raise ValidationError(
                'Password must contain all of: uppercase letter, '
                'lowercase letter, digit, and symbol.'
            )
