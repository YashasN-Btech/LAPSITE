from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('lapdata.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
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

if __name__ == '__main__':
    app.run(debug=True)