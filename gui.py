import tkinter as tk
import tkinter.ttk as ttk

from flashcard_controller import *

BTN_REVEAL_TXT = ('Show', 'Next')

FONT_NAME = 'Arial'
FONT_BIG = (FONT_NAME, 16)
FONT_SMALL = (FONT_NAME, 10)

class GUI:
    edit_decks_window_is_open = False
    edit_decks_window = None

    def __init__(self, parent):
        print('Start of GUI')

        frm_buttons = tk.Frame(width=100)
        frm_buttons.grid(column=0, row=0, sticky='nw')

        frm_card = tk.Frame(width=600, height=400, borderwidth=1, relief='solid')
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

        lbl_set_name=tk.Label(text='Click "New deck" to start!',
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

        btn_new_set_no_save = ttk.Button(text='New deck',
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

        btn_edit_decks = ttk.Button(text='Edit decks',
                                    master=frm_buttons,
                                    command=self.open_edit_decks_window)
        btn_edit_decks.grid(column=2, row=0,
                            padx=(30, 0))

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

    def open_edit_decks_window(self):
        if not self.edit_decks_window_is_open:
            self.edit_decks_window_is_open = True
            self.edit_decks_window = EditDeckGUI(window)
            self.edit_decks_window.protocol('WM_DELETE_WINDOW', lambda: self.close_edit_decks_window(self.edit_decks_window))

        self.edit_decks_window.lift()

    def close_edit_decks_window(self, window):
        print("Closed")
        self.edit_decks_window_is_open = False
        window.destroy()

class EditDeckGUI(tk.Toplevel):
    def __init__(self, master=None):

        super().__init__(master=master)

        # Frame of top menu
        frm_top_menu = tk.Frame(width=1000, master=self)
        frm_top_menu.grid(row=0, column=0)

        # Frame of deck title
        frm_deck_name = tk.Frame(master=self, width=1000)
        frm_deck_name.grid(row=1, column=0)

        # Frame of cards in deck
        self.frm_canvas = tk.Frame(master=self, width=800, height=100)
        self.frm_canvas.grid(row=2, column=0, sticky='news')
        self.frm_canvas.grid_rowconfigure(0, weight=1)
        self.frm_canvas.grid_columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(master=self.frm_canvas, width=470, height=400)
        self.canvas.grid(row=0, column=0, sticky='news')

        # Label for drop-down menu
        tk.Label(text='Deck to edit: ', master=frm_top_menu).grid(column=0, row=0)

        # Drop-down menu
        self.selected_deck = tk.StringVar(self)
        decks = db.fetch_all_sets()
        deck_names = sorted([decks[i][1] for i in range(len(decks))])
        self.decks_dict = { decks[i][1]:decks[i][0] for i in range(len(decks))}

        lst_decks = ttk.OptionMenu(frm_top_menu, self.selected_deck, deck_names[0], *deck_names)
        lst_decks.grid(column=1, row=0)

        # Load deck button
        ttk.Button(text='Open',
                   master=frm_top_menu,
                   command=self.load_deck_to_edit)\
            .grid(column=2, row=0)

        # Deck title
        self.lbl_selected_deck = tk.Label(font=FONT_BIG,
                                          text=self.selected_deck.get(),
                                          master=frm_deck_name)
        self.lbl_selected_deck.grid(column=0, row=1, sticky='w')

    def load_deck_to_edit(self, *args):
        global frm_deck_cards

        self.lbl_selected_deck.config(text=self.selected_deck.get())
        deck_id = self.decks_dict[self.selected_deck.get()]

        self.canvas.delete('all')

        frm_inside_canvas = tk.Frame(master=self.canvas)
        self.canvas.create_window((0, 0), window=frm_inside_canvas, anchor='nw')

        frm_deck_cards = tk.Frame(master=frm_inside_canvas)
        frm_deck_cards.grid(row=0, column=0)

        frm_deck_buttons = tk.Frame(master=frm_inside_canvas)
        frm_deck_buttons.grid(row=1, column=0, pady=20)

        btn_add_new_card = ttk.Button(text='Add', master=frm_deck_buttons, command=self.create_new_card_fields)
        btn_add_new_card.pack()

        # Scrollbar
        vbar = ttk.Scrollbar(master=self.frm_canvas, orient='vertical', command=self.canvas.yview)
        vbar.grid(row=0, column=1, sticky='ns')
        self.canvas.configure(yscrollcommand=vbar.set)

        # hbar = ttk.Scrollbar(master=frm_canvas, orient='horizontal', command=canvas.xview)
        # hbar.grid(row=1, column=0, sticky='ew')
        # canvas.configure(yscrollcommand=hbar.set)

        # Cards
        # deck_size
        deck_cards = db.fetch_flaschards(deck_id)
        print(deck_cards)
        self.deck_size = len(deck_cards)

        self.entry_field_frames = []
        self.entry_field_labels = []
        for i in range(self.deck_size):
            self.create_card_fields(frm_deck_cards, i, deck_cards[i][0], deck_cards[i][1], deck_cards[i][2])

            # txt_front_side = tk.Entry(master=frm_deck_cards)
            # txt_front_side.grid(row=i, column=0, pady=10)

        # canvas.config(scrollregion=canvas.bbox('all'))
        self.canvas.config(scrollregion=(0, 0, 450, 51 * self.deck_size + 50))

    def create_new_card_fields(self):
        global frm_deck_cards

        self.deck_size += 1
        print(self.deck_size)

        self.create_card_fields(frm_deck_cards, self.deck_size-1)
        self.canvas.config(scrollregion=(0, 0, 450, 51 * self.deck_size + 50))
        self.canvas.yview_moveto(1)

    def delete_card(self, frm):
        frm.grid_remove()

        idx = self.entry_field_frames.index(frm)

        for i in range(idx+1, len(self.entry_field_frames)):
            new_id = int(self.entry_field_labels[i]["text"])-1
            self.entry_field_labels[i].config(text=new_id)
            self.entry_field_frames[i].grid_forget()
            self.entry_field_frames[i].grid(row=new_id-1, column=0)

        del self.entry_field_frames[idx]
        del self.entry_field_labels[idx]
        self.deck_size -= 1
        self.canvas.config(scrollregion=(0, 0, 450, 51 * self.deck_size + 50))

    def create_card_fields(self, master, row, front='', back='', hint=''):
        frm_entry = tk.Frame(master=master)
        frm_entry.grid(row=row, column=0)

        lbl_card_number = tk.Label(master=frm_entry, text=f'{row + 1}')
        lbl_card_number.grid(row=row, column=0, sticky='nsw', padx=10, pady=(10 if row > 0 else 0, 0))

        tk.Label(master=frm_entry, text='Front side').grid(row=row, column=1, sticky='nw',
                                                                pady=(10 if row > 0 else 0, 20))
        entry_front_side = tk.Entry(master=frm_entry)
        entry_front_side.grid(row=row, column=1, sticky='sw', padx=(0, 10))
        entry_front_side.insert(0, front)

        tk.Label(master=frm_entry, text='Back side').grid(row=row, column=2, sticky='nw',
                                                               pady=(10 if row > 0 else 0, 20))
        entry_back_side = tk.Entry(master=frm_entry)
        entry_back_side.grid(row=row, column=2, sticky='sw', padx=(0, 10))
        entry_back_side.insert(0, back)

        tk.Label(master=frm_entry, text='Hint side').grid(row=row, column=3, sticky='nw',
                                                               pady=(10 if row > 0 else 0, 20))
        entry_hint_side = tk.Entry(master=frm_entry)
        entry_hint_side.grid(row=row, column=3, sticky='sw')
        entry_hint_side.insert(0, hint)

        btn_delete = ttk.Button(text='X', master=frm_entry, width=3,
                                command=lambda:self.delete_card(frm_entry))
        btn_delete.grid(row=row, column=4, sticky='e', padx=10)

        self.entry_field_frames.insert(row, frm_entry)
        self.entry_field_labels.insert(row, lbl_card_number)

window = tk.Tk()
window.columnconfigure(0, weight=1, minsize=400)
window.rowconfigure([0, 2], weight=1, minsize=50)
window.resizable(width=False, height=False)
window.title('Flashcards')