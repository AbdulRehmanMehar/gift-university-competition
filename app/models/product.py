from . import db


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    slug = db.Column(db.String, nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(1500), nullable=False)
    photo = db.Column(db.String, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship('Category', backref=db.backref('products', uselist=True))

    def __init__(self, title, price, description, photo, category):
        self.title = title
        self.price = price
        self.photo = photo
        self.category_id = category
        self.description = description
        self.slug = self.set_slug(title)

    def set_slug(self, slug):
        return slug.lower().strip().replace(' ', '-')
    
    def __repr__(self):
        return self.title
