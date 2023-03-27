import sqlite3

class BASADATA():
    def __init__(self):
        self.connect = sqlite3.connect('baseserver.db')
        self.cursor = self.connect.cursor()

    def create_class_table(self, class_id):
        self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS {class_id}('
        name TEXT,
        id INT PRIMARY KEY,
        status TEXT,
        year BIGINT,
        classteacher TEXT
        )''').connection.commit()