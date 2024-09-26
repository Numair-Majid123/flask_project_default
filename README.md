## Use

* Flask
* Flask-SQLAlchemy

## Install

```
In Terminal:
pip (or pip3) install -r requirements.txt (this depends on how your system is set up)
```
## Run

```
In Terminal:
python (or python3) app.py (this depends on how your system is set up)
```

# Flask ToDo Application

A robust ToDo application built with Flask, featuring user authentication and a dynamic task management system.

## Features

- User registration and authentication
- Create, read, update, and delete ToDo items
- Mark ToDos as complete/incomplete
- Due date tracking for ToDos
- Drag-and-drop reordering of ToDos

## Technologies Used

- Backend: Flask, Flask-SQLAlchemy
- Frontend: HTML, CSS (Bootstrap), JavaScript
- Database: SQLite

## Installation

1. Clone the repository:

```
git clone https://github.com/Numair-Majid123/flask_project_default.git
```

2. Install dependencies:

```
pip install -r requirements.txt
```

## Running the Application

1. Start the Flask server:

```
python app.py
```

2. Open a web browser and navigate to `http://localhost:3000`

## Project Structure

- `app.py`: Main application file
- `models.py`: Database models
- `routes/`: Application routes
- `user_routes.py`: User authentication routes
- `todo_routes.py`: ToDo management routes
- `templates/`: HTML templates
- `static/`: Static files (CSS, JS)

## Makefile Commands

This project includes a Makefile to simplify common development tasks:

- `make setup`: Creates a virtual environment and installs dependencies
- `make run`: Runs the Flask application
- `make test`: Runs the test suite
- `make clean`: Removes the virtual environment and Python cache files
- `make db-init`: Initializes the database
- `make db-migrate`: Creates a new database migration
- `make db-upgrade`: Applies database migrations

To use these commands, simply run `make <command>` in your terminal.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
