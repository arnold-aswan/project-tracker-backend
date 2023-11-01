from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse, fields, marshal
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, JWTManager
from models import db, Project, User,  project_members, Class
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project-tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# CORS(app, resources={r"/projects/*": {"origins": "http://localhost:5173"}, r"/login": {"origins": "http://localhost:5173"}})
CORS(app, resources={r"/*": {"origins": "*"}})


db.init_app(app)

migrate = Migrate(app, db)
api = Api(app)

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
        # Assuming 'Project' is the SQLAlchemy model for projects
        projects = Project.query.all()
        
        response_dict = [{
            'id': project.id,
            'name': project.name,
            'description': project.description,
            'github_link': project.github_link,
            'user_id': project.user_id,
            'class_id': project.class_id,
            'members': project.memebers,
            'project_type': project.project_type
        } for project in projects]

        return response_dict
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

        response_dict = new_project.to_dict()
        return response_dict,201

class ProjectByIdResource(Resource):
    def delete(self, id):
        project = Project.query.get(id)
        if project:
            db.session.delete(project)
            db.session.commit()
            return {"message": "Project deleted successfully"}, 200
        return {"message": "Project not found"}, 404

class ClassResource(Resource):
    def get(self):
        response_dict = [n.to_dict() for n in Class.query.all()]

        response = make_response(
            jsonify(response_dict),
            200
        )

        return response
    
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