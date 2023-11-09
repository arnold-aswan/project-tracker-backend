from models import db, User, Class, Project
from app import app
from faker import Faker

fake = Faker()
def test_user_to_dict():
    with app.app_context():
        username = fake.user_name()
        email = fake.email()
        first_name=fake.first_name()
        last_name=fake.last_name()
        user = User(username=username, email=email, first_name=first_name, last_name=last_name, password='password', role="Student")
        db.session.add(user)
        db.session.commit()
        
        user_dict = user.to_dict()
        assert user_dict['username'] == username
        assert user_dict['email'] == email
        assert user_dict['first_name'] == first_name
        assert user_dict['last_name'] == last_name
        assert user_dict['role'] == 'Student'
    
# def test_class_to_dict():
#     class_ = Class(name='Test Class')
#     db.session.add(class_)
#     db.session.commit()
    
#     class_dict = class_.to_dict()
#     assert class_dict['name'] == 'Test Class'
#     # Add more assertions as needed
    
# def test_project_to_dict():
#     project = Project(
#         name='Test Project',
#         description='This is a test project',
#         github_link='https://github.com/test/testproject',
#         user_id=1,  # Assuming a user with ID 1 exists
#         class_id=1,  # Assuming a class with ID 1 exists
#         members='John, Jane',
#         project_type='Test'
#     )
#     db.session.add(project)
#     db.session.commit()
    
#     project_dict = project.to_dict()
#     assert project_dict['name'] == 'Test Project'
#     assert project_dict['description'] == 'This is a test project'
#     assert project_dict['github_link'] == 'https://github.com/test/testproject'
#     assert project_dict['user_id'] == 1
#     assert project_dict['class_id'] == 1
#     assert project_dict['members'] == 'John, Jane'
#     assert project_dict['project_type'] == 'Test'
    # Add more assertions as needed

# with app.app_context():
#     test_user_to_dict()