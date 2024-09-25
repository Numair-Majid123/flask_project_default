import pytest
from app import app, db
from flask import url_for
from models import ToDo, User
from datetime import datetime, timedelta


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


@pytest.fixture
def authenticated_client(client):
    with app.app_context():
        user = User(username="testuser", email="test@example.com")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()

    client.post("/login", data={"username": "testuser", "password": "password123"})
    return client


def test_index(authenticated_client):
    with app.test_request_context():
        response = authenticated_client.get(url_for("todo.index"))
        assert response.status_code == 200


def test_add_todo(authenticated_client):
    with app.test_request_context():
        response = authenticated_client.post(
            url_for("todo.add_todo"),
            data={
                "title": "Test Todo",
                "description": "Test Description",
                "due_date": "2025-12-31",
            },
        )
        assert response.status_code == 302
        assert ToDo.query.filter_by(title="Test Todo").first() is not None


def test_edit_todo(authenticated_client):
    with app.app_context():
        todo = ToDo(
            title="Original Todo",
            description="Original Description",
            due_date=datetime.now() + timedelta(1),
            user_id=1,
        )
        db.session.add(todo)
        db.session.commit()
        todo_id = todo.id

    with app.test_request_context():
        response = authenticated_client.post(
            url_for("todo.edit_todo", id=todo_id),
            data={
                "title": "Updated Todo",
                "description": "Updated Description",
                "due_date": "2025-12-31",
            },
        )
        assert response.status_code == 302
        assert ToDo.query.get(todo_id).title == "Updated Todo"


def test_delete_todo(authenticated_client):
    with app.app_context():
        todo = ToDo(
            title="To Delete",
            description="Will be deleted",
            due_date=datetime.now() + timedelta(1),
            user_id=1,
        )
        db.session.add(todo)
        db.session.commit()
        todo_id = todo.id

    with app.test_request_context():
        response = authenticated_client.get(url_for("todo.delete_todo", id=todo_id))
        assert response.status_code == 302
        assert ToDo.query.get(todo_id) is None


def test_complete_todo(authenticated_client):
    with app.app_context():
        todo = ToDo(
            title="To Complete",
            description="Will be completed",
            due_date=datetime.now() + timedelta(1),
            user_id=1,
        )
        db.session.add(todo)
        db.session.commit()
        todo_id = todo.id
    with app.test_request_context():
        response = authenticated_client.get(url_for("todo.complete_todo", id=todo_id))
        assert response.status_code == 302
        assert ToDo.query.get(todo_id).completed == True


def test_reorder_todos(authenticated_client):
    with app.app_context():
        todo1 = ToDo(title="Todo 1", user_id=1, order=0)
        todo2 = ToDo(title="Todo 2", user_id=1, order=1)
        db.session.add_all([todo1, todo2])
        db.session.commit()
        with app.test_request_context():
            response = authenticated_client.post(
                url_for("todo.reorder_todos"), json={"new_order": [todo2.id, todo1.id]}
            )
            assert response.status_code == 204

            db.session.refresh(todo1)
            db.session.refresh(todo2)

            assert todo1.order == 1
            assert todo2.order == 0


def test_todo_list(authenticated_client):
    with app.test_request_context():
        response = authenticated_client.get(url_for("todo.todo_list"))
        assert response.status_code == 200
