# Project Tracker Backend README

## Overview

The Project Tracker backend is a Flask-based API for managing users, projects, classes, and their relationships.

## Technologies used
```python

1. Flask: Micro web framework
2. SQLAlchemy: SQL toolkit and ORM
3. Flask-Migrate: Database migrations
4. Flask-RESTful: RESTful API building
5. Flask-JWT-Extended: JWT support
6. Flask-CORS: Cross-Origin Resource Sharing
7. Alembic: Database migrations tool
8. SQLite: Database system (for development)
```

## Project Structure
Project structure:

- app.py: Main Flask application
- models.py: Data models (users, projects, classes)
- alembic: Database migrations
- README.md: This documentation.

## Getting Started
To set up the backend, follow these steps:

Clone the project.
```bash
# Install required packages
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start the Flask app
python app.py

The backend will run at http://localhost:5555.

```
## API Endpoints
API endpoints:

- /signUp: Register a new user.
- /login: Authenticate a user and receive a JWT token for authorization.
- /classes: Manage classes (GET: Retrieve classes, POST: Create a new class).
- /students: Retrieve a list of students (users with the "Student" role).
- /projects: Manage projects (GET: Retrieve projects, POST: Create a new project).
- /project/<int:id>: Retrieve or delete a project by its ID.
- /projects/<int:id>: Retrieve the user information of a project's owner.
- /projectmembers: Manage project members (GET: Retrieve project members, POST: Add a user as a member to a project).

## Migrations
The project uses Alembic for managing database migrations. When making changes to the database schema, you can generate and apply migrations using the following commands:

```bash

# Create a new migration
flask db migrate

# Apply the migration
flask db upgrade

```

## License
This project is MIT-licensed. [https://opensource.org/license/mit/]

## Acknowledgments
- Flask: https://flask.palletsprojects.com/
SQLAlchemy: https://www.sqlalchemy.org/
- Flask-RESTful: https://flask-restful.readthedocs.io/
- Flask-Migrate: https://flask-migrate.readthedocs.io/
- Flask-JWT-Extended: https://flask-jwt-extended.readthedocs.io/
- Werkzeug: https://werkzeug.palletsprojects.com/
- CORS: https://flask-cors.readthedocs.io/

## Contact
For inquiries or support, contact:
   - Arnold Aswani.
   - Ephrahim Lenaiayasa.
   - Antonia Njuguna.




