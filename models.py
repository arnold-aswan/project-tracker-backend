from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Table

# Create an instance of SQLAlchemy
from exts import db

#many-to-many relationship between users and projects using project members table
class ProjectMember(db.Model):
    __tablename__ = 'project_members'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    #Many to many relationshio with the user and projects
    projects = db.relationship('Project', secondary=ProjectMember.__table__, back_populates='users')

class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    github_link = db.Column(db.String(255), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    memebers = db.Column(db.String)
    project_type = db.Column(db.String(50), nullable=True)



    # Rename the 'group_projects' property to 'project_users'.
    project_users = db.relationship('User', secondary='project_members', back_populates='project_members')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'github_link': self.github_link,
            'user_id':self.user_id,
            'class_id':self.class_id,
            'members':self.memebers,
            'project_type':self.project_type
        }

project_members = db.Table('project_members',
    db.Column('project_id', db.Integer, db.ForeignKey('projects.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)

# user_in_project = db.Table('user_in_project',
#     db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
#     db.Column('project_id', db.Integer, db.ForeignKey('projects.id'), primary_key=True)
# )

# class User_in_project(db.Model):
#     __tablename__ = 'users_in_project'

#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#     project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))

#     user = db.relationship('User', backref='projects_participated', lazy=True)
#     project = db.relationship('Project', backref='project_participants', lazy=True)
