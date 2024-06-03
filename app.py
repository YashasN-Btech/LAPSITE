from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Function to get a database connection
def get_db_connection(db_name='lapdata.db'):
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    return conn

# Function to initialize the users database and add a test user
def init_users_db():
    conn = get_db_connection('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')
    # Insert a test user if not already present
    try:
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', ('admin', 'password'))
    except sqlite3.IntegrityError:
        print("User already exists.")
    conn.commit()
    conn.close()

# Function to initialize the laptops database
def init_laptops_db():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS laptops (
            id INTEGER PRIMARY KEY,
            brand TEXT NOT NULL,
            ram INTEGER NOT NULL,
            price REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('login.html', show_popup=session.pop('show_popup', False))

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    conn = get_db_connection('users.db')
    user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
    conn.close()
    
    if user:
        session['username'] = username  # Store username in session
        return redirect(url_for('home'))
    else:
        session['show_popup'] = True  # Set show_popup to True in session
        return redirect(url_for('index'))

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/suggest', methods=['POST'])
def suggest():
    brand = request.form['brand']
    min_ram = int(request.form['min_ram'])
    max_price = float(request.form['max_price'])

    conn = get_db_connection()
    query = """
    SELECT * FROM laptops 
    WHERE brand = ? AND ram >= ? AND price <= ?
    """
    laptops = conn.execute(query, (brand, min_ram, max_price)).fetchall()
    conn.close()

    return render_template('result.html', laptops=laptops)

@app.route('/searchagain')
def searchagain():
    return render_template('index.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)  # Remove username from session
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_users_db()  # Initialize the users database when the app starts
    init_laptops_db()  # Initialize the laptops database when the app starts
    app.run(debug=True)
