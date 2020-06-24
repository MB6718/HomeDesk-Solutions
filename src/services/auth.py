class AuthService:
    def __init__(self, connection):
        self.connection = connection
 
    def login_user(self, email):
        cur = self.connection.cursor()
        cur.execute(
            'SELECT * '
            'FROM accounts '
            'WHERE email = ?',
            (email,),
        )
        user = cur.fetchone()
        return user
