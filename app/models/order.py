from . import db
from datetime import datetime


class Order(db.Model):
    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    cart = db.Column(db.String(5000), nullable=False)
    owner_id = db.Column(db.ForeignKey('users.id'),
                         unique=False, nullable=False)
    owner = db.relationship('User', backref=db.backref('order', uselist=True))
    placed_on = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, status, amount, cart, owner_id):
        self.cart = cart
        self.status = status
        self.amount = amount
        self.owner_id = owner_id

    def __repr__(self):
        return f'{self.owner.name}'
