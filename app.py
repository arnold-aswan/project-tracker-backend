from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse, fields, marshal
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, JWTManager
from models import db, Project, User,  ProjectMember, Class
from flask_cors import CORS
import logging

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project-tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# CORS(app, resources={r"/projects/*": {"origins": "http://localhost:5173"}, r"/login": {"origins": "http://localhost:5173"}})
CORS(app, resources={r"/*": {"origins": "*"}})


db.init_app(app)

migrate = Migrate(app, db)
api = Api(app)
jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = 'your_secret_key_here'

# Define API models using reqparse and fields
signup_parser = reqparse.RequestParser()
signup_parser.add_argument('first_name', type=str, required=True)
signup_parser.add_argument('last_name', type=str, required=True)
signup_parser.add_argument('username', type=str, required=True)
signup_parser.add_argument('email', type=str, required=True)
signup_parser.add_argument('password', type=str, required=True)
signup_parser.add_argument('role', type=str, default='Student') 

login_parser = reqparse.RequestParser()
login_parser.add_argument('email', type=str, required=True)
login_parser.add_argument('password', type=str, required=True)
login_parser.add_argument('role', type=str, required=True)

project_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'github_link': fields.String,
    'user_id': fields.Integer,
    'class_id': fields.Integer,
    'members': fields.String,
    'project_type': fields.String
}

class Projects(Resource):
    def get(self):
        projects = Project.query.all()
        project_list = [marshal(project, project_fields) for project in projects]

        response_dict = {
            "projects": project_list
        }

        return response_dict, 200

class Signup(Resource):
    def post(self):
        data = signup_parser.parse_args()
        email = data['email']
        db_user = User.query.filter_by(email=email).first()

        if db_user is not None:
            return make_response(jsonify({"message": f"user with email {email} already exists"}))

        new_user = User(
            first_name=data['first_name'],
            last_name=data['last_name'],
            username=data['username'],
            email=data['email'],
            password=generate_password_hash(data['password']),
            role=data['role']

        )
        db.session.add(new_user)
        db.session.commit()

        return make_response(jsonify({"message": "user created successfully"}), 201)

class Login(Resource):
    def post(self):
        data = login_parser.parse_args()
        email = data['email']
        password = data['password']
        role = data['role']

        db_user = User.query.filter_by(email=email).first()
        if db_user and check_password_hash(db_user.password, password):
            access_token = create_access_token(identity=db_user.email, fresh=True)
            refresh_token = create_refresh_token(identity=db_user.email)

            return jsonify({"access_token": access_token, "refresh_token": refresh_token})

# api.add_resource(Projects, '/projects')
class ProjectsResource(Resource):
    def get(self):
        projects = Project.query.all()
        response_dict = []

        for project in projects:
            user = User.query.get(project.user_id)

            project_info = project.to_dict()
            user_info = user.to_dict()
            project_info['user'] = user_info

            # Fetch project members for the current project
            project_members = ProjectMember.query.filter_by(project_id=project.id).all()
            members_data = []

            for member in project_members:
                if member.user:
                    members_data.append(member.user.to_dict())

            project_info['project_members'] = members_data
            response_dict.append(project_info)

        return response_dict

    def post(self):

        data = request.form

        required_fields = ['name','description', 'github_link','user_id','class_id', 'memebers', 'project_type']
        for field in required_fields:
            if field not in data:
                return {"error": f"'{field}' is required"}, 400
        
        new_project = Project(
            name=data['name'],
            description=data['description'],
            github_link=data['github_link'],
            user_id=data['user_id'],
            class_id=data['class_id'],
            memebers=data['memebers'],
            project_type=data['project_type']
        )

        db.session.add(new_project)
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
        data = request.form

        required_fields = ['name','user_id','admin_id']
        for field in required_fields:
            if field not in data:
                return {"error": f"'{field}' is required"}, 400
            
        new_class = Class(
            name=data['name'],
            user_id=data['user_id'],
            admin_id=data['admin_id']
        )

        db.session.add(new_class)
        db.session.commit()

        response_dict = new_class.to_dict()
        return response_dict,201
    


class ProjectUsersResource(Resource):
    def get(self, id):
        project = Project.query.get(id)

        if project:
            user = User.query.get(project.user_id)  # Get the user who created the project
            if user:
                user_data = {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'role': user.role
                }
                return user_data, 200
            else:
                return {"message": "User not found"}, 404
        return {"message": "Project not found"}, 404

    
class StudentUserResource(Resource):
    def get(self):
        # Get all users with the role "Student"
        student_users = User.query.filter_by(role='Student').all()
        user_list = [user.to_dict() for user in student_users]
        return user_list
    
class ProjectMembersResource(Resource):
    def get(self, project_id):
        # Get the members of a specific project
        project = Project.query.get(project_id)
        if project:
            project_members = project.project_members  # This assumes that you have a back-reference from Project to User for project_members
            members_data = [user.to_dict() for user in project_members]
            return members_data, 200
        return {"message": "Project not found"}, 404


    def post(self):
        data = request.json

        project_id = data.get('project_id')
        user_id = data.get('user_id')

        if project_id is None or user_id is None:
            return {"message": "project_id and user_id are required in the request data"}, 400

        project = Project.query.get(project_id)
        if project is None:
            return {"message": "Project not found"}, 404

        # Check if the user is already a member of the project
        if ProjectMember.query.filter_by(project_id=project_id, user_id=user_id).first() is not None:
            return {"message": "User is already a member of the project"}, 400

        project_member = ProjectMember(project_id=project_id, user_id=user_id)

        try:
            db.session.add(project_member)
            db.session.commit()
            response_dict = project_member.to_dict()
            return response_dict, 201
        except Exception as e:
            db.session.rollback()
            return {"message": "An error occurred while adding the user to the project"}, 500


api.add_resource(ProjectMembersResource, '/projectmembers' )


api.add_resource(StudentUserResource, '/students')
api.add_resource(ClassResource, '/classes')
api.add_resource(ProjectUsersResource, '/projects/<int:id>')
api.add_resource(ProjectByIdResource, '/project/<int:id>')
api.add_resource(ProjectsResource, '/projects')    
api.add_resource(Signup, '/signUp')
api.add_resource(Login, '/login')
        
if __name__ == '__main__':
    app.run(port=5555)