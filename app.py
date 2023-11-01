import os
from flask import Flask, request, make_response,jsonify
from flask_restx import Api, Resource,fields
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager,get_jwt_identity, create_access_token, create_refresh_token
from config import DevConfig
from flask_sqlalchemy import SQLAlchemy
from models import User, Project
from exts import db
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config.from_object(DevConfig)

db.init_app(app)

migrate = Migrate(app, db)
JWTManager(app)

# app.json.compact = False

api = Api(app)

signup_model = api.model(
    "Signup",
    {
        "first_name": fields.String(),
        "last_name": fields.String(),
        "username": fields.String(),
        "email": fields.String(),
        "password": fields.String(),
        "role": fields.String(enum=["admin", "student"]), 
    }
)

login_model = api.model(
    "Login",
    {
        "email": fields.String(),
        "password": fields.String(),
        "role": fields.String(enum=["admin", "student"]), 
    }
)


class Projects(Resource):

    def get(self):
        projects = [project.to_dict() for project in Project.query.all()]

        response_dict = {
            "projects": projects  
        }

        return response_dict, 200

api.add_resource(Projects, '/projects')

# User sign-up area

@api.route("/signUp", methods=["POST"])
class Signup(Resource):
    @api.expect(signup_model)
    def post(self):
        # getting the user's data
        data= request.get_json()
        # checking if the user exists
        email = data.get("email")
        db_user = User.query.filter_by(email=email).first()
        if db_user is not None:
            return make_response(jsonify({"message":f"user with email {email} already exists"}))
        
        new_user = User(
            first_name = data.get("first_name"),
            last_name = data.get("last_name"),
            username = data.get("username"),
            email= data.get("email"),
            password = generate_password_hash(data.get("password"))
        )
        db.session.add(new_user)
        db.session.commit()
        return make_response(jsonify({"message":"user created successfully"}), 201)

# User log-in area
@api.route("/login", methods=["POST"])
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        data = request.get_json()

        email = data.get("email")
        password = data.get("password")

        
        db_user=User.query.filter_by(email=email).first()

        if db_user and  check_password_hash(db_user.password, password):

            access_token=create_access_token(identity=db_user.username, fresh=True)
            refresh_token=create_refresh_token(identity=db_user.username)
            return jsonify(
                     {"access_token":access_token, "refresh_token":refresh_token}
                 )

@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "User": User
    }        
if __name__ == '__main__':
    app.run(port=5555)