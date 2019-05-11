from . import db


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    slug = db.Column(db.String, nullable=False, unique=True)
    parent_id = db.Column(db.ForeignKey('categories.id'), nullable=True)
    parent = db.relationship(lambda: Category, remote_side=id, backref='child', passive_deletes=True)

    def __init__(self, name, parent_id=None):
        self.name = name
        self.parent_id = parent_id
        self.slug = self.set_slug(name)
    def set_slug(self, slug):
        return slug.lower().strip().replace(' ', '-')

    def __repr__(self):
        return self.name
