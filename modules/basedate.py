import sqlite3

class BASADATA():
    def __init__(self):
        self.connect = sqlite3.connect('baseserver.db')
        self.cursor = self.connect.cursor()
        return print('Connect to basedate version 0.1')

    def create_class_table(self, class_id):
        self.cursor.execute(f'''CREATE TABLE IF NOT EXISTS {class_id}('
        name TEXT,
        id INT PRIMARY KEY,
        status TEXT,
        year BIGINT,
        classteacher TEXT
        )''').connection.commit()

    def create_user_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users (
        name_user TEXT,
        id_user BIGINT,
        status_user TEXT,
        class_user TEXT
        )""").connection.commit()
        return print('Table users - successful')
    
    def create_user(self, name_user, id, status, class_user):
        self.cursor.execute('INSERT INTO users VALUES (?, ?, ?, ?, ?)'.format())
    def find_user_table(self, id):
        return self.cursor.execute(f'SELECT id_user FROM users WHERE id_user = {id}').fetchone()
