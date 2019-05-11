from wtforms import Form, PasswordField, StringField, TextAreaField, validators, ValidationError
from ..models import User


class EditProfileForm(Form):

    name = StringField('Name', [
        validators.DataRequired(),
        validators.Length(min=5, max=25)
    ])

    email = StringField('Email', render_kw={'disabled': True})

    username = StringField('Username', render_kw={'disabled': True})

    phone = StringField('Phone', [
        validators.DataRequired(),
        validators.Regexp('^((\+92)|(0092))-{0,1}\d{3}-{0,1}\d{7}$|^\d{11}$|^\d{4}-\d{7}$', message='Invalid phone number has been provided.')
    ])

    def validate_phone(self, field):
        user = User.query.filter(User.phone == field.data).first()
        if user:
            raise ValidationError('Phone number already registered.')

    address = TextAreaField('Address', [
        validators.DataRequired(),
        validators.Length(min=50, max=500),
    ])


    password = PasswordField('Password', [
        validators.Optional(),
        validators.Length(min=8, max=25),
        validators.equal_to('cpassword', message='Passwords don\'t match.')
    ], description='************')

    cpassword = PasswordField('Confirm Password', [
        validators.equal_to('password', message='Passwords don\'t match.')
    ], description='************')
