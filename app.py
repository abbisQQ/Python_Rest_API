from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authendication, identify
from user import UserRegister
from item import ItemList, Item
# We don't need jsonify with flask restful, flask-restful do it automatic.

app = Flask(__name__)
api = Api(app)
app.secret_key = "This is a secret key :o"

jwt = JWT(app, authendication, identify)# This will create a new end point /auth


# This is a resource




api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, "/items/")
api.add_resource(UserRegister, '/register')

if __name__ == "__main__":
    app.run(debug=True)
