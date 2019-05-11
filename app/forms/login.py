from wtforms import Form, StringField, PasswordField, validators, ValidationError
from flask import Markup, url_for
from ..models import User

class LoginForm(Form):
    username = StringField('Username or Email', [
        validators.DataRequired()
    ], description='jone')
    
    def validate_username(self, field):
        self.user = User.query.filter((User.email == field.data) | (User.username == field.data)).first()
        if not self.user:
            raise ValidationError('Username or Email was not found in record.' + Markup('<a href='+ url_for('auth.register') +' style="float: right">Register?</a>'))
    
    password = PasswordField('Password', [
        validators.DataRequired()
    ], description='**********')

    def validate_password(self, field):
        if (not self.user or not self.user.compare(field.data)) and not len(self.username.errors) > 0:
            raise ValidationError('Incorrect Credentials were provided. ' + Markup('<a href='+ url_for('auth.send_token', uname=self.username.data) +' style="float: right">Reset Password?</a>'))

    def get_user(self):
        return self.user
