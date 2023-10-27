from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from models import db, User, Project, Admins, Class, ProjectMember
from flask_restx import Resource, Api, fields
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import get_jwt_identity, create_access_token, create_refresh_token, JWTManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project-tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app,db)
JWTManager(app)

api = Api(app)

db.init_app(app)
signup_model = api.model(
    "Signup",
    {
        "first_name":fields.String(),
        "last_name":fields.String(),
        "username":fields.String(),
        "email":fields.String(),
        "password":fields.String(),
    }
)

login_model = api.model(
    "Login",
    {
        "email":fields.String(),
        "password":fields.String(),
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
        email = data.get("email"),
        password = data.get("password")

        db_user = User.query.filter_by(email= email).first()
        if db_user and check_password_hash(db_user.password, password):
            access_token = create_access_token(identity= db_user.email, fresh = True)
            refresh_token = create_refresh_token(identity = db_user.email)
            return jsonify(
                {"access_token": access_token, "refresh_token": refresh_token}
                )
        
if __name__ == '__main__':
    app.run(port=5555)