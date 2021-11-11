import sqlite3

con = sqlite3.connect('main.db')
cursor = con.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (name text, id int NOT NULL PRIMARY KEY, password text)")

def put(id, name = 'undefined', password = '101'):
    cursor.execute('INSERT INTO users(name, id, password) VALUES(?, ?, ?)', (name, id, password)) 
    con.commit()

#region debug

def print_all():
    cursor.execute('SELECT * FROM users')
    print(cursor.fetchone())

def cmd(commmand):
    cursor.execute(commmand)
    print(cursor.fetchone())

#endregion