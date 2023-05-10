import random
import db
from datetime import datetime, date, timedelta

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
    # print(word_sequence)
    current_card_number = 1
    return word_sequence.pop(0)

def load_new_set(btns, lbl_card, lbl_page, lbl_max_page, lbl_set_name, sliders):
    global set, words, word_count, word_idx, answer_revealed, right_answer_count

    sets = db.fetch_all_set_stats()
    print(sets)
    tags = {}

    # calculate tag for all sets
    for s in sets:
        set_id = s[0]
        last_reviewed = s[1]
        count = s[2]
        accuracy = s[3]

        td = datetime.strptime(last_reviewed, '%Y-%m-%d')
        days_since_last = (datetime.now() - td).days

        date_weight = sliders['Last reviewed'].get() ** 3

        largest_count = db.get_largest_count()
        inverted_count = largest_count - count
        count_weight = sliders['Least reviewed'].get() ** 3

        inverted_accuracy = 100 - accuracy
        accuracy_weight = sliders['Least accurate'].get()

        tag = days_since_last * date_weight + \
              inverted_count * count_weight + \
              inverted_accuracy * accuracy_weight

        tags[set_id] = tag

    # get all sets with highest tag
    sets_with_highest_tag = []
    highest_tag = max(tags.values())
    for id_tag in tags.items():
        if id_tag[1] == highest_tag:
            sets_with_highest_tag.append(id_tag[0])

    print('Tags:', tags)
    print('Highest ranking sets:', sets_with_highest_tag)

    # randomly pick a set from the sets_with_highest_tag
    set = random.choice(sets_with_highest_tag)
    print('Set:', set)
    words = db.fetch_flaschards(set)

    word_count = len(words)
    right_answer_count = 0
    word_idx = init_card_sequence()

    answer_revealed = False

    lbl_page.config(text='1')
    update_card_label(lbl_card, lbl_page, lbl_max_page)
    lbl_set_name.config(text=db.get_set_name(set))

    set_button_state(btns, 'normal')
    show_hide_buttons(btns[0], btns[1], btns[2])

    print('Loaded set')
    print(words)

def register_review_stats():
    current_stats = db.fetch_set_stats(set_id=set)
    count = current_stats[1]
    accuracy = current_stats[2]

    gamma = 1 - 0.7 * (right_answer_count / word_count)
    print('gamma = ', gamma)
    print('accuracy * count * gamma', accuracy * count * gamma)
    updated_accuracy = ((accuracy * count * gamma) + (right_answer_count * 100 / word_count)) / (count * gamma + 1.0)

    print('set:', set, 'reviewed for the', count+1, 'th time, with an accuracy of', accuracy)
    print('average accuracy:', updated_accuracy)

    db.register_review_stats(set, updated_accuracy)

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

            register_review_stats()

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

#load_new_set()