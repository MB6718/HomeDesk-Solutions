import sqlite3
from werkzeug.security import generate_password_hash

from exceptions import ConflictError


class UsersService:
    def __init__(self, connection):
        self.connection = connection
    
    def add_user(self, user):
        try:
            self.connection.execute("""
                INSERT INTO accounts (first_name, last_name, email, password)
                VALUES (?, ?, ?, ?)
                """,
                (user['first_name'],
                 user['last_name'],
                 user['email'],
                 generate_password_hash(user['password'])
                )
            )
            self.connection.commit()
        except sqlite3.IntegrityError:
            raise ConflictError
        return self.get_user(user['email'])
    
    def get_user(self, email):
        cur = self.connection.execute("""
            SELECT id, first_name, last_name, email
            FROM accounts
            WHERE email = ?
            """,
            (email,)
        )
        return dict(cur.fetchone())
