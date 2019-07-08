from . import db


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    product_id = db.Column(
        db.Integer, db.ForeignKey('products.id'))
    reviewer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    product = db.relationship(
        'Product', backref=db.backref('reviews', uselist=True))
    reviewer = db.relationship(
        'User', backref=db.backref('reviews', uselist=True))

    def __init__(self, rating, product_id, reviewer_id):
        self.rating = rating
        self.product_id = product_id
        self.reviewer_id = reviewer_id

    def __repr__(self):
        return f'{self.rating}'
