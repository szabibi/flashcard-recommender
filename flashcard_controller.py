import random

BTN_REVEAL_TXT = ('Show', 'Next')

def init_card_sequence():
    global word_sequence, current_card_number
    word_sequence = [i for i in range(word_count)]
    current_card_number = 1
    return word_sequence.pop(0)

def get_next_word():
    global word_sequence, current_card_number

    # elfogytak a szavak
    if len(word_sequence) == 0:
        idx = init_card_sequence()
        return idx
    else:
        current_card_number += 1
        return word_sequence.pop(0)

def update_card_label(lbl_card, lbl_page):
    if not answer_revealed:
        lbl_card.config(text= words[word_idx][0])
        lbl_page.config(text= f'{current_card_number}')
    else:
        lbl_card.config(text= words[word_idx][1])

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

words = (('ร้อย', 'hundred'),
         ('พุม', 'thousand'),
         ('หมั่น', 'ten thousand'),
         ('หนัก', 'heavy'),
         ('เบา', 'light'),
         ('แมว', 'cat')
         )
word_count = len(words)

word_idx = init_card_sequence()

answer_revealed = False