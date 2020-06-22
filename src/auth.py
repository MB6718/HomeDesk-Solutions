from functools import wraps

from flask import session

from database import db

def auth_required(view_func):
	@wraps(view_func)
	def wrapper(*args, **kwargs):
		account_id = session.get('account_id')
		if account_id is None:
			return '', 403
		return view_func(*args, **kwargs, account_id=account_id)
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
		
		if transaction['account_id'] != kwargs['account_id']:
			return '', 403
		
		return view_func(*args, **kwargs)
	return wrapper


def category_owner(view_func):
	@wraps(view_func)
	def wrapper(*args, **kwargs):
		account_id = session.get('account_id')
		with db.connection as con:
			cur = con.execute("""
			SELECT *
			FROM category
			WHERE id = ? AND account_id = ?
			""",
				(kwargs['category_id'],account_id)
			)

			ans = cur.fetchone()
		if not ans:
			return '', 403
		return view_func(*args, **kwargs)

	return wrapper
