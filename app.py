from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identify
from resources.user import UserRegister
from resources.item import ItemList, Item
# We don't need jsonify with flask restful, flask-restful do it automatic.

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)
app.secret_key = "This is a secret key :o"


@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identify)# This will create a new end point /auth

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, "/items/")
api.add_resource(UserRegister, '/register')

if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(debug=True)
