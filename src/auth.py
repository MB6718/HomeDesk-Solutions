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


def must_be_owner(who_is=None):
	def decorator(view_func):
		@wraps(view_func)
		def wrapper(*args, **kwargs):
			if who_is is not None and who_is in ('transaction', 'category'):
				if who_is is 'category':
					name = 'categories'
				else:
					name = 'transactions'
				with db.connection as con:
					cur = con.execute(f"""
						SELECT f.account_id
						FROM {name} AS f
						WHERE f.id = ?
						""",
						(kwargs[f'{who_is}_id'],)
					)
					result = cur.fetchone()
				if not result:
					return '', 404
				if result['account_id'] != kwargs['account_id']:
					return '', 403
			return view_func(*args, **kwargs)
		return wrapper

	return decorator
