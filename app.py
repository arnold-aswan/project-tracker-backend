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
CORS(app)
# CORS(app, resources={r"/projects/*": {"origins": "http://localhost:5173"}, r"/login": {"origins": "http://localhost:5173"}})


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
        
        response_dict = {
            'id': new_user.id,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'username': new_user.username,
            'email': new_user.email,
            'role': new_user.role
        }

        return make_response(jsonify({"message": "user created successfully", "user": response_dict}), 201)

class Login(Resource):
    def post(self):
        data = login_parser.parse_args()
        email = data['email']
        password = data['password']
        role = data['role']

        db_user = User.query.filter_by(email=email).first()

        if db_user and check_password_hash(db_user.password, password):
            if db_user.role == role:
                access_token = create_access_token(identity=db_user.email, fresh=True)
                refresh_token = create_refresh_token(identity=db_user.email)
                return jsonify({"access_token": access_token, "refresh_token": refresh_token, "role": role, "user_id": db_user.id,})
            else:
                return make_response(jsonify({"message": "Invalid role for this user"}), 401)
        else:
            return make_response(jsonify({"message": "Invalid email or password"}), 401)
# api.add_resource(Projects, '/projects')

class UsersResource(Resource):
    def get(self):
        # Assuming 'Project' is the SQLAlchemy model for projects
        users = User.query.all()
        
        response_dict = [{
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'firstname': user.firstname,
            'lastname': user.lastname,
            'role': user.role,
            
        } for user in users]

        return response_dict, 200
class ProjectsResource(Resource):
    def get(self):
        projects = Project.query.all()
        response_dict = []

        for project in projects:
            user = User.query.get(project.user_id) 

            project_info = {
                'id': project.id,
                'name': project.name,
                'description': project.description,
                'github_link': project.github_link,
                'user_id': project.user_id,
                'class_id': project.class_id,
                'members': project.memebers,
                'project_type': project.project_type,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'role': user.role
                }
            }
            response_dict.append(project_info)

        return response_dict
    def post(self):

        data = request.get_json()

        required_fields = ['name','description', 'github_link','user_id','class_id', 'project_type'] #<='memebers'
        for field in required_fields:
            if field not in data:
                return {"error": f"'{field}' is required"}, 400

        memebers = data.get('memebers', [])
        
        new_project = Project(
            name=data['name'],
            description=data['description'],
            github_link=data['github_link'],
            user_id=data['user_id'],
            class_id=data['class_id'],
            # memebers=data['memebers'],
            memebers=', '.join(memebers),
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
        # data = request.form
        data = request.get_json()

        required_fields = ['name','admin_id'] #'<=user_id'
        for field in required_fields:
            if field not in data:
                return {"error": f"'{field}' is required"}, 400
            
        new_class = Class(
            name=data['name'],
            # user_id=data['user_id'],
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

api.add_resource(UsersResource, '/users')
api.add_resource(StudentUserResource, '/students')
api.add_resource(ClassResource, '/classes')
api.add_resource(ProjectUsersResource, '/projects/<int:id>')
api.add_resource(ProjectByIdResource, '/project/<int:id>')
api.add_resource(ProjectsResource, '/projects')    
api.add_resource(Signup, '/signUp')
api.add_resource(Login, '/login')
        
if __name__ == '__main__':
    app.run(port=5555)