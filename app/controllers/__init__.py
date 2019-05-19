import os
from .. import app
from ..models import Category, Product
from flask import Blueprint, render_template, send_file, request, session, abort
from ..utils import Pagination

index = Blueprint('app', __name__)


@app.context_processor
def inject():
    cat = Category.query.all()
    # session['cart'] = { }
    cart = session.get('cart') if session.get('cart') else {'len': 0}
    # print(cart)
    return dict(categories=cat, cart=cart)


@index.route('/')
def home():
    return render_template('index.html')


@index.route('/cart')
def cart():
    return render_template('cart.html')


@index.route('/cart-len', methods=['POST'])
def cart_len():
    return str(session['cart']['len']) if session.get('cart') else str(0)


@index.route('/add-to-cart/<string:slug>', methods=['POST'])
def add_to_cart(slug):
    prod = Product.query.filter(Product.slug == slug).first()
    if prod:
        d = {
            'pid': prod.id,
            'title': prod.title,
            'price': prod.price,
            'slug': prod.slug,
            'quantity': int(request.form['quantity'])
        }
        try:
            old = session['cart'][f'p-{prod.id}']
            if old:
                session['cart']['len'] = session['cart']['len'] + d['quantity']
                session['cart'][f'p-{prod.id}']['quantity'] = old['quantity'] + d['quantity']
                session['cart'] = session['cart']
            else:
                session['cart'] = {
                    **session['cart'],
                    f'p-{prod.id}': d,
                    'len': session['cart'].get('len') + d.get('quantity')
                }
        except KeyError:
            length = d.get('quantity')
            try:
                length += session['cart']['len']
                session['cart'] = {
                    **session['cart'],
                    f'p-{prod.id}': d,
                    'len': length
                }
            except KeyError:
                length = d.get('quantity')
                session['cart'] = {
                    f'p-{prod.id}': d,
                    'len': length
                }
           
        return f'{slug}, {request.form["quantity"]} The Product Id'
    return abort(500)


@index.route('/update-cart/<string:slug>', methods=['POST'])
def update_cart(slug):
    qtty = int(request.form['quantity'])
    prod = Product.query.filter(Product.slug == slug).first()
    if prod and session.get('cart'):
        length = session['cart']['len'] - \
            session['cart'][f'p-{prod.id}']['quantity']
        session['cart']['len'] = length + qtty
        session['cart'][f'p-{prod.id}']['quantity'] = qtty
        session['cart'] = session['cart']
        return 'all is well'
    return abort(500)


@index.route('/remove-from-cart/<string:slug>', methods=['POST'])
def remove_cart(slug):
    prod = Product.query.filter(Product.slug == slug).first()
    if prod and session.get('cart'):
        length = session['cart']['len'] - \
            session['cart'][f'p-{prod.id}']['quantity']
        session['cart']['len'] = length
        del session['cart'][f'p-{prod.id}']
        session['cart'] = session['cart']
        return 'all is well'
    return abort(500)


@index.route('/category/<string:slug>', defaults={'page': 1})
@index.route('/category/<string:slug>/<int:page>')
def category(slug, page):
    cat = Category.query.filter(Category.slug == slug).first()
    paginator = Pagination(cat.products, 9, page)
    return render_template('products.html',
                           category=cat,
                           pages=paginator.pages,
                           products=paginator.get_results(),
                           items_per_page=paginator.get_items_per_page(),
                           current_page_number=paginator.get_current_page_number()
                           )


@index.route('/product/<string:slug>')
def product(slug):
    prod = Product.query.filter(Product.slug == slug).first()
    return render_template('product.html', product=prod)


@index.route('/product-image/<string:slug>')
def product_photo(slug):
    prod = Product.query.filter(Product.slug == slug).first()
    file = os.path.join(f'{app.config["UPLOADS_FOLDER"]}/products', prod.photo)
    return send_file(file)


# IMPORT other controllers
from .auth import auth
from .dashboard import dashboard
from .admin import admin


# REGISTER CONTROLLERS
app.register_blueprint(index)
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(dashboard, url_prefix='/dashboard')
