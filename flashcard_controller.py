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

    # betölti az összes szettet az adatbázisból, kivéve azt, aminek
    # a last_flagje = 1 (az az, amit legutoljára gyakorolt a felhasználó)
    sets = db.fetch_all_set_stats()

    # kiszedi az összes szettet, amiben nincs kártya
    sets_tmp = sets[:]
    for i in range(len(sets)):
        set_id = sets[i][0]
        card_count = db.get_card_count_in_deck(set_id)
        if card_count <= 0:
            del sets_tmp[i]

    sets = sets_tmp
    print(sets)

    # ebben a szótárban fogja eltárolni a szetteket és a hozzájuk tartozó címkét
    tags = {}

    # a csúszkák értékeiből kiszámolja, hogy az egyes tulajdonságokat milyen súllyal
    # kell figyelembe venni majd ajánláskor
    # az első kettőt négyzetre emeljük, mivel a szett pontosságának értéke várhatóan nagyobb,
    # mint az elmúlt napok és a gyakorlások száma
    date_weight = sliders['Days since review'].get() ** 2
    count_weight = sliders['Least reviewed'].get() ** 2
    accuracy_weight = sliders['Least accurate'].get()

    # kiszámol minden szettre egy címkét, ami a három tulajdonság és hozzá tartozó
    # súly szorzatainak összege
    for s in sets:

        # szett attribútumainak kinyerése a listából
        set_id = s[0]
        last_reviewed = s[1]
        count = s[2]
        accuracy = s[3]

        # utolsó gyakorlás átalakítása python datetime objektummá
        # majd azóta eltelt napok számolása
        # (egyet azért hozzáad, hogy a ma gyakorolt szettek is szóba jöhessenek valamennyire)
        td = datetime.strptime(last_reviewed, '%Y-%m-%d')
        days_since_last = (datetime.now() - td).days + 1

        # adatbázisból megkeressük a legtöbbet gyakorolt szett gyakorlásainak számát
        # ebből kivonjuk a feldolgozás alatt lévő szett számát, hogy
        # a kevesebbet gyakoroltabbak nagyobb számmal rendelkezzenek
        largest_count = db.get_largest_count() + 1
        inverted_count = largest_count - count

        # a helyességi arányt tévedési aránnyá alakítjuk, hogy
        # a pontatlanabb szettek nagyobb számmal rendelkezzenek
        inverted_accuracy = 100 - accuracy

        # címke számolása
        tag = days_since_last * date_weight + \
              inverted_count * count_weight + \
              inverted_accuracy * accuracy_weight

        tags[set_id] = tag

    # megkeresi a legnagyobb címkét
    sets_with_highest_tag = []
    highest_tag = max(tags.values())

    # majd egy listába elment minden szettet, aminek ugyanez a címkéje
    for id_tag in tags.items():
        if id_tag[1] == highest_tag:
            sets_with_highest_tag.append(id_tag[0])

    # véletlenszerűen választ egy szettet az előbb kigyűjtöttek közül
    set = random.choice(sets_with_highest_tag)

    # betölti az összes szót, ami ebbe a szettbe tartozik
    words = db.fetch_flaschards(set)

    # a kódban ezután még a GUI megfelelően frissül, hogy a szett gyakorlását meg
    # lehessen kezdeni

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
    # betölti adatbázisból a szett jelenlegi gyakorlásainak számát és pontossági arányát
    current_stats = db.fetch_set_stats(set_id=set)
    count = current_stats[1]
    accuracy = current_stats[2]

    # kiszámol egy gammát, ami annál kisebb, minél szélsőségesebben teljesített
    # a felhasználó (nagyon sokat rontott, nagyon sokat eltalált)
    # ez a gamma határozza meg, hogy a korábbi pontossági arányt mennyire "jegyzi meg"
    gamma = -3.5 * ((right_answer_count / word_count) - 0.5) ** 2 + 1

    # a frissített pontosság a korábbi pontosságból [eddigi gyakorlások száma] darab
    # gamma súlyú érték
    # és a mostani gyakorlás pontosságának (súlya 1) súlyozott átlaga
    updated_accuracy = ((accuracy * count * gamma) + (right_answer_count * 100 / word_count)) / (count * gamma + 1.0)

    # új értékek felvitele adatbázisba
    # a háttérben nő meg a gyakorlások száma eggyel, és cserélődik le a legutóbbi
    # gyakorlás napja a maira
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
            set_button_state((btn_shuffle,), 'normal')
    else:
        set_button_state((btn_shuffle,), 'disabled')

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