import sqlite3

conn = sqlite3.connect('voting.db')
cursor = conn.cursor()

# Create users table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        adhaarnumber TEXT UNIQUE NOT NULL
    )
''')

# Create votes table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS votes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        adhaarnumber TEXT NOT NULL,
        candidate TEXT NOT NULL
    )
''')

conn.commit()
conn.close()
print("Database setup complete.")
