import re
from . import app
from ..models import Product
from wtforms import Form, FileField, ValidationError, validators


class PhotoUploadForm(Form):
    photo = FileField('Photo', [
        validators.DataRequired(message='Image is required.')
    ], description='Choose a photo')

    def validate_photo(self, field):
        print(field.data)
        self.ext = field.data.filename.split('.').pop()
        if not self.ext in app.config['UPLOAD_ABLE_IMAGES']:
            raise ValidationError('Invalid file has been selected.')

