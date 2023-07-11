from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from schemas import ItemSchemas, ItemUpdateSchemas

from db import db
from models import ItemModel


blp = Blueprint("item", __name__, description = "Operations on Items")

@blp.route("/items")
class ItemList(MethodView):

    @blp.response(200, ItemSchemas(many=True))
    def get(self):
        return ItemModel.query.all()
    
    @blp.arguments(ItemSchemas)
    @blp.response(200, ItemSchemas)
    def post(self, item_data):
        item = ItemModel(**item_data)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message = "Error occured while inserting item")

        return item

@blp.route("/items/<int:item_id>")
class ItemID(MethodView):

    @blp.response(200, ItemSchemas)
    def get(self, item_id):
        return ItemModel.query.get_or_404(item_id)

    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item Deleted"}

    @blp.arguments(ItemUpdateSchemas)
    @blp.response(200, ItemSchemas)
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)

        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]

        else:
            item = ItemModel(id=item_id, **item_data)

        db.session.add(item)
        db.session.commit()

        return item