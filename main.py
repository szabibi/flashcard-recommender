from gui import GUI, window
from db import flush_last_flags
# from flashcard_controller import load_new_set

# load_new_set()
flush_last_flags()

app = GUI(window)
window.mainloop()



