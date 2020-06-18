from functools import wraps

from flask import session

from database import db

def auth_required(view_func):
	@wraps(view_func)
	def wrapper(*args, **kwargs):
		user_id = session.get('user_id')
		if user_id is None:
			return '', 403
		return view_func(*args, **kwargs, user_id=user_id)
	return wrapper

def transaction_owner(view_func):
	@wraps(view_func)
	def wrapper(*args, **kwargs):
		with db.connection as con:
			cur = con.execute("""
				SELECT t.account_id
				FROM transactions AS t
				WHERE t.id = ?
				""",
				(kwargs['transaction_id'],)
			)
			transaction = cur.fetchone()
		
		if not transaction:
			return '', 404
		
		if transaction['account_id'] != kwargs['user_id']:
			return '', 403
		
		return view_func(*args, **kwargs)
	return wrapper
