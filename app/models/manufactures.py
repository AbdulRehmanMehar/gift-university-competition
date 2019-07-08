from . import db


class Manufactures(db.Model):
    __tablename__ = 'manufacturers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    slug = db.Column(db.String, nullable=False, unique=True)

    def __init__(self, name):
        self.name = name
        self.slug = self.set_slug(name)

    def set_slug(self, slug):
        return slug.lower().strip().replace(' ', '-')

    def __repr__(self):
        return self.name
