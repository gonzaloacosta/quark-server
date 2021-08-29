import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)", 
            ('J-Boss', 'That\'s pretty much it')
            )
cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('Big Boss', 'Another things, butterfly.')
            )
cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('Superb Boss', 'What say the finger to the cave?')
            )
cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('Hammer', 'The elephant that taked notes, remeber! :]')
            )
cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('Culiau', 'Ma mior, ieia! :]')
            )

connection.commit()
connection.close()
