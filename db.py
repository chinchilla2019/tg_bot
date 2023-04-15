import sqlite3


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.db = db_file
        self.cursor = self.connection.cursor()

    def add_user(self, client_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO Users ('client_id') VALUES (?)", (client_id,))

    def user_exists(self, client_id):
        with self.connection:
            res = self.cursor.execute("""SELECT * FROM Users WHERE client_id=?""", (client_id,)).fetchall()
            return bool(len(res))

    def set_user_name(self, client_id, user_name):
        with self.connection:
            return self.cursor.execute("""UPDATE Users SET user_name=? WHERE client_id=?""",
                                       (user_name, client_id))

    def get_signup(self, client_id):
        with self.connection:
            res = self.cursor.execute("""SELECT * FROM Users WHERE client_id=?""", (client_id,)).fetchall()[0]
            for row in res:
                signup = str(row)
            return signup

    def get_user_name(self, client_id):
        with self.connection:
            res = self.cursor.execute("""SELECT * FROM Users WHERE client_id=?""", (client_id,)).fetchall()[0]
            return res[2]

    def set_signup(self, client_id, signup):
        with self.connection:
            return self.cursor.execute("""UPDATE Users SET signup=? WHERE client_id=?""",
                                       (signup, client_id))
