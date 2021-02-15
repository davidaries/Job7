from tkinter import *
import sqlite3
from database_interactor import database_interactor
import db_tools
import initial_load
from icecream import ic

conn = sqlite3.connect('language_dict.db')
root = Tk()
root.title('Language DB 1.0')  # title for window
root.geometry('900x600+0+0')  # main window geometry
rows = 0
while rows < 10:
    root.rowconfigure(rows, weight=1)
    root.columnconfigure(rows,weight=1)
    rows += 1

print('connection made')

interactor = database_interactor(conn, root)
interactor.populate()
#reload data from initial load
# initial_load.initial_load(conn)


# to delete all data from a dict
# vals = conn.execute("SELECT vocab, term, other from Spanish_words")
#
# for row in vals:
#     ex = '''DELETE from Spanish_words where vocab ='%s' ''' %(row[0])
#     conn.execute(ex)
#     ic('~vocab: ', row[0])
#     ic('term: ', row[1])
#     ic('other: ', row[2])
# conn.commit()

root.mainloop()