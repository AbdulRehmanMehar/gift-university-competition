from .. import app
from ..models import Category
from flask import Blueprint, render_template
from ..utils import Pagination

index = Blueprint('app', __name__)

@app.context_processor
def inject():
    cat = Category.query.all()
    return dict(categories=cat)


@index.route('/')
def home():
    return render_template('index.html')
    

@index.route('/cart')
def cart():
    return render_template('cart.html')


@index.route('/category/<string:slug>', defaults={'page': 1})
@index.route('/category/<string:slug>/<int:page>')
def category(slug, page):
    cat = Category.query.filter(Category.slug == slug).first()
    paginator = Pagination(cat.products, 10, page)
    return render_template('products.html',
                           category=cat,
                           pages=paginator.pages,
                           products=paginator.get_results(),
                           items_per_page=paginator.get_items_per_page(),
                           current_page_number=paginator.get_current_page_number()
                           )


# IMPORT other controllers
from .auth import auth
from .dashboard import dashboard
from .admin import admin


# REGISTER CONTROLLERS
app.register_blueprint(index)
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(dashboard, url_prefix='/dashboard')
