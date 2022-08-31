from flask import Flask, request
from flask_restful import Resource, Api
from security import authenticate, identity
from flask_jwt import JWT, jwt_required

app = Flask(__name__)

api = Api(app)

app.secret_key = 'abhiram'

jwt = JWT(app, authenticate, identity)  # this JWT function is creating a new endpoint called /auth

items = []


# class Student(Resource):
#
#     def get(self, name):
#         return {'name': name}


class Item(Resource):
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {"item": item}, 200 if item is not None else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'MESSAGE': 'An item with name {} already exists'.format(name)}, 400
        item_request = request.get_json()
        item = {
            "name": name,
            "price": item_request['price']
        }
        items.append(item)
        return item, 201


class ItemList(Resource):
    def get(self):
        return {"items": items}


# api.add_resource(Student, '/student/<string:name>')

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=8000, debug=True)
