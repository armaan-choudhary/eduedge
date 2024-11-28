from flask import Flask
from flask_login import LoginManager
from config import Config
from models import create_tables, initialize_roles, get_user_by_id
from user import User

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id):
    user_data = get_user_by_id(user_id)
    if user_data:
        return User(
            id=user_data[0],
            firstname=user_data[1],
            lastname=user_data[2],
            username=user_data[3],
            password=user_data[4],
            role_id=user_data[5],
        )
    return None


# Register blueprints
from routes import auth_bp, attendance_bp, dashboard_bp, main_bp

app.register_blueprint(auth_bp)
app.register_blueprint(attendance_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(main_bp)

if __name__ == "__main__":
    create_tables()
    initialize_roles()
    app.run(debug=True)
