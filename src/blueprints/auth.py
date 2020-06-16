from flask import (
	Blueprint,
	request,
	session
)

from werkzeug.security import (
	generate_password_hash,
	check_password_hash
)

from database import db

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=["POST"])
def login():
	""" Обработка аутентификации пользователя """
	return 'login - OK', 200

@bp.route('/logout', methods=["POST"])
def logout():
	""" Обработка выхода(деаутентификации) пользователя """
	return 'logout - OK', 200
