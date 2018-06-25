from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authendication, identify

# We don't need jsonify with flask restful, flask-restful do it automatic.

app = Flask(__name__)
api = Api(app)
app.secret_key = "This is a secret key :o"
items = []

jwt = JWT(app, authendication, identify) # This will create a new end point /auth


# This is a resource

class Item(Resource):
    # parsing the request using reqparser
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float,
                        required=True,
                        help='This field cannot be blank')

    # @app.route('student/<string:name>') We can do it that way or user our api and add resources to it
    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x["name"] == name, items), None)

        return {"item": item}, 200 if item else 404

    @jwt_required()
    def post(self, name):

        if next(filter(lambda x: x["name"] == name, items), None) is not None:
            return {"message": "An item with name {} already exists".format(name)}, 400 # 400 bad request

        data = Item.parser.parse_args()
        item = {
            "name": name,
            "price": data["price"]
        }

        items.append(item)
        return item, 201

    @jwt_required()
    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))

    @jwt_required()
    def put(self, name):

        data = Item.parser.parse_args()

        item = next(filter(lambda x: x['name'] != name, items), None)
        if item is None:
            item = {"name": name, "price": data['price']}
            items.append(item)
        else:
            item.update(data)
        return item


class ItemList(Resource):
    def get(self):
        return {"Item List": items}, 200


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, "/item/")
app.run(debug=True)
