import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk

import db
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
        if window.unsaved:
            confirm = tk.messagebox.askyesnocancel('Warning', 'You have unsaved changes.\nSave before proceeding?',
                                                   default='yes')
            if confirm:
                window.save_deck()
            elif confirm is None:
                return

        self.edit_decks_window_is_open = False
        window.destroy()

class EditDeckGUI(tk.Toplevel):
    def __init__(self, master=None):

        super().__init__(master=master)

        # Frame of top menu
        self.frm_top_menu = tk.Frame(width=1000, master=self)
        self.frm_top_menu.grid(row=0, column=0, sticky='we', pady=10, padx=10)

        # Frame of deck title
        frm_deck_name = tk.Frame(master=self, width=1000)
        frm_deck_name.grid(row=1, column=0)

        frm_deck_name_buttons=tk.Frame(master=frm_deck_name)
        frm_deck_name_buttons.grid(row=1, column=0, pady=10)

        # Frame of cards in deck
        self.frm_canvas = tk.Frame(master=self, width=800, height=100)
        self.frm_canvas.grid(row=2, column=0, sticky='news')
        self.frm_canvas.grid_rowconfigure(0, weight=1)
        self.frm_canvas.grid_columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(master=self.frm_canvas, width=470, height=400)
        self.canvas.grid(row=0, column=0, sticky='news')

        # Label for drop-down menu
        tk.Label(text='Deck to edit: ', master=self.frm_top_menu).grid(column=0, row=0, sticky='w')

        # Drop-down menu
        self.selected_deck = tk.StringVar(self)
        decks = db.fetch_all_sets()
        deck_names = sorted([decks[i][1] for i in range(len(decks))])
        self.decks_dict = {decks[i][1]:decks[i][0] for i in range(len(decks))}

        self.dropdown_menu_init(deck_names)

        # Load deck button
        ttk.Button(text='Open',
                   master=self.frm_top_menu,
                   command=lambda:self.load_deck_to_edit(deck_names, entry_rename_deck, btn_confirm_rename_deck, var_rename_deck))\
            .grid(column=2, row=0)

        # Save deck button
        self.btn_save_deck = ttk.Button(text='Save',
                                        master=frm_deck_name_buttons,
                                        state='disabled',
                                        command=lambda:self.save_deck())

        # Rename deck button
        self.btn_rename_deck = ttk.Button(text='Rename',
                                          master=frm_deck_name_buttons,
                                          state='disabled',
                                          command=lambda:self.rename_deck(entry_rename_deck, btn_confirm_rename_deck, var_rename_deck))

        self.renaming_in_process = False

        # Delete deck button
        self.btn_delete_deck = ttk.Button(text='Delete',
                                          master=frm_deck_name_buttons,
                                          state='disabled')

        ttk.Button(text='New',
                   master=self.frm_top_menu).grid(column=6, row=0)

        self.btn_save_deck.grid(column=0, row=2)
        self.btn_rename_deck.grid(column=1, row=2)
        self.btn_delete_deck.grid(column=2, row=2)


        # Deck title
        self.lbl_selected_deck = tk.Label(font=FONT_BIG,
                                          text='Open a deck',
                                          master=frm_deck_name)
        self.lbl_selected_deck.grid(column=0, row=0, sticky='we')

        var_rename_deck = tk.StringVar()
        entry_rename_deck = tk.Entry(textvariable=var_rename_deck,
                                     master=frm_deck_name)
        btn_confirm_rename_deck = ttk.Button(text='OK',
                                             master=frm_deck_name,
                                             command=lambda:self.confirm_rename(deck_names, entry_rename_deck, btn_confirm_rename_deck, var_rename_deck))

        # Unsaved flag
        self.unsaved = False

    def dropdown_menu_init(self, names):
        lst_decks = ttk.OptionMenu(self.frm_top_menu, self.selected_deck, names[0], *names)
        lst_decks.grid(column=1, row=0)

    def set_deck_buttons_state(self, state):
        self.btn_save_deck.config(state=state)
        self.btn_rename_deck.config(state=state)
        self.btn_delete_deck.config(state=state)

    def rename_deck(self, entry, btn, sv):
        self.lbl_selected_deck.grid_forget()
        entry.grid(row=0, column=0, sticky='w')
        btn.grid(row=0, column=0, sticky='e')
        self.set_deck_buttons_state('disabled')
        sv.set(self.lbl_selected_deck['text'])

        self.renaming_in_process = True

    def confirm_rename(self, names, entry, btn, sv):
        old_name = self.lbl_selected_deck['text']
        new_name = sv.get()

        deck_id = self.decks_dict[old_name]

        # update database
        try:
            db.rename_deck(deck_id, new_name)
        except:
            tk.messagebox.showerror('Name not unique', f'There already exists a deck with the name \'{new_name}\'')
            return False

        names[names.index(old_name)] = new_name
        self.dropdown_menu_init(names)

        self.selected_deck.set(new_name)
        self.lbl_selected_deck.config(text=new_name)

        # replace dictionary entry with new name
        del self.decks_dict[old_name]
        self.decks_dict[new_name] = deck_id

        # update gui
        entry.grid_forget()
        btn.grid_forget()
        self.lbl_selected_deck.grid(row=0, column=0, sticky='we')
        self.set_deck_buttons_state('normal')

        self.renaming_in_process = False

    def load_deck_to_edit(self, *args):
        global frm_deck_cards

        if self.lbl_selected_deck['text'] == self.selected_deck.get():
            return

        if self.renaming_in_process:
            tk.messagebox.showinfo('Cannot open deck', 'You must finish renaming the current deck\nbefore opening another one.')
            self.selected_deck.set(self.lbl_selected_deck["text"])
            return

        if self.unsaved:
            confirm = tk.messagebox.askyesnocancel('Warning', 'You have unsaved changes.\nSave before proceeding?', default='yes')
            if confirm:
                self.save_deck()
            elif confirm is None:
                return # cancel load

        self.unsaved = False

        # activate save, rename and delete buttons
        self.set_deck_buttons_state('normal')

        self.lbl_selected_deck.config(text=self.selected_deck.get())
        self.deck_id = self.decks_dict[self.selected_deck.get()]

        self.canvas.delete('all')

        frm_inside_canvas = tk.Frame(master=self.canvas)
        self.canvas.create_window((0, 0), window=frm_inside_canvas, anchor='nw')

        frm_deck_cards = tk.Frame(master=frm_inside_canvas)
        frm_deck_cards.grid(row=0, column=0)

        frm_deck_buttons = tk.Frame(master=frm_inside_canvas)
        frm_deck_buttons.grid(row=1, column=0, pady=20)

        btn_add_new_card = ttk.Button(text='Add', master=self.frm_canvas, command=self.create_new_card_fields)
        btn_add_new_card.grid(row=1, column=0, pady=10)

        # Scrollbar
        vbar = ttk.Scrollbar(master=self.frm_canvas, orient='vertical', command=self.canvas.yview)
        vbar.grid(row=0, column=1, sticky='ns')
        self.canvas.configure(yscrollcommand=vbar.set)

        # hbar = ttk.Scrollbar(master=frm_canvas, orient='horizontal', command=canvas.xview)
        # hbar.grid(row=1, column=0, sticky='ew')
        # canvas.configure(yscrollcommand=hbar.set)

        # Cards
        # deck_size
        deck_cards = db.fetch_flashcards_with_id(self.deck_id)
        print(deck_cards)
        self.deck_size = len(deck_cards)

        self.cards_to_delete = []
        self.entry_field_card_info = []
        for i in range(self.deck_size):
            self.create_card_fields(frm_deck_cards, i, deck_cards[i][0], deck_cards[i][1], deck_cards[i][2], deck_cards[i][3])

        # canvas.config(scrollregion=canvas.bbox('all'))
        self.canvas.config(scrollregion=(0, 0, 450, 51 * self.deck_size + 50))

    def create_new_card_fields(self):
        global frm_deck_cards

        self.deck_size += 1
        print(self.deck_size)

        self.create_card_fields(frm_deck_cards, self.deck_size-1, new=True)
        self.canvas.config(scrollregion=(0, 0, 450, 51 * self.deck_size + 50))
        self.canvas.yview_moveto(1)

        self.mark_deck_as_unsaved(None)

    def delete_card(self, frm):
        frames = []
        for info in self.entry_field_card_info:
            frames.append(info['frame'])

        idx = frames.index(frm)

        if self.entry_field_card_info[idx]["front"].get() != '' or\
                self.entry_field_card_info[idx]["back"].get() != '' or\
                self.entry_field_card_info[idx]["hint"].get() != '':
            if not tk.messagebox.askyesno('Confirm', f'This action cannot be undone. Delete \'{self.entry_field_card_info[idx]["front"].get()}\'?', default='yes'):
                return

        frm.grid_remove()

        for i in range(idx+1, len(self.entry_field_card_info)):
            new_id = int(self.entry_field_card_info[i]['label']['text'])-1
            self.entry_field_card_info[i]['label'].config(text=new_id)
            self.entry_field_card_info[i]['frame'].grid_forget()
            self.entry_field_card_info[i]['frame'].grid(row=new_id-1, column=0)

        if self.entry_field_card_info[idx]['id'] is not None:
            self.cards_to_delete.append(self.entry_field_card_info[idx]['id'])
            print(self.cards_to_delete)

        del self.entry_field_card_info[idx]

        self.deck_size -= 1
        self.canvas.config(scrollregion=(0, 0, 450, 51 * self.deck_size + 50))

        self.mark_deck_as_unsaved(None)

    def create_card_fields(self, master, row, id=None, front='', back='', hint='', new=False):
        frm_entry = tk.Frame(master=master)
        frm_entry.grid(row=row, column=0)

        lbl_card_number = tk.Label(master=frm_entry, text=f'{row + 1}')
        lbl_card_number.grid(row=row, column=0, sticky='nswe', padx=10, pady=(10 if row > 0 else 0, 0))

        var_front_side = tk.StringVar()
        var_front_side.set(front)
        var_front_side.trace('w', lambda name, index, mode, sv=var_front_side: self.mark_deck_as_unsaved(sv))
        tk.Label(master=frm_entry, text='Front side').grid(row=row, column=1, sticky='nw',
                                                                pady=(10 if row > 0 else 0, 20))
        entry_front_side = tk.Entry(master=frm_entry, textvariable=var_front_side)
        entry_front_side.grid(row=row, column=1, sticky='sw', padx=(0, 10))

        var_back_side = tk.StringVar()
        var_back_side.set(back)
        var_back_side.trace('w', lambda name, index, mode, sv=var_back_side: self.mark_deck_as_unsaved(sv))
        tk.Label(master=frm_entry, text='Back side').grid(row=row, column=2, sticky='nw',
                                                               pady=(10 if row > 0 else 0, 20))
        entry_back_side = tk.Entry(master=frm_entry, textvariable=var_back_side)
        entry_back_side.grid(row=row, column=2, sticky='sw', padx=(0, 10))

        var_hint_side = tk.StringVar()
        var_hint_side.set(hint)
        var_hint_side.trace('w', lambda name, index, mode, sv=var_hint_side: self.mark_deck_as_unsaved(sv))
        tk.Label(master=frm_entry, text='Hint side').grid(row=row, column=3, sticky='nw',
                                                               pady=(10 if row > 0 else 0, 20))
        entry_hint_side = tk.Entry(master=frm_entry, textvariable=var_hint_side)
        entry_hint_side.grid(row=row, column=3, sticky='sw')

        btn_delete = ttk.Button(text='X', master=frm_entry, width=3,
                                command=lambda:self.delete_card(frm_entry))
        btn_delete.grid(row=row, column=4, sticky='e', padx=10)

        self.entry_field_card_info.insert(row, {'frame':frm_entry,
                                             'label':lbl_card_number,
                                             'id':id,
                                             'front':var_front_side,
                                             'back':var_back_side,
                                             'hint':var_hint_side,
                                             'new':new})

    def mark_deck_as_unsaved(self, sv):
        self.unsaved = True

    def save_deck(self, *args):
        if self.unsaved:

            # update cards in database
            for info in self.entry_field_card_info:
                if info['new']:
                    db.add_card(self.deck_id, info['front'].get(), info['back'].get(), info['hint'].get())
                    id = db.get_cur().lastrowid
                    info['id'] = id
                    info['new'] = False
                else:
                    db.update_card(info['id'], info['front'].get(), info['back'].get(), info['hint'].get())

            # delete cards to database
            for id in self.cards_to_delete:
                db.delete_card(id)
                print('Deleted card', id, 'remaining:', self.cards_to_delete)
            self.cards_to_delete.clear()

            db.commit()

            self.unsaved = False

window = tk.Tk()
window.columnconfigure(0, weight=1, minsize=400)
window.rowconfigure([0, 2], weight=1, minsize=50)
window.resizable(width=False, height=False)
window.title('Flashcards')