import sqlite3

class Database:

    def __init__(self, db_file='zedchat.db'):
        self.filename = db_file
        Users_table_query = 'CREATE TABLE IF NOT EXISTS "Users" ("Id" INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, "Name"	TEXT, "Bio"	TEXT, "Email"	TEXT, "password"	TEXT);'
        
        Posts_table_query = 'CREATE TABLE IF NOT EXISTS "Posts" ("Id"	 INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, "UserId"	INTEGER, "Text"	TEXT, "DateTime"	TEXT);'

        Likes_table_query = 'CREATE TABLE IF NOT EXISTS "Likes" ("UserId" INTEGER PRIMARY KEY, "PostId"	INTEGER);'
        
        Counts_table_query = 'CREATE TABLE IF NOT EXISTS "Counts" ("Id"	TEXT, "Likescount"	TEXT);'

        self.execute_void_query(Users_table_query)
        self.execute_void_query(Posts_table_query)
        self.execute_void_query(Likes_table_query)
        self.execute_void_query(Counts_table_query)


    def execute_void_query(self, query_text, *parameters):
        conn = sqlite3.connect(self.filename)
        cur = conn.cursor()
        cur.execute(query_text, parameters)
        conn.commit()

    def execute_return_query(self, query_text,  *parameters, headers=True):
        conn = sqlite3.connect(self.filename)
        cur = conn.cursor()
        cur.execute(query_text, parameters)

        column_names = []
        for column in cur.description:
            column_names.append(column[0])

        rows = cur.fetchall()
        if (headers):
            dicts = []
            for row in rows:
                d = dict(zip(column_names, row))
                dicts.append(d)
            conn.close()
            return dicts
        else:
            return rows

    
    def get_user_data(self, name, password):
        query = "SELECT * FROM Users WHERE Name=? AND password=?"
        return self.execute_return_query(query, name, password)

    
    def insert_new_user(self, name, email, password):
        query = "INSERT INTO Users(Name,Email,password) VALUES (?,?,?)"
        return self.execute_return_query(query, name, email, password)