from faker import Faker
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import User, Admin, Class, Project, db

app = Flask(__name__)

# Update the app configuration with your database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project-tracker.db'
db.init_app(app)

# Create tables in the database
with app.app_context():
    db.create_all()

fake = Faker()

# Function to create users
def create_users(num_users):
    for _ in range(num_users):
        user = User(
            username=fake.user_name(),
            email=fake.email(),
            password='your_hashed_password_here'
        )
        db.session.add(user)
    db.session.commit()

# Function to create admins
# Function to create admins
def create_admins(num_admins):
    for _ in range(num_admins):
        # Create a new user for the admin
        user = User(
            username=fake.user_name(),
            email=fake.email(),
            password='your_hashed_password_here'
        )
        db.session.add(user)
        db.session.commit()  # Commit the user to get the user_id

        # Create the admin using the user_id
        admin = Admin(user_id=user.id)
        db.session.add(admin)

    db.session.commit()


# Function to create classes
def create_classes(num_classes):
    for _ in range(num_classes):
        class_obj = Class(
            name=fake.word()
        )
        db.session.add(class_obj)
    db.session.commit()

# Function to create projects
def create_projects(num_projects, num_users, num_classes):
    for _ in range(num_projects):
        project = Project(
            name=fake.sentence(nb_words=3),
            description=fake.paragraph(nb_sentences=3),
            github_link=fake.url(),
            user_id=fake.random_int(min=1, max=num_users),
            class_id=fake.random_int(min=1, max=num_classes)
        )
        db.session.add(project)
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        create_users(num_users=10)  # Adjust the number of users as needed
        create_admins(num_admins=3)  # Adjust the number of admin users as needed
        create_classes(num_classes=5)  # Adjust the number of classes as needed
        create_projects(num_projects=20, num_users=10, num_classes=5)  # Adjust the number of projects as needed
