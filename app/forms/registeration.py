from wtforms import Form, PasswordField, StringField, TextAreaField, validators, ValidationError
from wtforms.fields.html5 import EmailField
from ..models import User, app

class RegisterationForm(Form):
    name = StringField('Name', [    
        validators.DataRequired(),
        validators.Length(min=5, max=25)
    ], description='Jone Doe')
    email = EmailField('Email Address', [
        validators.DataRequired(), 
        validators.Email()
    ], description='jone@doe.io')

    def validate_email(self, field):
        user = User.query.filter(User.email == field.data).first()
        if user != None:
            raise ValidationError('Email already registered.')

    username = StringField('Username', [
        validators.DataRequired(),
        validators.Length(min=4, max=10),
        validators.Regexp('(([a-z]+)([^- \[\]A-Z])(([_]+)?)([0-9a-z]?)+)', message='Username may contain lowercase letters, numbers or underscores.Username should begin with lowercase letters.')
    ], description='jone')

    def validate_username(self, field):
        user = User.query.filter(User.username == field.data).first()
        if user or field.data in app.config['PROHIBITED_USERNAMES']:
            raise ValidationError('Username not available.')
    
    phone = StringField('Phone Number', [
        validators.DataRequired(),
        validators.Regexp('^((\+92)|(0092))-{0,1}\d{3}-{0,1}\d{7}$|^\d{11}$|^\d{4}-\d{7}$', message='Invalid phone number has been provided.')
    ], description='+923001234567')

    def validate_phone(self, field):
        user = User.query.filter(User.phone == field.data).first()
        if user and user.username != self.username:
            raise ValidationError('Phone number already registered.')

    address = TextAreaField('Address', [
        validators.DataRequired(),
        validators.Length(min=50, max=1500),
    ], description='Gulberg Park, Lahore')

    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.Length(min=8, max=25),
        validators.equal_to('cpassword', message='Passwords don\'t match.')
    ], description='************')  
    cpassword = PasswordField('Confirm Password', [
        validators.DataRequired(),
        validators.equal_to('password', message='Passwords don\'t match.')
    ], description='************')
