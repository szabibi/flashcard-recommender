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

        frm_buttons = tk.Frame(width=100)
        frm_buttons.grid(column=0, row=0, sticky='nw')

        frm_card = tk.Frame(width=600, height=400, borderwidth=1, relief="solid")
        frm_card.grid(column=0, row=3, sticky='we', padx=20)

        lbl_card_txt = tk.Label(text='',
                                font=FONT_BIG,
                                bg='white',
                                width=30, height=10,
                                master=frm_card)
        lbl_card_txt.pack()

        frm_card_buttons_top = tk.Frame(width=300, height=20)
        frm_card_buttons_top.grid(column=0, row=4)

        frm_card_buttons_bottom = tk.Frame(width=300, height=20)
        frm_card_buttons_bottom.grid(column=0, row=5)

        btn_reveal = ttk.Button(text=BTN_REVEAL_TXT[0],
                                master=frm_card_buttons_top,
                                state='disabled',
                                command=lambda: load_next_card(btn_reveal, btn_mark_right, btn_mark_wrong, btn_shuffle, lbl_card_txt, lbl_current_page))

        btn_reveal.grid(column=0, row=0, pady=(10,  5))

        btn_mark_right = ttk.Button(text='Right',
                                    master=frm_card_buttons_top,
                                    command=lambda: load_next_card(btn_reveal, btn_mark_right, btn_mark_wrong, btn_shuffle, lbl_card_txt, lbl_current_page, inc_score=True))
        btn_mark_wrong = ttk.Button(text='Wrong',
                                    master=frm_card_buttons_top,
                                    command=lambda: load_next_card(btn_reveal, btn_mark_right, btn_mark_wrong, btn_shuffle, lbl_card_txt, lbl_current_page))

        #btn_mark_correct.grid(column=0, row=0, padx=5, pady=(10,  5))
        #btn_mark_wrong.grid(column=1, row=0, padx=5, pady=(10, 5))

        btn_shuffle = ttk.Button(text='Shuffle',
                                 master=frm_card_buttons_bottom,
                                 state='disabled',
                                 command=lambda: shuffle_set(btn_reveal, btn_mark_right, btn_mark_wrong, lbl_card_txt, lbl_current_page))

        btn_shuffle.grid(column=0, row=1, pady=(0,10))

        frm_stats = tk.Frame()

        frm_stats.grid(column=0,
                       row=2,
                       sticky='n',
                       pady=5)

        lbl_set_name=tk.Label(text='Click "New set" to start!',
                              font=FONT_BIG,
                              width=30
                              )
        lbl_set_name.grid(column=0, row=1)

        lbl_current_page_txt = tk.Label(text='Card:',
                                        font=FONT_SMALL,
                                        master=frm_stats)

        lbl_current_page = tk.Label(text='0',
                                    font=FONT_SMALL,
                                    master=frm_stats)

        lbl_max_page = tk.Label(text=f'/ {word_count}',
                                font=FONT_SMALL,
                                master=frm_stats)

        lbl_current_page_txt.grid(column=1,
                                  row=1,
                                  sticky='we')

        lbl_current_page.grid(column=2,
                              row=1)

        lbl_max_page.grid(column=3,
                          row=1)

        # New Set buttons
        # btn_new_set_save = ttk.Button(text='Save & New set', master=frm_buttons)
        # btn_new_set_save.grid(column=0, row=0, padx=(10,0))

        btn_new_set_no_save = ttk.Button(text='New set',
                                         master=frm_buttons,
                                         command=lambda: load_new_set((btn_reveal, btn_mark_right, btn_mark_wrong, btn_shuffle),
                                                                      lbl_card_txt,
                                                                      lbl_current_page,
                                                                      lbl_max_page,
                                                                      lbl_set_name,
                                                                      sliders))
        btn_new_set_no_save.grid(column=0, row=0, padx=(10,0), pady=10)

        lbl_new_set_warning = tk.Label(text='(Current progress will be lost!)',
                            master=frm_buttons)

        lbl_new_set_warning.grid(column=1, row=0, pady=10)

        # Priority sliders
        i = 1
        sliders = {}
        for txt in ("Days since review", "Least reviewed", "Least accurate"):
            lbl_txt = tk.Label(text=txt,
                               master=frm_buttons)
            lbl_txt.grid(column=0, row = i, padx=(10,5), pady=(0,5), sticky='w')

            lbl_val = tk.Label(text="0.00", master=frm_buttons)
            lbl_val.grid(column=1, row=i, pady=(0,5), padx=0, sticky='e')

            sld = ttk.Scale(from_=0, to=10,
                            master=frm_buttons,
                            command=lambda value, lbl=lbl_val: update_slider(value, lbl))
            sld.grid(column=1, row=i, pady=(0,5), sticky='w')

            sliders[txt]=sld
            i += 1

        print(sliders)



window = tk.Tk()
window.columnconfigure(0, weight=1, minsize=200)
window.rowconfigure([0, 2], weight=1, minsize=50)
window.resizable(width=False, height=False)
window.title('Flashcards')