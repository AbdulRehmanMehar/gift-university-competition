from flask import session
from flask_login import current_user
from ..models import db, Product, Cart as CartModel

class Cart:

    def __init__(self, p_slug, quantity, cart_title=None, cart_id=None):
        self.cart_id = cart_id
        self.quantity = quantity
        self.cart_title = cart_title
        self.product = Product.query.filter(Product.slug == p_slug).first()

    def addToCart(self):
        if self.product:
            if session.get('cart'):
                old = session.get('cart').get(f'p-{self.product.id}')
                if old:
                    session['cart']['len'] = session['cart']['len'] + self.quantity
                    session['cart'][f'p-{self.product.id}']['quantity'] = old['quantity'] + self.quantity
                    session['cart'] = session['cart']
                else: 
                    session['cart'] = {
                        **session['cart'],
                        f'p-{self.product.id}': {
                            'pid': self.product.id,
                            'slug': self.product.slug,
                            'title': self.product.title,
                            'price': self.product.price,
                            'quantity': self.quantity,
                        },
                        'len': session['cart']['len'] + self.quantity
                    }
            else:
                session['cart'] = {
                    f'p-{self.product.id}': {
                        'pid': self.product.id,
                        'slug': self.product.slug,
                        'title': self.product.title,
                        'price': self.product.price,
                        'quantity': self.quantity,
                    },
                    'len': self.quantity
                }
            return True
        return False

    def updateTheCart(self):
        if self.product and session.get('cart'):
            length = session['cart']['len'] - \
                session['cart'][f'p-{self.product.id}']['quantity']
            session['cart']['len'] = length + self.quantity
            session['cart'][f'p-{self.product.id}']['quantity'] = self.quantity
            session['cart'] = session['cart']
            return True
        return False

    def removeFromCart(self):
        if self.product and session.get('cart'):
            length = session['cart']['len'] - \
                session['cart'][f'p-{self.product.id}']['quantity']
            session['cart']['len'] = length
            del session['cart'][f'p-{self.product.id}']
            session['cart'] = session['cart']
            return True
        return False

    def deleteTheCart(self):
        session['cart'] = {'len': 0}

    def saveToDatabase(self):
        if current_user.is_authenticated:
            ndbc = CartModel(self.cart_title, f'{session.get("cart")}', current_user.id)
            db.session.add(ndbc)
            db.session.commit()
            self.deleteTheCart()
            return True
        return False

    def getCartFromDatabase(self):
        if self.cart_id:
            dbc = CartModel.query.filter(CartModel.id == self.cart_id).first()
            return dbc
        return {'len': 0}

    def deleteCartFromDatabase(self):
        if self.cart_id:
            dbc = CartModel.query.filter(CartModel.id == self.cart_id).first()
            db.session.delete(dbc)
            db.session.commit()
            return True
        return False