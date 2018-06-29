from flask_restful import Resource, reqparse
import sqlite3
from flask_jwt import jwt_required


class Item(Resource):
    # parsing the request using reqparser
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float,
                        required=True,
                        help='This field cannot be blank')

    # @app.route('student/<string:name>') We can do it that way or user our api and add resources to it
    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item
        return {"message": "Item not found"}

    def post(self, name):
        if self.find_by_name(name):
            return {"message": "An item with name {} already exists".format(name)}, 400  # 400 bad request

        data = Item.parser.parse_args()
        item = {
            "name": name,
            "price": data["price"]
        }
        try:
            self.insert(item)
        except:
            return {'message': "An error occurred inserting a new item"}, 500
        return item, 201

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        results = cursor.execute(query, (name,))
        row = results.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[0], "price": row[1]}}

    @jwt_required()
    def delete(self, name):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {'message': 'Item deleted'}

    @jwt_required()
    def put(self, name):

        data = Item.parser.parse_args()

        item = self.find_by_name(name)
        updated_item = {'name': name, 'price': data['price']}

        if item is None:
            try:
                self.insert(updated_item)
            except:
                return {'message': "An error occurred inserting a new item"}, 500
        else:
            try:
                self.update(updated_item)
            except:
                return {'message': "An error occurred updating an item"}, 500
        return item

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['price'], item['name']))

        connection.commit()
        connection.close()


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        results = cursor.execute(query)
        items = []
        for row in results:
            items.append({'item': row[0], 'price': row[1]})

        connection.close()
        return {'items': items}