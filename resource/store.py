import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import StoreSchemas

from db import stores

blp = Blueprint("store", __name__, description = "Operations on Stores")

@blp.route("/stores")
class StoreList(MethodView):

    @blp.response(200, StoreSchemas)
    def get(self):
        stores.values()
    
    @blp.arguments(StoreSchemas)
    @blp.response(200, StoreSchemas)
    def post(self, store_data, store_id):
    
        for store in stores.values():
            if store_data["name"] == stores["name"]:
                #Check if the name of the store already exist in the database
                abort(400, message = "Bad Request. Store already exist")

        store_id = uuid.uuid4().hex
        store = {**store_data, "id": store_id}
        stores[store_id] = store
        
        return store, 201
    


@blp.route("/stores/<string:store_id>")
class StoreID(MethodView):

    @blp.response(200, StoreSchemas)
    def get(self, store_id):
        try: 
            return stores[store_id]
        except KeyError: 
            abort(404, message = "Store not found")

    def delete(self, store_id):
        try:
            del stores[store_id]
            return stores
        except:
            abort(404, message = "Store not found")

