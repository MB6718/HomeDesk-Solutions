from flask import (
	Blueprint,
	request,
	jsonify
)

from werkzeug.security import (
	generate_password_hash,
	check_password_hash
)

from src.auth import auth_required

from src.database import db

from src.services.users import UsersService

bp = Blueprint('users', __name__)

@bp.route('', methods=["POST"])
def users():
	""" Обработка регистрации нового пользователя """
	#""" проверка коммита """
	return 'users POST - OK', 200
