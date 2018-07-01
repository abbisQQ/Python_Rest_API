from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    # parsing the request using reqparser
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float,
                        required=True,
                        help='This field cannot be blank')

    # @app.route('student/<string:name>') We can do it that way or user our api and add resources to it
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "Item not found"}

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": "An item with name {} already exists".format(name)}, 400  # 400 bad request

        data = Item.parser.parse_args()
        item = ItemModel( name, data["price"])

        try:
            ItemModel.save_to_db(item)
        except:
            return {'message': "An error occurred inserting a new item"}, 500
        return item.json(), 201



    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return  {'message': 'item deleted'}

    @jwt_required()
    def put(self, name):

        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)


        if item is None:
           item = ItemModel(name, data['price'])
        else:
           item.price = data['price']

        item.save_to_db()
        return item.json()




class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}