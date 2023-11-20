import sqlite3


# CREATE USER
def create_user():
    
    conn = sqlite3.connect("test.db")
    c = conn.cursor()
    
    c.execute('''CREATE TABLE login(
            id integer primary key,
            password text default null,
            phrase text default null
            
            )''')

    conn.commit()

    conn.close



# CREATE TABLE
def create_table():
    
    conn = sqlite3.connect("test.db")
    c = conn.cursor()
    
    c.execute('''CREATE TABLE password(
            id integer primary key,
            title text default null,
            user_name text default null,
            password text default null,
            notes text default null,
            last_modified text default null
            )''')

    conn.commit()

    conn.close
  
# INSERT USER
def insert_user(password, phrase):
        
    conn = sqlite3.connect("test.db")
    c = conn.cursor()
    
    command = "INSERT INTO login (password,phrase) VALUES (?,?)"
    c.execute(command, (password,phrase))
    
    conn.commit()

    conn.close
  
  
# INSERT RECORD
def insert_data(title, uname, password, notes, last_modified):
        
    conn = sqlite3.connect("test.db")
    c = conn.cursor()
    
    command = "INSERT INTO password (title, user_name, password,notes, last_modified) VALUES (?, ?, ?, ?, ?)"
    c.execute(command, (title, uname, password,notes, last_modified))
    
    conn.commit()

    conn.close
    
# DELETE RECORD
def delete_record(id_value):
        
    conn = sqlite3.connect("test.db")
    c = conn.cursor()
    
    delete_query = f"DELETE FROM password WHERE id = ?"
    c.execute(delete_query, (id_value,))
    
    conn.commit()

    conn.close

# UPDATE RECORD
def update_record(id ,title, user_name, password,notes, last_modified):
    
    conn = sqlite3.connect("test.db")
    c = conn.cursor()
    
    update_query = f"UPDATE password SET title = ? WHERE id = ?"    
    c.execute(update_query, (title, id))
    
    update_query = f"UPDATE password SET user_name = ? WHERE id = ?"    
    c.execute(update_query, (user_name, id))    
    
    update_query = f"UPDATE password SET password = ? WHERE id = ?"    
    c.execute(update_query, (password, id))

    update_query = f"UPDATE password SET notes = ? WHERE id = ?"    
    c.execute(update_query, (notes, id))
    
    update_query = f"UPDATE password SET last_modified = ? WHERE id = ?"    
    c.execute(update_query, (last_modified , id))

    conn.commit()

    conn.close
    
# RETRIEVE SPECIFIC RECORD
def retrieve_record_by_attribute(id_value):
        
    conn = sqlite3.connect("test.db")
    c = conn.cursor()
    
    query = "SELECT * FROM password WHERE year = ?"
    c.execute(query, (id_value,))
    records = c.fetchall()

    conn.close

    return records

#RETRIEVE USER DATA
def retrieve_user():
        
    conn = sqlite3.connect("test.db")
    c = conn.cursor()
    
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='login'")
    table_exists = c.fetchone() is not None
    if table_exists:
        c.execute("SELECT * FROM login")
        data = c.fetchall()

        conn.close
    
        return(data)
    else:
        
        conn.close
        
        return None


# RETRIEVE ALL DATA
def retrieve():
        
    conn = sqlite3.connect("test.db")
    c = conn.cursor()
    
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='password'")
    table_exists = c.fetchone() is not None
    if table_exists:
        c.execute("SELECT * FROM password")
        data = c.fetchall()

        conn.close
    
        return(data)
    else:
        
        conn.close
        
        return None
        

# USER COUNT
def user_count():
        
    conn = sqlite3.connect("test.db")
    c = conn.cursor()
    
    c.execute("SELECT * FROM login")
    data = c.fetchall()
    varlen=int(len(data))
    
    conn.commit()

    conn.close
    
    return(varlen)

# UPDATE USER
def update_user(password):
    conn = sqlite3.connect("test.db")
    c = conn.cursor()
    
    id=1
    
    update_query = f"UPDATE LOGIN SET password = ? WHERE id = ?"    
    c.execute(update_query, (password, id))
   
    

    conn.commit()

    conn.close

# GET RECORD COUNT
def record_count():
        
    conn = sqlite3.connect("test.db")
    c = conn.cursor()
    
    c.execute("SELECT * FROM password")
    data = c.fetchall()
    varlen=int(len(data))
    
    conn.commit()

    conn.close
    
    return(varlen)


# CLEAR USER
def clear_user():
    
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()

    try:
        cursor.execute('DELETE FROM login')
        
        conn.commit()
        
        print('Records cleared successfully.')
    except Exception as e:
        
        print(f'Error: {str(e)}')
    finally:
        
        conn.close()




def delete_all():
    
    conn = sqlite3.connect("test.db")
    c = conn.cursor()
    
    c.execute('DROP TABLE IF EXISTS password')
    clear_user()
    
    conn.commit()

    conn.close



    
# delete_all()
# record_count()
# print(*retrieve())
# clear_user()
# print(retrieve_user())
# create_user()
# destroy()
