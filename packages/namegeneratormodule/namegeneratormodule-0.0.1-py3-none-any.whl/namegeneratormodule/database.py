import sqlite3
from random import choice 

def get_first_name():
    ''' Get a random first name from the database '''
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor() 

    val = cursor.execute("SELECT * FROM first_name").fetchall()
    data = val.copy()

    conn.close()

    return choice(data)[1]

def get_last_name():
    ''' Get a random last name from database '''

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor() 

    val = cursor.execute("SELECT * FROM last_name").fetchall()
    data = val.copy()

    conn.close()

    return choice(data)[1]