import random
import db

BTN_REVEAL_TXT = ('Show', 'Next')

def show_hide_buttons(btn_show, btn_right, btn_wrong):
    if not answer_revealed:
        btn_show.grid(column=0, row=0, pady=(10, 5))
        btn_right.grid_forget()
        btn_wrong.grid_forget()
    else:
        btn_show.grid_forget()
        btn_right.grid(column=0, row=0, padx=5, pady=(10, 5))
        btn_wrong.grid(column=1, row=0, padx=5, pady=(10, 5))

def set_button_state(btns, state):
    for btn in btns:
        btn.config(state=state)

def update_slider(val, lbl):
    lbl.config(text='%0.2f' % float(val))

def init_card_sequence():
    global word_sequence, current_card_number
    word_sequence = [i for i in range(word_count)]
    print(word_sequence)
    current_card_number = 1
    return word_sequence.pop(0)

def load_new_set(btns=None, lbl_card=None, lbl_page=None, lbl_max_page=None):
    global words, word_count, word_idx, answer_revealed, right_answer_count

    success = False
    while not success:
        try:
            set = random.randrange(1, db.get_largest_set_id() + 1)
            print('Set:', set)
            words = db.fetch_flaschards(set)

            word_count = len(words)
            right_answer_count = 0
            word_idx = init_card_sequence()

            answer_revealed = False

            if lbl_page:
                lbl_page.config(text='1')
            if lbl_card and lbl_page and lbl_max_page:
                update_card_label(lbl_card, lbl_page, lbl_max_page)

            success = True

            if btns:
                set_button_state(btns, 'normal')
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

def load_next_card(btn_show, btn_right, btn_wrong, btn_shuffle, lbl_card, lbl_page, inc_score=False):
    global word_idx,current_card_number, answer_revealed,word_sequence, right_answer_count

    print('ANSWER:', answer_revealed)

    if inc_score:
        right_answer_count += 1
        print(right_answer_count)

    if answer_revealed:
        if len(word_sequence) == 0: # elfogytak a szavak

            lbl_card.config(text=f"All cards reviewed.\nYou got {right_answer_count} right,\nand {word_count-right_answer_count} wrong.\n\nStats recorded.")
            set_button_state((btn_show, btn_right, btn_wrong, btn_shuffle), 'disabled')

            return
        else:
            current_card_number += 1
            word_idx = word_sequence.pop(0)

    answer_revealed = not answer_revealed

    show_hide_buttons(btn_show, btn_right, btn_wrong)

    update_card_label(lbl_card, lbl_page)

def shuffle_set(btn_show, btn_right, btn_wrong, lbl_card, lbl_page):
    global word_sequence, word_idx, answer_revealed, current_card_number

    if answer_revealed:
        # ha már fel lett fedve a kihúzott kártya, tovább is lép egyszerre
        current_card_number += 1
        answer_revealed = False
    else:
        # ha még nem lett felfedve a válasz, visszarakja a kártyák közé
        word_sequence.append(word_idx)

    show_hide_buttons(btn_show, btn_right, btn_wrong)

    random.shuffle(word_sequence)
    word_idx = word_sequence.pop(0)
    update_card_label(lbl_card, lbl_page)

words = []
word_idx = 0
word_count = 0

load_new_set()