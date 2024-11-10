from flask import Flask, render_template, request, redirect, url_for, session, g
from flask_bcrypt import Bcrypt
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key
bcrypt = Bcrypt(app)
DATABASE = 'voting.db'

# Database setup function
def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        # Create users table
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT UNIQUE NOT NULL,
                            password TEXT NOT NULL,
                            adhaarnumber TEXT UNIQUE NOT NULL
                        )''')
        # Create votes table
        cursor.execute('''CREATE TABLE IF NOT EXISTS votes (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            adhaarnumber TEXT NOT NULL,
                            candidate TEXT NOT NULL
                        )''')
        conn.commit()

# Initialize the database
init_db()

# Database connection function
def get_db():
    if '_database' not in g:
        g._database = sqlite3.connect(DATABASE)
        g._database.row_factory = sqlite3.Row
    return g._database

@app.teardown_appcontext
def close_connection(exception):
    db = g.pop('_database', None)
    if db is not None:
        db.close()

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        adhaarnumber = request.form['Adhaarnumber']

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        db = get_db()
        try:
            db.execute("INSERT INTO users (username, password, Adhaarnumber) VALUES (?, ?, ?)",
                       (username, hashed_password, adhaarnumber))
            db.commit()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            return "Username or Aadhaar number already exists!"

    return render_template('signup.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        
        if user and bcrypt.check_password_hash(user['password'], password):
            session['username'] = username
            session['adhaarnumber'] = user['adhaarnumber']  # Store Aadhaar number in session
            return redirect(url_for('vote'))
        else:
            return "Invalid credentials. Please try again."
    
    return render_template('login.html')


# Vote route
@app.route('/vote', methods=['GET', 'POST'])
def vote():
    if request.method == 'POST':
        candidate = request.form['candidate']
        adhaarnumber = session.get('Adhaarnumber')  # Get Aadhaar number from session

        db = get_db()
        db.execute('INSERT INTO votes (adhaarnumber, candidate) VALUES (?, ?)', (adhaarnumber, candidate))
        db.commit()

        # Redirect to the thank-you page after voting
        return redirect(url_for('thank_you'))
    
    return render_template('vote.html')


# Thank You page route
@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')

# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove username from session
    return redirect(url_for('login'))  # Redirect to login page

# Debug route to check tables
@app.route('/debug')
def debug():
    db = get_db()
    cursor = db.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    return f"Tables in database: {tables}"

if __name__ == '__main__':
    app.run(debug=True)
