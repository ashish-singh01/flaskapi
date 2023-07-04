import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import ItemSchemas, ItemUpdateSchemas
from db import items


blp = Blueprint("item", __name__, description = "Operations on Items")

@blp.route("/items")
class ItemList(MethodView):

    @blp.response(200, ItemSchemas)
    def get(self):
        return items.values()
    
    @blp.arguments(ItemSchemas)
    @blp.response(200, ItemSchemas)
    def post(self, item_data, item_id):
        for item in items.values():
            if item_data["name"] == item["name"]:
                #Check if the name of item already exist in the database
                abort(400, message = "Bad Requet. Item already exist")

        # if item_data["store_id"] not in items: 
        #     return {"message": "Item not found"}, 404
        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id}
        items[item_id] = item
        
        return item, 201
    

@blp.route("/items/<string:item_id>")
class ItemID(MethodView):

    @blp.response(200, ItemSchemas)
    def get(self, item_id):
        try: 
            return items[item_id]
        except KeyError: 
            abort(404, message = "Item not found")

    def delete(self, item_id):
        try:
            del items[item_id]
            return items
        except KeyError:
            abort(404, message = "Item not found")

    @blp.arguments(ItemUpdateSchemas)
    @blp.response(200, ItemSchemas)
    def put(self, item_data, item_id):
        
        try:
            item = items[item_id]
            item |= item_data
            return (item)
        except KeyError:
            abort(404, message = "Item not found")
