from flask import Blueprint

auth_bp = Blueprint('auth', __name__)
attendance_bp = Blueprint('attendance', __name__)
dashboard_bp = Blueprint('dashboard', __name__)

from . import auth, attendance, dashboard
from .main import main_bp