import sqlite3
import telegram


class DatabaseWorker:

    def __init__(self):
        self.conn = sqlite3.connect('jeeves.db')
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS users"
                         "(id TEXT, first_name TEXT, last_name TEXT, username TEXT, is_friend TEXT)")

    def add_user(self, user: telegram.User):
        self.cur.execute("SELECT * FROM users WHERE id = ?", (user.id, ))
        if self.cur.rowcount > 0:
            pass  # The user is already in the database
        else:
            self.cur.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?",
                             (user.id, user.first_name, user.last_name, user.username, "False"))


