from database.db import db_connection


# MAIN USER CLASS
# IT Staff and Admin will inherit from this class

class User:
    def __init__(self, id, name, username, password, role,):
        self.id = id
        self.name = name
        self.username = username
        self.password = password
        self.role = role 

    def save_user(self):
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, username, password, role) VALUES (?, ?, ?, ?)",
            (self.name, self.username, self.password, self.role),
        )
        conn.commit()
        conn.close() # this saves the user to the database.
        
    @staticmethod
    def get_user(username):
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return User(id=row[0], name=row[1], username=row[2], password=row[3], role=row[4])
        return None
    
    @staticmethod
    def get_id(id):
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return User(id=row[0], name=row[1], username=row[2], password=row[3], role=row[4])
        return None
    
    @staticmethod
    def update_password(username, new_password):
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET password = ? WHERE username = ?", (new_password, username))
        conn.commit()
        conn.close()

        
    


