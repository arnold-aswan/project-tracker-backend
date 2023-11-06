from faker import Faker
from app import db, app, User, Class, Project, ProjectMember
from sqlalchemy import func

fake = Faker()

def create_fake_users(num_users):
    with app.app_context():
        for _ in range(num_users):
            user = User(
                username=fake.user_name(),
                email=fake.email(),
                password=fake.password(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                role=fake.random_element(elements=("Student", "Admin"))
            )
            db.session.add(user)

def create_fake_classes(num_classes):
    with app.app_context():
        max_user_id = db.session.query(func.max(User.id)).scalar()
        if max_user_id is None:
            max_user_id = 1

        for _ in range(num_classes):
            class_name = fake.catch_phrase()
            user_id = fake.random_int(min=1, max=max_user_id)
            admin_id = fake.random_int(min=1, max=max_user_id)
            new_class = Class(name=class_name, user_id=user_id, admin_id=admin_id)
            db.session.add(new_class)

def create_fake_projects(num_projects):
    with app.app_context():
        for _ in range(num_projects):
            project = Project(
                name=fake.catch_phrase(),
                description=fake.text(max_nb_chars=200),
                github_link=fake.url(),
                user_id=fake.random_int(min=1, max=User.query.count()),
                class_id=fake.random_int(min=1, max=Class.query.count()),
                memebers=fake.random_element(elements=("Student")),
                project_type=fake.random_element(elements=("Android", "Fullstack"))
            )
            db.session.add(project)

def create_fake_project_members(num_project_members):
    with app.app_context():
        for _ in range(num_project_members):
            project_id = fake.random_int(min=1, max=Project.query.count())
            user_id = fake.random_int(min=1, max=User.query.count())
            project_member = ProjectMember(project_id=project_id, user_id=user_id)
            db.session.add(project_member)

if __name__ == '__main__':
    # Number of fake records to create
    num_fake_users = 10
    num_fake_classes = 5
    num_fake_projects = 15
    num_fake_project_members = 20

    # clear database
    db.delete(User)
    db.delete(Class)
    db.delete(Project)
    db.delete(ProjectMember)

    # Create fake data for each table
    create_fake_users(num_fake_users)
    create_fake_classes(num_fake_classes)
    create_fake_projects(num_fake_projects)
    create_fake_project_members(num_fake_project_members)

    # Commit changes and close the session
    with app.app_context():
        db.session.commit()
