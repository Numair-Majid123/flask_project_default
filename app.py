from flask import Flask, redirect,request, flash
from flask_login import (
    LoginManager,
)
from models import db, User
from routes.user_routes import user_bp
from routes.todo_routes import todo_bp

app = Flask(__name__)
app.config["SECRET_KEY"] = (
    "\x14B~^\x07\xe1\x197\xda\x18\xa6[[\x05\x03QVg\xce%\xb2<\x80\xa4\x00"
)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///book.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["DEBUG"] = True

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = "user.login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.errorhandler(Exception)
def handle_exception(err):
    if len(err.args) > 0:
        flash(err.args[0])
    else:
        flash(str(err))
    return redirect(request.url)

app.register_blueprint(user_bp)
app.register_blueprint(todo_bp)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(port=3000)
