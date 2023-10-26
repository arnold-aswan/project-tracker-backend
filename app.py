from flask import Flask
from flask_migrate import Migrate
from models import db, User, Project, Admins, Class, ProjectMember
from flask_restful import Resource, Api
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project-tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app,db)



api = Api(app)

db.init_app(app)

class Projects(Resource):

    def get(self):
        projects = [project.to_dict() for project in Project.query.all()]

        response_dict = {
            "projects": projects  
        }

        return response_dict, 200

api.add_resource(Projects, '/projects')



if __name__ == '__main__':
    app.run(port=5555)