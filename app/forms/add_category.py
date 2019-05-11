from wtforms import Form, SelectField, StringField, validators
from ..models import Category
from wtforms.ext.sqlalchemy.fields import QuerySelectField


def get_cats():
    return Category.query


class AddCategoryForm(Form):

    name = StringField('Name', [
        validators.DataRequired(),
        validators.length(min=5, max=20)
    ], description='Twizzers')

    parent = QuerySelectField('Parent', query_factory=get_cats, get_pk=lambda a: a.id, get_label=lambda a: a.name, allow_blank=True)

