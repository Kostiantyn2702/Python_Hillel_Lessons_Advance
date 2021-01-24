import sqlite3

try:
    connection = sqlite3.connect('./db.sqlite3')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users
    (id INTEGER NOT NULL PRIMARY KEY, first_name VARCHAR(50), last_name VARCHAR(50), is_student BOOLEAN);
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS phones
    (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, value VARCHAR(50), 
    user_id INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(id));
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS emails
    (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, value VARCHAR(50), 
    user_id INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(id));
    ''')

    connection.commit()
finally:
    connection.close()