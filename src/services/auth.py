from werkzeug.security import check_password_hash

from exceptions import PermissionError


class AuthService:
    def __init__(self, connection):
        self.connection = connection
    
    def login_user(self, auth_data):
        cur = self.connection.cursor()
        cur.execute("""
            SELECT *
            FROM accounts
            WHERE email = ?
            """,
            (auth_data['email'],)
        )
        user = cur.fetchone()
        if user is not None:
            check_password = check_password_hash(
                user['password'],
                auth_data['password']
        )
        if user is None or not check_password:
            raise PermissionError
        return user['id']
