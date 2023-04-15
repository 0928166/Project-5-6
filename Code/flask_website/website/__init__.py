from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from os.path import dirname, abspath
from flask_login import LoginManager
from werkzeug.security import generate_password_hash

# assign SQLAlchemy functionallity to db
db = SQLAlchemy()
# creates the app that will run the website
def create_app():
    # assigns and configures the Flask object. Also attaches the database to this object
    app = Flask(__name__)
    app.config.from_pyfile(path.join('config', 'app.conf'))
    db.init_app(app)

    # import all the routes that the webpages use
    from .views import views
    from .auth import auth
    from .camera import camera
    from .admin import admin
    # registers all the blueprints to the urls
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(camera, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/')
    # import database models and creates the database, if it doesn't exist already
    from .models import User, IpCamera
    create_database(app)
    # creates the loginmanager, this will handle the login system
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # this allows the login manager to get the id of users
    @login_manager.user_loader
    def load_user(id):
        return db.session.query(User).get(int(id))
    return app
# creates a database if one doesn't exist yet. It will also create an admin account
def create_database(app):
    # check if the database already exists
    if not path.exists(path.join(dirname(dirname(abspath(__file__))),'instance', app.config.get("DB_NAME"))):
        # within context of this app, create database and make admin user with adminadmin as password, please change this after the first login
        with app.app_context():
            # import models that will be used in the database
            from .models import User
            db.create_all()
            admin = User(username="admin",first_name="admin", password=generate_password_hash("adminadmin", method='sha256'), is_admin=True)
            db.session.add(admin)
            db.session.commit()
        print('Created Database!')