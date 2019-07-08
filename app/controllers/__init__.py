import os, stripe, yaml
from .. import app
from ..utils import Pagination, Cart
from flask_login import login_required, current_user
from ..models import db, Category, Product, Order, Refund, User, Review
from flask import Blueprint, render_template, send_file, request, session, abort, flash, redirect, url_for

index = Blueprint('app', __name__)
stripe.api_key = app.config['STRIPE_SECRET_KEY']


@app.context_processor
def inject():
    cat = Category.query.all()
    cart = session.get('cart') if session.get('cart') else {'len': 0}
    return dict(categories=cat, cart=cart)


@index.route('/')
def home():
    featured = Product.query.filter(Product.featured == True).all()
    return render_template('index.html', featured=featured)


@index.route('/cart')
def cart():
    return render_template('cart.html')


@index.route('/checkout', defaults={'cid': None})
@index.route('/checkout/<int:cid>')
@login_required
def checkout(cid):
    if cid:
        crt = Cart(None, None, None, int(cid))
        res = crt.getCartFromDatabase()
        if res:
            amount = 0
            for key, product in yaml.load(res.cart).items():
                if key != 'len':
                    amount += product.get('price') * product.get('quantity')
            return render_template('checkout.html', stripe_pk=app.config['STRIPE_PUBLISHABLE_KEY'], amount=amount, cid=cid)
    else:
        if session.get('cart').get('len') > 0:
            amount = 0
            for key, product in session.get('cart').items():
                if key != 'len':
                    amount += product.get('price') * product.get('quantity')
            return render_template('checkout.html', stripe_pk=app.config['STRIPE_PUBLISHABLE_KEY'], amount=amount, cid=cid)
    flash('It seems that you\'re cart is empty.', 'danger')
    return redirect(url_for('app.cart'))


@index.route('/charge', methods=['POST'], defaults={'cid': None})
@index.route('/charge/<int:cid>', methods=['POST'])
@login_required
def charge(cid):
    try:
        amount = 0
        crt = Cart(None, None, None, int(cid) if cid else None)
        res = crt.getCartFromDatabase()
        if res:
            for key, product in yaml.load(res.cart).items():
                if key != 'len':
                    amount += product.get('price') * product.get('quantity')
        else:
            for key, product in session.get('cart').items():
                if key != 'len':
                    amount += product.get('price') * product.get('quantity')
        customer = stripe.Customer.create(
            email = current_user.email,
            source = request.form['stripeToken']
        )

        charge = stripe.Charge.create(
            customer = customer.id,
            amount = amount * 100, # in cents
            currency = 'usd',
            description = 'ordered'
        )
        ordr = Order('Placed', amount, res.cart if res else f'{session.get("cart")}', current_user.id, charge.id, customer.id)
        db.session.add(ordr)
        db.session.commit()
        if res:
            for key, product in yaml.load(res.cart).items():
                if key != 'len':
                    prod = Product.query.filter(Product.id == int(product.get('pid'))).first()
                    prod.quantity -= int(product.get('quantity'))
                    db.session.commit()
            crt.deleteCartFromDatabase() 
        else: 
            for key, product in session.get('cart').items():
                if key != 'len':
                    prod = Product.query.filter(Product.id == int(product.get('pid'))).first()
                    prod.quantity -= int(product.get('quantity'))
                    db.session.commit()
            crt.deleteTheCart()
        return redirect(url_for('dashboard.order'))
    except:
        flash('Something went seriously wrong.', 'danger')
        return redirect(url_for('app.cart'))


@index.route('/refund/<int:id>', defaults={'fee': 1})
@index.route('/refund/<int:id>/<int:fee>')
@login_required
def refund(id, fee):
    ordr = Order.query.filter(Order.id == id).first()
    try:
        if ordr:
            # Refunds will be 75% of the amount, 25% will be fee
            amount = int(ordr.amount * 75 / 100) if fee == 1 else ordr.amount
            ref = stripe.Refund.create(
                charge=ordr.charge_id,
                amount=amount * 100 # in cents..
            )
            
            refund = Refund(amount, ref.id, ordr.id)
            db.session.add(refund)
            db.session.commit()

            for key, product in yaml.load(ordr.cart).items():
                if key != 'len':
                    prod = Product.query.filter(
                        Product.id == int(product.get('pid'))).first()
                    prod.quantity += int(product.get('quantity'))
                    db.session.commit()
            flash(f'{amount} was refunded to you!', 'success')
            return redirect(url_for('dashboard.view_order', id=id))
        else:
            flash('Something went seriously wrong.', 'danger')
            return redirect(url_for('dashboard.order'))
    except:
        flash('Something went seriously wrong.', 'danger')
        return redirect(url_for('dashboard.order'))


@index.route('/cart-len', methods=['POST'])
def cart_len():
    return str(session['cart']['len']) if session.get('cart') else str(0)


@index.route('/add-to-cart/<string:slug>', methods=['POST'])
def add_to_cart(slug):
    crt = Cart(slug, int(request.form['quantity']))
    if crt.addToCart():
        return 'Good'
    return abort(500, {'message': 'It seems that something went wrong.'})

@index.route('/update-cart/<string:slug>', methods=['POST'])
def update_cart(slug):
    crt = Cart(slug, int(request.form['quantity']))
    if crt.updateTheCart():
        return 'Good'
    return abort(500, {'message': 'It seems that something went wrong.'})


@index.route('/remove-from-cart/<string:slug>', methods=['POST'])
def remove_cart(slug):
    crt = Cart(slug, None)
    if crt.removeFromCart():
        return 'good'
    return abort(500, {'message': 'It seems that something went wrong.'})


@index.route('/save-cart', methods=['POST'])
@login_required
def save_cart():
    title = request.form['title']
    crt = Cart(None, None, title)
    if crt.saveToDatabase():
        flash('Cart was saved to database successfully.', 'success')
        return 'Very Good'
    return abort(500, {'message': 'It seems that something went wrong.'})



@index.route('/delete-db-cart', methods=['POST'])
@login_required
def delete_db_cart():
    id = int(request.form['id'])
    crt = Cart(None, None, None, id)
    if crt.deleteCartFromDatabase():
        flash('Cart was removed from database successfully.', 'info')
        return 'Done'
    return abort(500)


@index.route('/cancel-order', methods=['POST'])
@login_required
def cancel_order():
    id = int(request.form['id'])
    ordr = Order.query.filter(Order.id == id).first()
    if ordr and ordr.status != 'Canceled' and ordr.status != 'Completed' and (current_user.admin or current_user.id == ordr.owner.id):
        ordr.status = 'Canceled'
        db.session.commit()
        if current_user.id == ordr.owner.id:
            return redirect(url_for('app.refund', id=id))
        else:
            return redirect(url_for('app.refund', id=id, fee=0))
    return redirect(url_for('dashboard.order')) 


@index.route('/user-profile/<string:uname>')
def user_profile(uname):
    user = User.query.filter(User.username == uname).first()
    return render_template('user.html', user=user)


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


@index.route('/leave-review', methods=['POST'])
@login_required
def leave_review():
    pid = request.form.get('product_id')
    rating = request.form.get('rating')
    if pid != None and rating > 0 and rating <= 5:
        review = Review(rating, pid, current_user.id)
        db.session.add(review)
        db.session.commit()
    redir = request.args.get('next') or request.referrer or url_for('app.home')
    return redirect(redir)


@index.route('/update-review', methods=['POST'])
@login_required
def update_review():
    rating = request.form.get('rating')
    review_id = request.form.get('review_id')
    review = Review.query.filter(Review.id == review_id).first()
    if review and rating > 0 and rating <= 5:
        review.rating = rating
        db.session.commit()
    redir = request.args.get('next') or request.referrer or url_for('app.home')
    return redirect(redir)


@index.route('/delete-review', methods=['POST'])
@login_required
def delete_review():
    review = Review.query.filter(Review.id == request.form.get('review_id')).first()
    db.session.delete(review)
    db.session.commit()
    redir = request.args.get('next') or request.referrer or url_for('app.home')
    return redirect(redir)







# IMPORT other controllers
from .auth import auth
from .dashboard import dashboard
from .admin import admin


# REGISTER CONTROLLERS
app.register_blueprint(index)
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(dashboard, url_prefix='/dashboard')
