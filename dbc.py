import sqlite3
conn = sqlite3.connect('lapdata.db')
cursor = conn.cursor()
cursor.execute('''
        CREATE TABLE IF NOT EXISTS laptops (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    brand TEXT NOT NULL,
    model TEXT NOT NULL,
    processor TEXT NOT NULL,
    ram INTEGER NOT NULL,
    storage INTEGER NOT NULL,
    price REAL NOT NULL
        )
    ''')

# new_laptops = [
     
    #  ('Samsung', 'Galaxy Book 2', 'Intel i5', 16, 512, 55000.00),
      
# ]
# cursor.executemany('''
# INSERT INTO laptops (brand, model, processor, ram, storage, price) VALUES (?, ?, ?, ?, ?, ?)
#  ''', new_laptops)

# cursor.execute('DELETE FROM laptops WHERE id = ?', (27,))



conn.commit()
conn.close()