import random
import db

BTN_REVEAL_TXT = ('Show', 'Next')

def init_card_sequence():
    global word_sequence, current_card_number
    word_sequence = [i for i in range(word_count)]
    print(word_sequence)
    current_card_number = 1
    return word_sequence.pop(0)

def load_new_set(lbl_card=None, lbl_page=None, lbl_max_page=None):
    global words, word_count, word_idx, answer_revealed
    success = False
    while not success:
        try:
            set = random.randrange(1, db.get_largest_set_id() + 1)
            print('Set:', set)
            words = db.fetch_flaschards(set)

            word_count = len(words)
            word_idx = init_card_sequence()

            if lbl_page:
                lbl_page.config(text='1')
            if lbl_card and lbl_page and lbl_max_page:
                update_card_label(lbl_card, lbl_page, lbl_max_page)

            answer_revealed = False
            success = True
        except IndexError:
            pass

    print('Loaded set')
    print(words)

def get_next_word():
    global word_sequence, current_card_number

    # elfogytak a szavak
    if len(word_sequence) == 0:
        idx = init_card_sequence()
        return idx
    else:
        current_card_number += 1
        return word_sequence.pop(0)

def update_card_label(lbl_card, lbl_page, lbl_max_page=None):
    if not answer_revealed:
        lbl_card.config(text= words[word_idx][0])
        lbl_page.config(text= f'{current_card_number}')
    else:
        lbl_card.config(text= words[word_idx][1])

    if lbl_max_page:
        lbl_max_page.config(text=f'/ {word_count}')

def load_next_card(btn, lbl_card, lbl_page):
    global word_idx
    global current_card_number
    global answer_revealed
    global word_sequence

    if answer_revealed:
        word_idx = get_next_word()
        btn_txt = BTN_REVEAL_TXT[0]
    else:
        btn_txt = BTN_REVEAL_TXT[1]

    btn.config(text=btn_txt)
    answer_revealed = not answer_revealed

    update_card_label(lbl_card, lbl_page)

def shuffle_set(btn, lbl_card, lbl_page):
    global word_sequence, word_idx, answer_revealed, current_card_number
    if answer_revealed:
        # ha már fel lett fedve a kihúzott kártya, tovább is lép egyszerre
        current_card_number += 1
        answer_revealed = False
    else:
        # ha még nem lett felfedve a válasz, visszarakja a kártyák közé
        word_sequence.append(word_idx)

    random.shuffle(word_sequence)
    word_idx = word_sequence.pop(0)
    update_card_label(lbl_card, lbl_page)

words = []
word_idx = 0
word_count = 0

load_new_set()