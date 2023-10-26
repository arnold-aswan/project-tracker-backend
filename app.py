from flask import Flask
from flask_migrate import Migrate
from models import db, User, Project, Admins, Class, ProjectMember

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project-tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app,db)





db.init_app(app)