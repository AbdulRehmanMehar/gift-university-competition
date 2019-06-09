from . import db
from datetime import datetime


class Refund(db.Model):
    __tablename__ = 'refunds'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    refund_id = db.Column(db.String, nullable=False)
    order_id = db.Column(db.ForeignKey('order.id'),
                        unique=True, nullable=False)
    order = db.relationship('Order', backref=db.backref('refund', uselist=False))
    placed_on = db.Column(db.DateTime, default=datetime.utcnow)


    def __init__(self, amount, refund_id, order_id):
        self.amount = amount
        self.order_id = order_id
        self.refund_id = refund_id

    def __repr__(self):
        return f'<Refund {self.order.owner}>'