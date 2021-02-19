from tkinter import *
import sqlite3
from database_interactor import database_interactor
import db_tools
import initial_load
from icecream import ic

# connect to DB
conn = sqlite3.connect('language_dict.db')
# Set up the main window

root = Tk()
root.title('Language DB 1.0')  # title for window
root.geometry('1500x600+0+0')  # main window geometry
rows = 0
# Apply standard row and column size to the window
while rows < 10:
    root.rowconfigure(rows, weight=1)
    root.columnconfigure(rows, weight=1)
    rows += 1
# load and populate the database interactor
interactor = database_interactor(conn, root)
interactor.menu()

root.mainloop()
