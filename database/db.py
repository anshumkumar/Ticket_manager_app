#this is the database file. 
#It is the first file im working on.


import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))   # file path for the database
db_path = os.path.join(BASE_DIR, 'tickets.db')   #path to the tickets.db database file.

# function definition.
def db_connection():   
    conn = sqlite3.connect(db_path) #connects to the database file.
    conn.row_factory = sqlite3.Row    #
    return conn


# ths file is just for the database connection.