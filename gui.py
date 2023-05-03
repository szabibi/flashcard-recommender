import tkinter as tk
import tkinter.ttk as ttk

from flashcard_controller import *

BTN_REVEAL_TXT = ('Show', 'Next')

FONT_NAME = 'Arial'
FONT_BIG = (FONT_NAME, 16)
FONT_SMALL = (FONT_NAME, 10)

class GUI:
    def __init__(self, parent):
        print('Start of GUI')

        frm_buttons = tk.Frame(width=100, bg='black')
        frm_buttons.grid(column=0, row=0, sticky='nw')

        frm_card = tk.Frame(bg='lime', width=600, height=400)
        frm_card.grid(column=0, row=1, sticky='we')

        lbl_card_txt = tk.Label(text=words[word_idx][0],
                                font=FONT_BIG,
                                bg='white',
                                width=30, height=10,
                                master=frm_card)
        lbl_card_txt.pack()

        frm_card_buttons = tk.Frame(width=300, height=50, master=frm_card)
        frm_card_buttons.pack()

        btn_reveal = ttk.Button(text=BTN_REVEAL_TXT[0],
                                master=frm_card_buttons,
                                command=lambda: load_next_card(btn_reveal, lbl_card_txt, lbl_current_page))

        btn_reveal.pack(side=tk.LEFT, padx=10, pady=10)

        btn_shuffle = ttk.Button(text='Shuffle',
                                 master=frm_card_buttons,
                                 command=lambda: shuffle_set(btn_shuffle, lbl_card_txt, lbl_current_page))

        btn_shuffle.pack(side=tk.RIGHT)

        frm_stats = tk.Frame(bg='chartreuse')

        frm_stats.grid(column=0,
                       row=2,
                       sticky='wn')

        lbl_current_page_txt = tk.Label(text='Card:',
                                        font=FONT_SMALL,
                                        master=frm_stats)

        lbl_current_page = tk.Label(text='1',
                                    font=FONT_SMALL,
                                    master=frm_stats)

        lbl_max_page = tk.Label(text=f'/ {word_count}',
                                font=FONT_SMALL,
                                master=frm_stats)

        lbl_current_page_txt.grid(column=1,
                                  row=0)

        lbl_current_page.grid(column=2,
                              row=0)

        lbl_max_page.grid(column=3,
                          row=0)

        btn_new_set_save = ttk.Button(text='Save & New set', master=frm_buttons)
        btn_new_set_save.pack(side=tk.LEFT, padx=10, pady=10)

        btn_new_set_no_save = ttk.Button(text='New set',
                                         master=frm_buttons,
                                         command=lambda: load_new_set(lbl_card_txt,
                                                                      lbl_current_page,
                                                                      lbl_max_page))
        btn_new_set_no_save.pack(side=tk.RIGHT)

window = tk.Tk()
window.columnconfigure(0, weight=1, minsize=200)
window.rowconfigure([0, 2], weight=1, minsize=50)