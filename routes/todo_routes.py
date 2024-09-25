from flask import Blueprint, request, redirect, url_for, render_template
from flask_login import login_required, current_user
from models import ToDo, db
from datetime import datetime

todo_bp = Blueprint("todo", __name__)


@todo_bp.route("/")
@login_required
def index():
    todos = ToDo.query.filter_by(user_id=current_user.id).order_by(ToDo.order).all()
    return render_template("index.html", todos=todos)


@todo_bp.route("/add_todo", methods=["POST"])
@login_required
def add_todo():
    title = request.form["title"]
    description = request.form["description"]
    due_date = datetime.strptime(request.form["due_date"], "%Y-%m-%d")
    todo = ToDo(
        title=title, description=description, due_date=due_date, user_id=current_user.id
    )
    db.session.add(todo)
    db.session.commit()
    return redirect(url_for("todo.index"))


@todo_bp.route("/edit_todo/<int:id>", methods=["GET", "POST"])
@login_required
def edit_todo(id):
    todo = ToDo.query.get_or_404(id)
    if request.method == "POST":
        todo.title = request.form["title"]
        todo.description = request.form["description"]
        todo.due_date = datetime.strptime(request.form["due_date"], "%Y-%m-%d")
        db.session.commit()
        return redirect(url_for("todo.todo_list"))
    return render_template("edit_todo.html", todo=todo)


@todo_bp.route("/delete_todo/<int:id>")
@login_required
def delete_todo(id):
    todo = ToDo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("todo.todo_list"))


@todo_bp.route("/complete_todo/<int:id>")
@login_required
def complete_todo(id):
    todo = ToDo.query.get_or_404(id)
    todo.completed = not todo.completed
    db.session.commit()
    return redirect(url_for("todo.todo_list"))


@todo_bp.route("/reorder_todos", methods=["POST"])
@login_required
def reorder_todos():
    new_order = request.json["new_order"]
    for index, todo_id in enumerate(new_order):
        todo = ToDo.query.get(todo_id)
        todo.order = index
    db.session.commit()
    return "", 204


@todo_bp.route("/todos")
@login_required
def todo_list():
    current_date = datetime.now().date()
    todos = ToDo.query.filter_by(user_id=current_user.id).order_by(ToDo.order).all()
    return render_template("todo_list.html", todos=todos, current_date=current_date)
