from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from models import db, User, Project, Class , project_members, Admin
from flask_restful import Resource, Api, marshal_with, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project-tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

api = Api(app)

db.init_app(app)


class ProjectsResource(Resource):
    @marshal_with({'id': fields.Integer, 'name': fields.String, 'description': fields.String, 'users': fields.List(fields.String)})


    def get(self):
        # Query the database to get all projects and their associated users
        projects = Project.query.all()

        # Prepare the response data
        result = []
        for project in projects:
            users = [user.username for user in project.project_users]
            project_data = {
                'id': project.id,
                'name': project.name,
                'description': project.description,
                'users': users
            }
            result.append(project_data)

        return result
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
    
api.add_resource(ClassResource, '/classes')
api.add_resource(ProjectUsersResource, '/projects/<int:id>')
api.add_resource(ProjectByIdResource, '/project/<int:id>')
api.add_resource(ProjectsResource, '/projects')
if __name__ == '__main__':
    app.run(port=5555)
