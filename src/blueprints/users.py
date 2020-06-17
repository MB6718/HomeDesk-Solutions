import sqlite3

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
	request_json = request.json

	email = request_json.get('email')
	first_name = request_json.get('first_name')
	last_name = request_json.get('last_name')
	password = request_json.get('password')

	password_hash = generate_password_hash(password)
	with db.connection as con:
		try:
			con.execute("""
				INSERT INTO Account (first_name, last_name, email, password)
				VALUES (?, ?, ?, ?)
				""",(first_name, last_name, email, password_hash)
				)
			con.commit()
		except sqlite3.IntegrityError:
			return 'Данный пользователь уже существует', 409
	return request_json, 200
