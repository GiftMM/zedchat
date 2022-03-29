import sqlite3

conn = sqlite3.connect('factbook.db')
cur = conn.cursor()
cur.execute("""SELECT * FROM facts""")
for row in cur.fetchall():
    print(row)