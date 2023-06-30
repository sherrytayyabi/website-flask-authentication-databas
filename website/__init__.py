from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():#function setups up a Flask application, so we can configure a secret key and database URI
    app = Flask(__name__) #creates a new Flask application instance 
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs' #creating a secret key 
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' #specifies the URI (Uniform Resource Identifier) for the database that the flask application will use
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/') #integrating the routes and views defined in the blueprint into your application, making them accessible to users when visitng a specified URL prefix
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note
    
    with app.app_context():
        db.create_all() #ensures that the database creation operation occurs within the application context, allowing it to function properly and access the required resources

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader #decorator provided by Flask-Login that registers a user loader function for the login manager
    def load_user(id): #load a user object based on the user ID provided
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')

#create_database function checks the database file to see if it exists, if it does then it creates the necessary tables by calling 'db.create_all(all=app). 