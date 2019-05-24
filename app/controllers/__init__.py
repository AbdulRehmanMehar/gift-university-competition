import os
from .. import app
from ..models import Category, Product
from flask import Blueprint, render_template, send_file, request, session, abort, flash
from ..utils import Pagination, Cart

index = Blueprint('app', __name__)


@app.context_processor
def inject():
    cat = Category.query.all()
    cart = session.get('cart') if session.get('cart') else {'len': 0}
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
    crt = Cart(slug, int(request.form['quantity']))
    if crt.addToCart():
        return 'Good'
    return abort(500)

@index.route('/update-cart/<string:slug>', methods=['POST'])
def update_cart(slug):
    crt = Cart(slug, int(request.form['quantity']))
    if crt.updateTheCart():
        return 'Good'
    return abort(500)


@index.route('/remove-from-cart/<string:slug>', methods=['POST'])
def remove_cart(slug):
    crt = Cart(slug, None)
    if crt.removeFromCart():
        return 'good'
    return abort(500)


@index.route('/save-cart', methods=['POST'])
def save_cart():
    title = request.form['title']
    crt = Cart(None, None, title)
    if crt.saveToDatabase():
        flash('Cart was saved to database successfully.', 'success')
        return 'Very Good'
    return abort(500)



@index.route('/delete-db-cart', methods=['POST'])
def delete_db_cart():
    id = int(request.form['id'])
    crt = Cart(None, None, None, id)
    if crt.deleteCartFromDatabase():
        flash('Cart was removed from database successfully.', 'info')
        return 'Done'
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
