import os
from os import path
from flask import Flask
from script.auth import auth  
from script.books_more import books_more  
from script.database import db 
from script.database import User
from werkzeug.security import generate_password_hash  
#  this is main.py


DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'qwertyuiop'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(books_more, url_prefix='/')

    return app

app = create_app()

def create_database(app):
    if path.exists('shop/instance' + DB_NAME):
        os.remove('shop/instance' + DB_NAME) 

    with app.app_context():
        db.create_all()


        if not User.query.first(): 
            default_user = User(email="user@gmail.com", password=generate_password_hash("password"))
            db.session.add(default_user)
            db.session.commit()

        

if __name__ == '__main__':
    create_database(app)
    app.run(debug=True)


# Shop/
# ├── templates/
# │   ├── login-sign/
# │   │   ├── base.html
# │   │   ├── login.html
# │   │   └── signin.html
# │   ├── home/
# │   │   ├── main.html
# │   │   ├── web.html
# │   │   ├── book_details.html
# │   │   ├── cart.html
# └── script/
# │   └── auth.py
# │   └── database.py
# │   └── books_more.py
# └── main.py