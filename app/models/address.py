from . import db


class AddressBook(db.Model):
    __tablename__ = 'addressbook'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    owner = db.relationship(
        'User', backref=db.backref('addresses', uselist=True))

    def __init__(self, name, address, owner_id):
        self.name = name
        self.address = address
        self.owner_id = owner_id

    def __repr__(self):
        return self.owner.name
