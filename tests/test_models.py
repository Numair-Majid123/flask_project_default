import pytest
from datetime import datetime, timedelta
from models import User, ToDo, db
from app import app

import sys

sys.path.append("/Users/dev/Downloads/flask_project_default")


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    client = app.test_client()

    with app.app_context():
        db.create_all()

    yield client

    with app.app_context():
        db.drop_all()


def test_user_creation(client):
    with app.app_context():
        user = User(username="testuser", email="test@example.com")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()

        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.check_password("password123")


def test_user_validation(client):
    with app.app_context():
        with pytest.raises(ValueError):
            User(username="", email="test@example.com")

        with pytest.raises(ValueError):
            User(username="testuser", email="invalid_email")

        user = User(username="testuser", email="test@example.com")
        with pytest.raises(ValueError):
            user.set_password("")


def test_todo_creation(client):
    with app.app_context():
        user = User(username="testuser", email="test@example.com")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()

        todo = ToDo(
            title="Test Todo",
            description="This is a test",
            due_date=datetime.now() + timedelta(days=1),
            user_id=user.id,
        )
        db.session.add(todo)
        db.session.commit()

        assert todo.title == "Test Todo"
        assert todo.description == "This is a test"
        assert todo.completed == False


def test_todo_validation(client):
    with app.app_context():
        user = User(username="testuser", email="test@example.com")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()

        with pytest.raises(ValueError):
            ToDo(title="", description="Test", user_id=user.id)

        with pytest.raises(ValueError):
            ToDo(
                title="Test",
                description="Test",
                due_date=datetime.now() - timedelta(days=1),
                user_id=user.id,
            )

        with pytest.raises(ValueError):
            ToDo(title="Test", description="Test", order=-1, user_id=user.id)
