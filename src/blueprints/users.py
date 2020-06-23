import sqlite3

from marshmallow import ValidationError

from flask import (
	Blueprint,
	request,
	jsonify
)

from werkzeug.security import generate_password_hash

from database import db

from services.validations import UsersSchema

from services.users import UsersService

bp = Blueprint('users', __name__)


@bp.route('', methods=['POST'])
def users():
	""" Обработка регистрации нового пользователя """
	request_json = request.json
	try:
		user_data = UsersSchema().load(request_json)
	except ValidationError as err:
		return err.messages, 400

	with db.connection as con:
		us = UsersService(con)
		us.add_user(user_data)
		response = us.get_user(user_data.get('email'))
	return jsonify(dict(response)), 201
