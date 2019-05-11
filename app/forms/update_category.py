from wtforms import Form, SelectField, StringField, validators
from ..models import Category
from wtforms.ext.sqlalchemy.fields import QuerySelectField


def get_cats():
    return Category.query


class UpdateCategoryForm(Form):

    name = StringField('Name', [
        validators.DataRequired(),
        validators.length(min=5, max=20)
    ], description='Twizzers')

    parent = QuerySelectField('Parent', query_factory=get_cats, get_pk=lambda a: a.id, get_label=lambda a: a.name, allow_blank=True)

    def __init__(self, category, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category = category

    def set_defaults(self):
        self.name.data = self.category.name
        self.parent.data = self.category.parent
