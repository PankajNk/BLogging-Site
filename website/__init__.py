from flask import  Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


db = SQLAlchemy() 
DB_NAME = "databse.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "pankaj" 
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' #baisc done just verfiy doc
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views,url_perfix="/")
    app.register_blueprint(auth,url_perfix="/")

    from .models import User,Post,Comment

    create_database(app)

    #login of flask
    login_manager = LoginManager()
    login_manager.login_view = "auth.login" #this will rediredct to LOGIN page if try to access something inside
    login_manager.init_app(app)


    @login_manager.user_loader #its does is each session will have id and try to get the ID
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists("website/" + DB_NAME):
        db.create_all(app= app)
        print("Database created")