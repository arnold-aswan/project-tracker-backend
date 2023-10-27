from flask import Flask
from flask_migrate import Migrate
from models import db, User, Project, Admins, Class, ProjectMember
from flask_restful import Resource, Api
from flask_cors import CORS  # pip install flask-cors

app = Flask(__name__)
CORS(app)   # for cross origin 

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
    
# Classes route
class Cohort(Resource):
    def get(self):
        cohorts = [cohort.to_dict() for cohort in Class.query.all()]
        
        response_dict = {
            "cohorts" : cohorts
        }    
        
        return response_dict, 200    

api.add_resource(Projects, '/projects')
api.add_resource(Cohort, "/class")


if __name__ == '__main__':
    app.run(port=5555)