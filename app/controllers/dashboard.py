import yaml
from ..utils import Cart
from ..models import User, Order
from flask_login import current_user
from flask import Blueprint, render_template, redirect, url_for, request, abort, flash, Markup


dashboard = Blueprint('dashboard', __name__)


@dashboard.before_request
def restrict():
    if not current_user.is_authenticated:
        return abort(401)
    if not current_user.verified:
        flash('Please verify your email. '+ Markup('<a class="alert-link" href="'+ url_for('auth.send_token', uname=current_user.username) +'">Resend Verification Token?</a>'), 'info')
    if not current_user.photo:
        flash(Markup('<a href="'+ url_for('auth.upload_photo') +'">Add a photo?</a>') + ' So we can approach you easily.', 'info')


@dashboard.route('/')
def home():
    user = User.query.get(current_user.get_id())     
    return render_template('dashboard/home.html')


@dashboard.route('/cart')
def cart():
    return render_template('dashboard/cart/home.html')


@dashboard.route('/view-cart/<int:id>')
def view_cart(id):
    crt = Cart(None, None, None, int(id))
    res = crt.getCartFromDatabase()
    if res:
        return render_template('dashboard/cart/viewable.html', crt=yaml.load(res.cart), ctitle=res.title, cid=res.id)
    return redirect(url_for('dashboard.cart'))


@dashboard.route('/orders')
def order():
    return render_template('dashboard/orders/home.html')


@dashboard.route('/view-order/<int:id>')
def view_order(id):
    res = Order.query.filter(Order.id == int(id)).first()
    if res:
        return render_template('dashboard/cart/viewable.html', crt=yaml.load(res.cart), status=res.status, cid=res.id, amount=res.amount)
    return redirect(url_for('dashboard.cart'))
