from flask import Flask, render_template, request, redirect, url_for, session, g
from flask_bcrypt import Bcrypt
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key
bcrypt = Bcrypt(app)
DATABASE = 'voting.db'

# Database setup
def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT UNIQUE NOT NULL,
                            password TEXT NOT NULL
                        )''')
        conn.execute('''CREATE TABLE IF NOT EXISTS votes (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            candidate TEXT NOT NULL
                        )''')
        conn.commit()

# Initialize the database
init_db()

# Database connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        adhaarnumber = request.form['adhaarnumber']

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        with sqlite3.connect(DATABASE) as conn:  # Use DATABASE constant here
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO users (username, password,adhaarnumber) VALUES (?, ?, ?,)", (username, hashed_password,adhaarnumber))
                conn.commit()
                return redirect(url_for('login'))
            except sqlite3.IntegrityError:
                return "Username already exists!"

    return render_template('signup.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        adhaarnumber = request.form['adhaarnumber']
        db = get_db()
        cursor = db.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        
        if user and bcrypt.check_password_hash(user[2], password,adhaarnumber):  # Compare hashed password
            session['username'] = username  # Store username in session
            return redirect(url_for('vote'))
        else:
            return "Invalid credentials. Please try again."
    return render_template('login.html')

# Vote route
@app.route('/vote', methods=['GET', 'POST'])
def vote():
    if request.method == 'POST':
        candidate = request.form['candidate']
        db = get_db()
        db.execute('INSERT INTO votes (candidate) VALUES (?)', (candidate,))
        db.commit()
        return redirect(url_for('results'))
    return render_template('vote.html')

# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove username from session
    return redirect(url_for('login'))  # Redirect to login page

# Results route
@app.route('/results')
def results():
    db = get_db()
    cursor = db.execute('SELECT candidate, COUNT(*) as count FROM votes GROUP BY candidate')
    results = cursor.fetchall()
    return render_template('results.html', results=results)

# Debug route to check tables
@app.route('/debug')
def debug():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
    return f"Tables in database: {tables}"

if __name__ == '__main__':
    app.run(debug=True)
