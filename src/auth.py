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


def must_be_owner(of):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(*args, **kwargs):
                name = {
                    'category': 'categories',
                    'transaction': 'transactions',
                }[of]
                with db.connection as con:
                    cur = con.execute(f"""
                        SELECT f.account_id
                        FROM {name} AS f
                        WHERE f.id = ?
                        """,
                        (kwargs[f'{of}_id'],)
                    )
                    result = cur.fetchone()
                if not result:
                    return '', 404
                if result['account_id'] != kwargs['account_id']:
                    return '', 403
            return view_func(*args, **kwargs)
        return wrapper
    return decorator
