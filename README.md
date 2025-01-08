# Projects API

REST API for project and team management.

## Features

- Create, update, and delete projects
- Task management within projects
- User creation and assignment to projects
- Commenting system for tasks
- MongoDB integration for data storage

## Requirements

- Python 3.7+
- Flask
- Flask-PyMongo
- PyYAML
- MongoDB
- Docker and Docker Compose

## Installation and Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/lukasz-cz/projects_api.git
    cd projects_api
    ```

2. Build and start the application using Docker Compose:
    ```bash
    docker-compose up --build
    ```

3. The API will be accessible on `http://127.0.0.1:5000`.

## Usage

Use tools like Postman or `curl` to interact with the API. Below are the main endpoints:

### Projects
- `POST /projects` - Create a new project.
- `GET /projects` - Retrieve all projects.
- `GET /projects/<project_id>` - Retrieve details of a specific project.
- `PUT /projects/<project_id>` - Update a project.
- `DELETE /projects/<project_id>` - Delete a project.

### Tasks
- `POST /projects/<project_id>/tasks` - Add a task to a project.
- `GET /projects/<project_id>/tasks` - Retrieve tasks for a project.
- `GET /projects/<project_id>/tasks/<task_id>` - Retrieve task details.
- `PUT /projects/<project_id>/tasks/<task_id>` - Update a task.
- `DELETE /projects/<project_id>/tasks/<task_id>` - Delete a task.

### Users
- `POST /members` - Create a new user.
- `GET /members` - Retrieve all users.
- `GET /members/<user_id>` - Retrieve details of a specific user.

### Team Management
- `POST /projects/<project_id>/members/<user_id>` - Add a user to a project.
- `GET /projects/<project_id>/members` - Retrieve all users assigned to a project.
- `DELETE /projects/<project_id>/members/<user_id>` - Remove a user from a project.

### Comments
- `POST /projects/<project_id>/tasks/<task_id>/comments` - Add a comment to a task.
- `GET /projects/<project_id>/tasks/<task_id>/comments` - Retrieve comments for a task.
- `DELETE /projects/<project_id>/tasks/<task_id>/comments/<comment_id>` - Delete a comment from a task.

## Example

Below is an example of creating a project using `curl`:
```bash
curl -X POST http://localhost:5000/projects \
-H "Content-Type: application/json" \
-d '{
    "name": "Project A",
    "description": "Description of Project A",
    "start_date": "2025-01-01",
    "end_date": "2025-12-31"
}'
```

Response:
```json
{
    "id": "60f8a2b48f629e001e5e3c1a"
}
```

## License

This project is licensed under the MIT License.
