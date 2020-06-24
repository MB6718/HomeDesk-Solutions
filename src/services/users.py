import sqlite3

from werkzeug.security import generate_password_hash


class UsersService:
	def __init__(self, connection):
		self.connection = connection
	
	def stub(self):
		pass

	def add_user(self, user_data):
		email = user_data.get('email')
		first_name = user_data.get('first_name')
		last_name = user_data.get('last_name')
		password = user_data.get('password')
		password_hash = generate_password_hash(password)
		try:
			self.connection.execute("""
				INSERT INTO accounts (first_name, last_name, email, password)
				VALUES (?, ?, ?, ?)
				""",
				(first_name, last_name, email, password_hash)
			)
			self.connection.commit()
		except sqlite3.IntegrityError:
			return 'Данный пользователь уже существует', 409

	def get_user(self, email):
		cur = self.connection.execute("""
			SELECT id, first_name, last_name, email
			FROM accounts
			WHERE email = ?
			""",
			(email,)
		)
		return cur.fetchone()
