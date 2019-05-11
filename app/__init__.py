import os
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_sendgrid import SendGrid

# INITIALIZE APPLICATION

app = Flask(__name__)

app.template_folder = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'views')

app.static_folder = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'public')

app.config['UPLOADS_FOLDER'] = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'uploads')

config_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'app.config')

with open(config_path) as data_file:
    config = data_file.readlines()
config = [x.strip() for x in config]

for x in config:
    if x != '':
        arr = x.split('=')
        app.config[arr[0]] = arr[1]

db = SQLAlchemy(app)
mail = SendGrid(app)

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check = 0, pre-check = 0, max-age = 0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

# IMPORT SUB MODULES
from .models import *
from .controllers import *
