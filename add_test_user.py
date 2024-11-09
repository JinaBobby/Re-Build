import sqlite3

# Connect to the database
conn = sqlite3.connect('voting.db')
cursor = conn.cursor()

# Insert a test user into the 'users' table
# You can change 'testuser' and 'password123' to any username and password you prefer
cursor.execute('''
    INSERT INTO users (username, password) VALUES (?, ?)
''', ('jina', '123'))

# Save the changes and close the connection
conn.commit()
conn.close()

print("Test user added to the 'users' table.")
