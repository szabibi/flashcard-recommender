import sqlite3

con = sqlite3.connect('flashcards.db')
cur = con.cursor()

def get_db():
    return cur

def get_largest_set_id():
    return cur.execute('SELECT MAX(id) FROM sets').fetchone()[0]

def fetch_flaschards(set_id):
    res = cur.execute(f'SELECT front, back FROM cards WHERE set_id = {set_id}')
    return res.fetchall()