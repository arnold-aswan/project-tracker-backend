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
jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = 'your_secret_key_here'

# Define API models using reqparse and fields


# api.add_resource(Projects, '/projects')
class ProjectsResource(Resource):
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
            users = project.project_users  # Access the project_users relationship
            user_data = [{'id': user.id, 'username': user.username, 'email': user.email} for user in users]
            return user_data, 200
        return {"message": "Project not found"}, 404
    
class StudentUserResource(Resource):
    def get(self):
        # Get all users with the role "Student"
        student_users = User.query.filter_by(role='Student').all()
        user_list = [user.to_dict() for user in student_users]
        return user_list

api.add_resource(StudentUserResource, '/students')
api.add_resource(ClassResource, '/classes')
api.add_resource(ProjectUsersResource, '/projects/<int:id>')
api.add_resource(ProjectByIdResource, '/project/<int:id>')
api.add_resource(ProjectsResource, '/projects')    

        
if __name__ == '__main__':
    app.run(port=5555)