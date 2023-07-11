from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt


from db import db
from models import UserModel
from schemas import UserSchemas
from blocklist import BLOCKLIST

blp = Blueprint("Users", "users", description="Operations on Users")


@blp.route("/register")
class UserRegister(MethodView):

    @blp.arguments(UserSchemas)
    def post(self, userdata):
        if UserModel.query.filter(UserModel.username == userdata["username"]).first():
            abort(409, message = "User Already exits")

        user = UserModel(username=userdata["username"], 
                         password = pbkdf2_sha256.hash(userdata["password"]))
        db.session.add(user)
        db.session.commit()

        return {"message": "User Registered Successfully"}, 201
    

@blp.route("/login")
class UserLogin(MethodView):

    @blp.arguments(UserSchemas)
    def post(self, userdata):
        user = UserModel.query.filter(UserModel.username == userdata["username"]).first()

        if user and pbkdf2_sha256.verify(userdata["password"], user.password):
            access_token = create_access_token(identity=user.id)
            
            return {"access_token": access_token}
        abort(404, message = "User Not Found")


@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200


@blp.route("/users/<int:user_id>")
class User(MethodView):

    @blp.response(200, UserSchemas)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user
    @jwt_required()
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()

        return {"message": "User Deleted Successfully"}, 201