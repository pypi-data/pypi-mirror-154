import sqlite3

def insert_first_names_db(name, nationality):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO first_name (first_name, nationality) VALUES (?,?)", [name, nationality])

    conn.commit()
    conn.close()


    return True

def insert_last_names_db(name, nationality):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("INSERT INTO last_name (last_name, nationality) VALUES (?,?)", [name, nationality])

    conn.commit()
    conn.close()


    return True


if __name__ == "__main__":

    with open('last_name_g.txt', 'r') as file:
        
        nat = input("type nationality:. ")
    
        file = file.readlines()
        for line in file:
            name = line.split(' ')[0].replace('\n', '')
            insert_last_names_db(name, nat)