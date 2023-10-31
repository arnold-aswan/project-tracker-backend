from app import app, db, User, Project, Admins, Class, ProjectMember
from faker import Faker
import random

fake = Faker()

def generate_fake_data():
    num_users = 10
    num_projects = 20
    num_classes = 5  # Adjust this number as needed

    with app.app_context():
        # Generate fake users
        for _ in range(num_users):
            user = User(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                username=fake.user_name(),
                email=fake.email(),
                password_hash='your_password_hash_here'  # Replace with hashed password
            )
            db.session.add(user)

        # Generate fake projects
        for _ in range(num_projects):
            project = Project(
                name=fake.word(),
                description=fake.sentence(),
                admin_id=random.randint(1, num_users),  # Randomly assign an admin
                github_link=fake.url(),
                class_id=random.randint(1, num_classes),  # Randomly assign a class
            )
            db.session.add(project)

        # seed classes table
        for _ in range(num_classes):
            classs = Class(
                name=fake.word(),
                description=fake.sentence()
            )    
            db.session.add(classs)
            
        db.session.commit()

if __name__ == '__main__':
    generate_fake_data()
