import sqlite3

con = sqlite3.connect('flashcards.db')
cur = con.cursor()

def commit():
    con.commit()

def get_cur():
    return cur

def get_largest_set_id():
    return cur.execute('SELECT MAX(id) FROM sets').fetchone()[0]

def get_largest_count():
    return cur.execute('SELECT MAX(count) FROM sets').fetchone()[0]

def get_set_name(set_id):
    return cur.execute(f'SELECT name FROM sets where id = {set_id}').fetchone()[0]

def fetch_flaschards(set_id):
    res = cur.execute(f'SELECT front, back FROM cards WHERE set_id = {set_id}')
    return res.fetchall()

def fetch_set_stats(set_id):
    res = cur.execute(f'SELECT last_reviewed, count, accuracy FROM sets WHERE id = {set_id}')
    return res.fetchone()

def fetch_all_set_stats():
    res = cur.execute(f'SELECT id, last_reviewed, count, accuracy FROM sets WHERE last_flag=0')
    return res.fetchall()

def register_review_stats(set_id, accuracy):
    cur.execute(f'UPDATE sets SET last_flag=0 WHERE last_flag=1')
    cur.execute(f'UPDATE sets SET last_reviewed=DATE(\'now\'), count=count+1, accuracy={accuracy}, last_flag=1 WHERE id={set_id}')
    con.commit()

def flush_last_flags():
    cur.execute(f'UPDATE sets SET last_flag=0')
    con.commit()