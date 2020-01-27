import sqlite3

connection = sqlite3.connect('sqlTestDB')
cursor = connection.cursor()

# cursor.execute('CREATE TABLE names (id INTEGER PRIMARY KEY, name TEXT)')
cursor.execute('INSERT INTO names(VALUES(?, ?)', (1, 'Donald'))

# connection.commit()
