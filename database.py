import sqlite3

conn = sqlite3.connect('zeddata.db')
cur = conn.cursor()
cur.execute("""SELECT * FROM facts""")
for row in cur.fetchall():
    print(row)