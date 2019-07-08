import os, binascii
from datetime import datetime
from flask_login import UserMixin
from passlib.hash import sha256_crypt
from . import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(200), nullable=False)
    email = db.Column('email', db.String(120), unique=True, nullable=False)
    username = db.Column('username', db.String(80), unique=True, nullable=False)
    phone = db.Column('phone', db.String(15), unique=True, nullable=False)
    address = db.Column('address', db.String(1500), nullable=False)
    password = db.Column('password', db.String(200), nullable=False)
    photo = db.Column('photo', db.String(200), unique=True, nullable=True)
    admin = db.Column('admin', db.Boolean, nullable=False, default=False)
    business = db.Column('business', db.Boolean, nullable=False, default=False)
    verified = db.Column('verified', db.Boolean, nullable=False, default=False)
    verificationToken = db.Column('verificationToken', db.String(300), nullable=True)
    created_on = db.Column('created_on', db.DateTime, default=datetime.utcnow)
    modified_on = db.Column('modified_on', db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, name, email, username, phone, address, password, admin=False, verified=False, business=False):
        self.name = name
        self.email = email
        self.username = username
        self.phone = phone
        self.address = address
        self.password = self.hash(password)
        self.admin = admin
        self.verified = verified
        self.business = business
        user = User.query.order_by(User.id.desc()).first()
        if not user:
            self.id = 1
        else:
            self.id = user.id + 1
        if not verified:
            self.verificationToken = self.set_token()
        else:
            self.verificationToken = None

    def hash(self, password):
        return sha256_crypt.encrypt(password)

    def compare(self, pwd):
        return sha256_crypt.verify(pwd, self.password)

    def set_token(self):
        return str(binascii.b2a_hex(os.urandom(15)))

    def __repr__(self):
        return self.username
