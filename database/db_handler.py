import sqlite3


class Database:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS jobs
                               (id INTEGER PRIMARY KEY AUTOINCREMENT,
                               title TEXT,
                               company TEXT,
                               location TEXT,
                               description TEXT)''')
        self.conn.commit()

    def insert_job(self, title, company, location, description):
        self.cursor.execute("INSERT INTO jobs (title, company, location, description) VALUES (?, ?, ?, ?)",
                            (title, company, location, description))
        self.conn.commit()

    def close_connection(self):
        self.cursor.close()
        self.conn.close()
