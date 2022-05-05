import sqlite3

class Database:

    def __init__(self, db_file='zedchat.db'):
        self.filename = db_file
        Users_table_query = 'CREATE TABLE IF NOT EXISTS "Users" ("Id" INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, "Name"	TEXT, "Bio"	TEXT, "Email" TEXT UNIQUE, "password" TEXT);'
        
        Posts_table_query = 'CREATE TABLE IF NOT EXISTS "Posts" ("Id" INTEGER PRIMARY KEY AUTOINCREMENT, "UserId"	INTEGER, "Text"	TEXT, "DateTime"	TIMESTAMP DEFAULT CURRENT_TIMESTAMP);'

        Likes_table_query = 'CREATE TABLE IF NOT EXISTS "Likes" ("UserId" INTEGER PRIMARY KEY, "PostId"	INTEGER);'
        
        Counts_table_query = 'CREATE TABLE IF NOT EXISTS "Counts" ("Id"	TEXT, "Likescount"	TEXT);'

        messages_table_query = 'CREATE TABLE IF NOT EXISTS "Messages" ("Id" INTEGER PRIMARY KEY AUTOINCREMENT, "UserId"	INTEGER, "Text"	TEXT, "DateTime" TIMESTAMP DEFAULT CURRENT_TIMESTAMP);'

        self.execute_void_query(Users_table_query)
        self.execute_void_query(Posts_table_query)
        self.execute_void_query(Likes_table_query)
        self.execute_void_query(Counts_table_query)
        self.execute_void_query(messages_table_query)


    def execute_void_query(self, query_text, *parameters):
        conn = sqlite3.connect(self.filename)
        cur = conn.cursor()
        cur.execute(query_text, parameters)
        conn.commit()

    def execute_return_query(self, query_text, *parameters):
      conn = sqlite3.connect(self.filename)
      cur = conn.cursor()
      cur.execute(query_text, parameters)

      column_names = []
      for column in cur.description:
       column_names.append(column[0])

      rows = cur.fetchall()
      dicts = []
      for row in rows:
        d = dict(zip(column_names, row))
        dicts.append(d)
        conn.close()
      return dicts

    
    def get_user_data(self, user):
        return self.execute_return_query("SELECT * FROM Users WHERE Name=?", user)

    def get_user_by_Id(self,Id):
      return self.execute_return_query("SELECT * FROM Users WHERE Id = ?",Id)

    def get_id_by_name(self, user):
      return self.execute_return_query("SELECT * FROM Users WHERE Name = ?", user)

    
    def insert_new_user(self, Name, Email, password):
        query = "INSERT INTO Users(Name,Email,password) VALUES (?,?,?)"
        self.execute_void_query(query, Name, Email, password)

    def insert_post(self, id, post_content):
        self.execute_void_query("INSERT INTO Posts (Text,UserId) VALUES (?,?)", post_content, id)


    def get_all_posts(self,user):
        return self.execute_return_query("SELECT * FROM Posts Inner JOIN Users ON Posts.UserId = Users.Id WHERE Users.Id = ?;", user)
        


    def get_all_posts_by_id(self, user):
        self.execute_return_query("""SELECT Posts.Id, Posts.UserId, Posts.Text, Users.Name, Users.Picture, L.LikeCount FROM Posts INNER JOIN Users ON Posts.UserId = Users.Id INNER JOIN (SELECT PostId, COUNT(UserId) AS LikeCount FROM Likes GROUP BY UserId)L ON Posts.Id = L.PostId WHERE Users.Id = ?""", user)

    

    def insert_comment(self, id, comment_content):
        self.execute_void_query("INSERT INTO Comments (Comment, Id) VALUES (?, ?)", comment_content, id)
        pass
    

    def  get_all_comments(self,post_id):
       conn = sqlite3.connect('zedchat.db')
       cur = conn.cursor()
       self.execute_return_query("""SELECT * FROM Comments WHERE PostId = ?""",post_id)
       columns = [column[0] for column in cur.description]
       results = []
       for row in cur:
            d = dict(zip(columns,row))
            results.append(d)
       return results



    def reset_database_password(self,username,password):
        self.execute_void_query("""UPDATE Users SET password=? WHERE Name =?""",password, username)
        


    def insert_message(self, id, post_content):
        self.execute_void_query("INSERT INTO Messages (Text, Id) VALUES (?, ?)", post_content, id)


    def get_all_messages(self,user ):
        return self.execute_return_query("SELECT * FROM Messages Inner JOIN Users ON Posts.Id = Users.Id WHERE Users.Id = ?;", user)