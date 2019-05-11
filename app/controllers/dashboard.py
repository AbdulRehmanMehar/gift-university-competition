from flask import Blueprint, render_template, redirect, url_for, request, abort, flash, Markup
from flask_login import current_user
from ..models import User

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


@dashboard.route('/checkout')
def checkout():
    return 'Welcome to checkout'