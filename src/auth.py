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
