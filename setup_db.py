import sqlite3

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('voting.db')
cursor = conn.cursor()

# Create the votes table if it doesn't already exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS votes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        candidate TEXT NOT NULL
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
''')

conn.commit()
conn.close()
print("Database setup complete. 'votes' and 'users' tables created if they didn't exist.")
