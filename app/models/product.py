from . import db
from datetime import datetime


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    slug = db.Column(db.String, nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    featured = db.Column(db.Boolean, default=False)
    description = db.Column(db.String(1500), nullable=False)
    photo = db.Column(db.String, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    manufacturer_id = db.Column(db.Integer, db.ForeignKey('manufacturers.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    owner = db.relationship(
        'User', backref=db.backref('products', uselist=True))
    category = db.relationship(
        'Category', backref=db.backref('products', uselist=True))
    manufacturer = db.relationship(
        'Manufactures', backref=db.backref('products', uselist=True))

    def __init__(self, title, price, quantity, featured, description, photo, owner, category, manufactures):
        self.title = title
        self.price = price
        self.photo = photo
        self.owner_id = owner
        self.quantity = quantity
        self.featured = featured
        self.category_id = category
        self.manufactures_id = manufactures
        self.description = description
        self.slug = self.set_slug(title)

    def set_slug(self, slug):
        return slug.lower().strip().replace(' ', '-')
    
    def __repr__(self):
        return self.title
