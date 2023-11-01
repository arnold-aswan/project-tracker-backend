from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Table
from sqlalchemy import CheckConstraint


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
    role = db.Column(db.String(20), nullable=False, server_default='student')
    
    # Add a CheckConstraint to enforce role values
    __table_args__ = (
        CheckConstraint(role.in_(('student', 'admin')), name='role_check'),
    )

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    #Many to many relationshio with the user and projects
    projects = db.relationship('Project', secondary=ProjectMember.__table__, back_populates='users')

class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(80), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('admins.id'))
    github_link = db.Column(db.String(80), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    #Many-to-one relationship with admins
    admin = db.relationship('Admins', back_populates='projects')

    #Many-to-one relationship with classes
    project_class = db.relationship('Class', back_populates='projects')

    #Many-to-many relationship with users
    users = db.relationship('User', secondary=ProjectMember.__table__, back_populates='projects')
    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'admin_id': self.admin_id,
            'github_link': self.github_link,
            'class_id': self.class_id,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        }

        if self.updated_at:
            data['updated_at'] = self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        else:
            data['updated_at'] = None

        if self.admin:
            data['admin'] = self.admin.to_dict()
        else:
            data['admin'] = None

        if self.project_class:
            data['project_class'] = self.project_class.to_dict()
        else:
            data['project_class'] = None

        data['users'] = [user.to_dict() for user in self.users]

        return data

class Admins(db.Model):
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    #One-to-many relationship with projects
    projects = db.relationship('Project', back_populates='admin')

class Class(db.Model):
    __tablename__ = 'classes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(80), nullable=False)

    #One-to-many relationship with projects
    projects = db.relationship('Project', back_populates='project_class')

    def to_dict(self):
        return {
            'id':self.id,
            'name': self.name,
            'description': self.description,
        }