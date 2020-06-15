from flask import (
	Blueprint,
	request,
	jsonify
)

from werkzeug.security import (
	generate_password_hash,
	check_password_hash
)

from auth import auth_required

from database import db

from services.users import UsersService

bp = Blueprint('users', __name__)

@bp.route('', methods=["POST"])
def users():
	""" Обработка регистрации нового пользователя """
	return 'users POST - OK', 200
