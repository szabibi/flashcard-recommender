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

def get_set_id(set_name):
    return cur.execute(f'SELECT id FROM sets where name = {set_name}').fetchone()[0]

def fetch_all_sets():
    res = cur.execute('SELECT id, name FROM sets').fetchall()
    #return [i[0] for i in res]
    return res

def fetch_flaschards(set_id):
    res = cur.execute(f'SELECT front, back, hint FROM cards WHERE set_id = {set_id}')
    return res.fetchall()

def fetch_flashcards_with_id(set_id):
    return cur.execute(f'SELECT id, front, back, hint FROM cards WHERE set_id = {set_id}').fetchall()

def fetch_set_stats(set_id):
    res = cur.execute(f'SELECT last_reviewed, count, accuracy FROM sets WHERE id = {set_id}')
    return res.fetchone()

def fetch_all_set_stats():
    res = cur.execute(f'SELECT id, last_reviewed, count, accuracy FROM sets WHERE last_flag=0 AND include=1')
    return res.fetchall()

def get_deck_size(set_id):
    return cur.execute(f'SELECT COUNT(*) FROM cards WHERE set_id = {set_id}').fetchone()[0]

def register_review_stats(set_id, accuracy):
    cur.execute(f'UPDATE sets SET last_flag=0 WHERE last_flag=1')
    cur.execute(f'UPDATE sets SET last_reviewed=DATE(\'now\'), count=count+1, accuracy={accuracy}, last_flag=1 WHERE id={set_id}')
    con.commit()

def flush_last_flags():
    cur.execute(f'UPDATE sets SET last_flag=0')
    con.commit()

def update_card(card_id, front, back, hint, commit=False):
    cur.execute(f'UPDATE cards SET front=?, back=?, hint=? WHERE id=?', (front, back, hint, card_id))
    if commit:
        con.commit()

def delete_card(card_id, commit=False):
    cur.execute(f'DELETE FROM cards WHERE id={card_id}')
    cur.execute(f'UPDATE sqlite_sequence SET seq = (SELECT MAX(id) FROM cards) WHERE name="cards"')
    if commit:
        con.commit()

def add_card(set_id, front, back, hint, commit=False):
    cur.execute(f'INSERT INTO cards (set_id, front, back, hint)VALUES (?, ?, ?, ?)', (set_id, front, back, hint))
    if commit:
        con.commit()

def rename_deck(set_id, new_name):
    cur.execute(f'UPDATE sets SET name=? WHERE id=?', (new_name, set_id))
    con.commit()

def delete_deck(set_id):
    cur.execute(f'DELETE FROM sets WHERE id={set_id}')
    cur.execute(f'DELETE FROM cards WHERE set_id={set_id}')
    cur.execute(f'UPDATE sqlite_sequence SET seq = (SELECT MAX(id) FROM sets) WHERE name="sets"')
    cur.execute(f'UPDATE sqlite_sequence SET seq = (SELECT MAX(id) FROM cards) WHERE name="cards"')
    con.commit()

def deck_name_exists(name):
    res = cur.execute(f'SELECT name FROM sets WHERE name = ?', (name,)).fetchall()
    if len(res) > 0:
        return True
    else:
        return False

def add_deck(name):
    cur.execute(f'INSERT INTO sets(name) VALUES (?)', (name,))
    con.commit()

def get_card_count_in_deck(set_id):
    return cur.execute(f'SELECT COUNT(*) FROM cards WHERE set_id={set_id}').fetchone()[0]

def clear_stats(deck_id):
    cur.execute(f'UPDATE sets SET last_reviewed=DATE(\'now\'), count=0, accuracy=0 WHERE id = ?', (deck_id,))
    con.commit()

def toggle_inclusion(deck_id):
    cur.execute(f'UPDATE sets SET include=CASE WHEN include=1 THEN 0 ELSE 1 END WHERE id = ?', (deck_id,))
    con.commit()

def get_deck_inclusion(deck_id):
    return cur.execute(f'SELECT include FROM sets WHERE id = {deck_id}').fetchone()[0]