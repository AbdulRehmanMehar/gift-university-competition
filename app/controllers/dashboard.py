import yaml
from ..utils import Cart, Pagination
from ..models import db, User, Order, AddressBook
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
        return render_template('dashboard/orders/viewable.html', crt=yaml.load(res.cart), order=res)
    return redirect(url_for('dashboard.order'))


@dashboard.route('/address-book')
def address_book():
    return render_template('dashboard/addressbook/home.html')


@dashboard.route('/address-book/add', methods=['GET', 'POST'])
def add_address():

    if request.method == 'POST':
        name = request.form.get('name').strip()
        address = request.form.get('address').strip()
        if name and address:
            book = AddressBook(name, address, current_user.id)
            db.session.add(book)
            db.session.commit()
        return redirect(url_for('dashboard.address_book'))

    return render_template('dashboard/addressbook/add.html')


@dashboard.route('/address-book/edit/<int:id>', methods=['GET', 'POST'])
def update_address(id):
    address = AddressBook.query.filter(AddressBook.id == id).first()
    if request.method == 'POST':
        address.name = request.form.get('name').strip()
        address.address = request.form.get('address').strip()
        db.session.commit()
        return redirect(url_for('dashboard.view_address_book'))

    return render_template('dashboard/addressbook/edit.html', address=address)


@dashboard.route('/address-book/delete/<int:id>')
def delete_address(id):
    address = AddressBook.query.filter(AddressBook.id == id).first()
    db.session.delete(address)
    db.session.commit()
    redir = request.args.get('next') or request.referrer or url_for('app.home')
    return redirect(redir)


@dashboard.route('/address-book/view', defaults={'page': 1})
@dashboard.route('/address-book/view/<int:page>')
def view_address_book(page):
    paginator = Pagination(AddressBook, 10, page)
    return render_template('dashboard/addressbook/view.html',
                           pages=paginator.pages,
                           addresses=paginator.get_results(),
                           items_per_page=paginator.get_items_per_page(),
                           current_page_number=paginator.get_current_page_number()
                           )
