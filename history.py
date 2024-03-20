import sqlite3

def connect():
    # Connect
    conn = sqlite3.connect('history.sqlite', check_same_thread=False)
    # Create Table
    conn.execute("CREATE TABLE IF NOT EXISTS messages ( id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT )")
    return conn


# Get History
def get_history():
    conn = connect()
    v = conn.execute("select * from messages order by id desc")
    history = v.fetchall()
    conn.close()
    return history

# Add History
def add_history(text):
    conn = connect()
    cur = conn.execute("insert into messages values(?,?)",(None, text,))
    conn.commit()
    id = cur.lastrowid
    conn.close()

    return id

# Delete History
def delete_history(id):
    conn = connect()
    conn.execute("DELETE FROM messages WHERE `id` = ?",( id,))
    conn.commit()
    conn.close()
