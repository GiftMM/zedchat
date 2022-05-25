import sqlite3

class Database:

    def __init__(self, db_file='zedchat.db'):
        self.filename = db_file
        Users_table_query = 'CREATE TABLE IF NOT EXISTS "Users" ("Id" INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, "Name"	TEXT, "Bio"	TEXT, "Email" TEXT UNIQUE, "password" TEXT);'
        
        Posts_table_query = 'CREATE TABLE IF NOT EXISTS "Posts" ("Id" INTEGER PRIMARY KEY AUTOINCREMENT, "UserId"	INTEGER, "Text"	TEXT, "DateTime"	TIMESTAMP DEFAULT CURRENT_TIMESTAMP);'

        Likes_table_query = 'CREATE TABLE IF NOT EXISTS "Likes" ("UserId" INTEGER PRIMARY KEY, "PostId"	INTEGER);'
        
        Counts_table_query = 'CREATE TABLE IF NOT EXISTS "Counts" ("Id"	TEXT, "Likescount"	TEXT);'

        messages_table_query = 'CREATE TABLE IF NOT EXISTS "Messages" ("MessageId" INTEGER PRIMARY KEY AUTOINCREMENT, "UserId1"	INTEGER, "UserId2"	INTEGER, "Text"	TEXT, "DateTime" TIMESTAMP DEFAULT CURRENT_TIMESTAMP);'

        friends_table_query = 'CREATE TABLE IF NOT EXISTS "friends" ( "Id"	INTEGER NOT NULL UNIQUE PRIMARY KEY AUTOINCREMENT, "UserId"	INTEGER NOT NULL , "friendId"	INTEGER NOT NULL);'

        friend_request_table_query = 'CREATE TABLE IF NOT EXISTS "Requests" ("Id"	INTEGER NOT NULL UNIQUE PRIMARY KEY AUTOINCREMENT, 	"RequesterId"	INTEGER NOT NULL, 	"ReceiverId"	INTEGER NOT NULL );'


        self.execute_void_query(Users_table_query)
        self.execute_void_query(Posts_table_query)
        self.execute_void_query(Likes_table_query)
        self.execute_void_query(Counts_table_query)
        self.execute_void_query(messages_table_query)
        self.execute_void_query(friends_table_query)
        self.execute_void_query(friend_request_table_query)


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
    
    def get_user(self, user):
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


    def get_all_posts(self):
        return self.execute_return_query("SELECT * FROM Posts Inner JOIN Users ON Posts.UserId = Users.Id;")
        


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
        


    def insert_message(self, id, message_content):
        self.execute_void_query("INSERT INTO Messages (Text, UserId2) VALUES (?, ?)", message_content, id)


    def get_all_messages(self,user ):
        return self.execute_return_query("SELECT * FROM Messages Inner JOIN Users ON  Messages.UserId1 = Users.Id  AND Messages.UserId2 = Users.Id;", user)


    def get_message_Id2(self,user):
        return self.execute_return_query("SELECT * FROM Messages WHERE UserId2 = ?;", user)


    def get_message_UserId1(self,user):
        return self.execute_return_query("SELECT * FROM Messages Inner JOIN Users ON  Messages.UserId1 = Users.Id WHERE UserId1 = ?;", user)


    def search_results(self, search_results):
        return self.execute_return_query("SELECT * FROM Users WHERE Name LIKE ?", "%" + search_results + "%")




    def get_all_users_alphabetically(self):
        return self.execute_return_query("SELECT * FROM Users ORDER BY Name DESC;")

    def edit_post(self, Text, Id, post_content):
        return self.execute_return_query("UPDATE Posts SET Text = ? WHERE Id = ?", Text, Id, post_content)


     #///Friends Methods///


    def insert_request(self, requesterid, receiverid):
        self.execute_void_query("INSERT INTO Requests (RequesterId, ReceiverId) VALUES (?,?)", requesterid, receiverid)
        pass

    def cancel_friend_request(self,requesterid, receiverid):
        return self.execute_return_query("DELETE FROM Requests WHERE RequesterId = ? And ReceiverId = ?", requesterid, receiverid) 

    def get_friend_requests(self, Id):
        self.execute_return_query("SELECT * FROM Requests Inner JOIN Users ON Requests.ReceiverId = Users.Id AND Requests.RequesterId = Users.Id WHERE ReceiverId = ?", Id)

    def insert_friend(self, friendid, userid):
        self.execute_return_query("INSERT INTO Friends (FriendId, UserId) VALUES (?, ?)", friendid, userid)


    def get_friends(self):
        self.execute_return_query("SELECT * FROM Friends Inner JOIN Users ON  Friends.FriendsId = Users.Id AND Friends.UserId = Users.Id WHERE FriendId = ?")

    def unfriend(self, friendid, userid):
        return self.execute_return_query("DELETE FROM Friends WHERE FriendId = ? And UserId = ?", friendid, userid) 