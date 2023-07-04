import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import StoreSchemas
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from db import db 
from models import StoreModel

blp = Blueprint("store", __name__, description = "Operations on Stores")

@blp.route("/stores")
class StoreList(MethodView):

    @blp.response(200, StoreSchemas(many=True))
    def get(self):
        return StoreModel.query.all()
    
    @blp.arguments(StoreSchemas)
    @blp.response(200, StoreSchemas)
    def post(self, store_data):
    
        store = StoreModel(**store_data)

        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message = "Store already exists")
        except SQLAlchemyError:
            abort(500, message = "An error occured while inserting store")

        return store


    


@blp.route("/stores/<string:store_id>")
class StoreID(MethodView):

    @blp.response(200, StoreSchemas)
    def get(self, store_id):
        return StoreModel.query.get_or_404(store_id)
    
    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store Deleted"}
