# TaskNest Backend

## Project Goals

This project provides a Django Rest Framework API for the [TaskNest React web app](https://github.com/BrrunaRibeiro/tasknest-react). TaskNest is designed to help users efficiently manage tasks with filtering, prioritization, and intuitive interaction features.

The primary goals of the TaskNest backend are to:
1. Provide a robust and secure API to support task management functionality in the frontend application.
2. Implement a scalable and modular backend to accommodate future enhancements, such as collaboration features.
3. Ensure security, scalability, and maintainability through adherence to best practices in API design and defensive programming.

## Table of Contents

- [Project Goals](#project-goals)
- [Planning](#planning)
  - [Data Models](#data-models)
- [API Endpoints](#api-endpoints)
- [Frameworks, Libraries, and Dependencies](#frameworks-libraries-and-dependencies)
- [Testing](#testing)
  - [Manual Testing](#manual-testing)
  - [Automated Tests](#automated-tests)
  - [Python Validation](#python-validation)
  - [Resolved Bugs](#resolved-bugs)
  - [Unresolved Bugs](#unresolved-bugs)
- [Deployment](#deployment)
- [Credits](#credits)

---

## Planning

### Data Models

#### ERD

<p align="center">
    <img src="readmeassets/erd-models-tasknest.png" width=600>
</p>

#### **Task**
The `Task` model represents a task and includes:
- **Title:** A brief description of the task.
- **Description:** Detailed information about the task.
- **Priority:** The urgency level of the task (`low`, `medium`, `high`).
- **State:** The status of the task (`open`, `completed`).
- **Due Date:** When the task is expected to be completed.
- **Category:** The type of task (e.g., "Work", "Personal").
- **Owners:** A many-to-many relationship with the `User` model, allowing task sharing.

#### **Category**
The `Category` model provides categories for task classification. It includes:
- **Name:** A unique category name.

---

## API Endpoints

| **URL**             | **Notes**                                      | **HTTP Method** | **CRUD Operation** | **View Type**      | **Data Format**                                                                                   |
|----------------------|------------------------------------------------|-----------------|---------------------|--------------------|---------------------------------------------------------------------------------------------------|
| `/tasks/`           | List or filter tasks by priority, state, etc.  | GET             | Read                | List               | -                                                                                                 |
| `/tasks/<id>/`      | Retrieve, update, or delete a specific task.    | GET, PUT, PATCH, DELETE | Read, Update, Delete | Detail             | `{ "title": "string", "description": "string", "priority": "low/medium/high", "state": "open/completed" }` |
| `/create-task/`     | Create a new task.                              | POST            | Create              | Detail             | `{ "title": "string", "description": "string", "priority": "low/medium/high", "state": "open/completed" }` |
| `/categories/`      | List or create categories.                      | GET, POST       | Read, Create        | List               | `{ "name": "string" }`                                                                            |
| `/categories/<id>/` | Retrieve, update, or delete a specific category.| GET, PUT, DELETE| Read, Update, Delete| Detail             | `{ "name": "string" }`                                                                            |
| `/check-email/`     | Verify if an email is already registered.       | GET             | Read                | Utility            | -                                                                                                 |

---

## Frameworks, Libraries, and Dependencies

### Python Libraries

- **Django**: Web framework for developing the backend.
- **Django Rest Framework**: For building RESTful APIs.
- **dj-rest-auth**: Provides endpoints for authentication and registration.
- **djangorestframework-simplejwt**: Enables JSON Web Token (JWT) authentication.
- **django-filter**: Adds filtering capabilities to the API.
- **django-cors-headers**: Handles Cross-Origin Resource Sharing (CORS).
- **dj-database-url**: Parses database configuration from environment variables.
- **Cloudinary**: For managing media storage.
- **gunicorn**: Production WSGI server for Python applications.

### Frontend Integration
The backend integrates with the TaskNest React frontend via its exposed RESTful API endpoints.

---

## Testing

### Manual Testing
Manual testing was conducted for all endpoints using Postman and the Django Rest Framework's built-in interface. Key tests included:
- Verifying CRUD operations for tasks and categories.
- Ensuring email validation functionality works correctly.
- Checking authentication flows for JWT tokens.

### Automated Tests
The following test cases were implemented using Django's `APITestCase`:
- **Task Creation**
  - Successfully create a task with all required fields.
  - Validate missing fields and raise appropriate errors.
  - Prevent creation with invalid due dates.
- **Task Retrieval**
  - Allow task owners to view their tasks.
  - Prevent unauthorized access to tasks.

### Python Validation
All Python code was validated using the [PEP8CI Linter](https://pep8ci.herokuapp.com/), with no errors found.

---

## Deployment

The backend is deployed on Heroku. Follow these steps to replicate the deployment:
1. Fork or clone the repository.
2. Set up a PostgreSQL database.
3. Configure the following environment variables in Heroku:
   - `DATABASE_URL`: PostgreSQL connection string.
   - `CLOUDINARY_URL`: Cloudinary credentials.
   - `SECRET_KEY`: Django secret key.
   - `ALLOWED_HOST`: Allowed hosts for production.
4. Deploy using the Heroku CLI or GitHub integration.

---

## Credits

- [Django documentation](https://docs.djangoproject.com/en/stable/)
- [Django Rest Framework documentation](https://www.django-rest-framework.org/)
- [django-cors-headers documentation](https://pypi.org/project/django-cors-headers/)
- [Cloudinary documentation](https://cloudinary.com/documentation)

