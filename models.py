from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    # Rename the 'project_members_relationship' property to 'project_members'.
    project_members = db.relationship('Project', secondary='project_members', back_populates='project_users')

    # Define a one-to-many relationship for projects created by this user.
    projects = db.relationship('Project', backref='owner', lazy=True)

class Admin(db.Model):
    __tablename__ = 'admin'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    user = db.relationship('User', backref='admin')

    def __init__(self, user_id):
        self.user_id = user_id

class Class(db.Model):
    __tablename__ = 'classes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    # Foreign key for regular users
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Foreign key for admin users
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Define relationships for regular users and admin users
    users = db.relationship('User', backref='class', lazy=True, foreign_keys="Class.user_id")
    admin = db.relationship('User', backref='admin_classes', lazy=True, foreign_keys="Class.admin_id")

    def to_dict(self):
        return{
            'id':self.id,
            'name':self.name,
            'user_id':self.user_id,
            'admin_id':self.admin_id
        }


class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    github_link = db.Column(db.String(255), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)

    # Rename the 'group_projects' property to 'project_users'.
    project_users = db.relationship('User', secondary='project_members', back_populates='project_members')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'github_link': self.github_link,
            'user_id':self.user_id,
            'class_id':self.class_id
        }

project_members = db.Table('project_members',
    db.Column('project_id', db.Integer, db.ForeignKey('projects.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)
