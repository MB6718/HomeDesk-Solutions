import sqlite3

from marshmallow import (
	Schema,
	fields,
	ValidationError
)

from flask import (
	Blueprint,
	request,
	jsonify
)

from werkzeug.security import generate_password_hash

from database import db

bp = Blueprint('users', __name__)


class UsersSchema(Schema):
	email = fields.Email()
	password = fields.Str()
	first_name = fields.Str()
	last_name = fields.Str()


@bp.route('', methods=['POST'])
def users():
	""" Обработка регистрации нового пользователя """
	request_json = request.json

	try:
		validation = UsersSchema().load(request_json)
	except ValidationError as err:
		return err.messages, 400

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

		cur = con.execute("""
		SELECT id, first_name, last_name, email
		FROM account
		WHERE email=?""",
		(email,)
		)
		response = cur.fetchone()
	return jsonify(dict(response)), 200
