from . import db


class Cart(db.Model):
    __tablename__ = 'cart'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    cart = db.Column(db.String(5000), nullable=False)
    owner_id = db.Column(db.ForeignKey('users.id'), unique=False, nullable=False)
    owner = db.relationship('User', backref=db.backref('cart', uselist=True))

    def __init__(self, title, cart, owner_id):
        self.cart = cart
        self.title = title
        self.owner_id = owner_id

    def __repr__(self):
        return f'{self.owner.name}'
