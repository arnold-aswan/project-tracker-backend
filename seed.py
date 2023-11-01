from faker import Faker
from app import app, db
from models import User, Class, Project

fake = Faker()

def seed_users(num_users):
    for _ in range(num_users):
        user = User(
            username=fake.user_name(),
            email=fake.email(),
            password=fake.password(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            role=fake.random_element(elements=("Student", "Admin", "Teacher"))
        )
        db.session.add(user)

def seed_classes(num_classes):
    for _ in range(num_classes):
        class_name = fake.unique.first_name()
        # Retrieve random user IDs and admin IDs differently
        user_ids = [user.id for user in User.query.all()]
        admin_ids = [user.id for user in User.query.all()]
        user_id = fake.random_element(user_ids)
        admin_id = fake.random_element(admin_ids)
        class_instance = Class(
            name=class_name,
            user_id=user_id,
            admin_id=admin_id
        )
        db.session.add(class_instance)

def seed_projects(num_projects):
    for _ in range(num_projects):
        project_name = fake.catch_phrase()
        project_description = fake.text()
        github_link = fake.url()
        user_id = fake.random_element([user.id for user in User.query.all()])
        class_ids = [cls.id for cls in Class.query.all()]
        class_id = fake.random_element(class_ids)
        memebers = fake.first_name()
        project_type = fake.random_element(elements=("Open Source", "Team Project", "Individual Project"))
        project = Project(
            name=project_name,
            description=project_description,
            github_link=github_link,
            user_id=user_id,
            class_id=class_id,
            memebers=memebers,
            project_type=project_type
        )
        db.session.add(project)

with app.app_context():
    db.create_all()
    seed_users(10)
    seed_classes(5)
    seed_projects(20)
    db.session.commit()