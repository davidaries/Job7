from tkinter import *
from tkinter import font as tk_font
import db_tools
from icecream import ic

class database_interactor:

    def __init__(self, connection, root):
        self.db_conn = connection
        self.root = root
        self.medium_font = tk_font.Font(root=self.root.master, family='Helvetica', size=12, weight=tk_font.BOLD)
        self.larger_font = tk_font.Font(root=self.root.master, family='Helvetica', size=14, weight=tk_font.BOLD)
        self.inputs = {}


    def populate(self):
        self.top_buttons()

    def top_buttons(self):
        print('starting')
        #search DB
        btn_search = Button(self.root, text='Search', font = self.larger_font,
                            command=lambda: self.search_listener(),
                            fg="black", bg="light gray", width=10)
        btn_search.grid(row=0, column = 0, sticky = NW)
        #add to DB
        btn_search = Button(self.root, text='Add', font = self.larger_font,
                            command=lambda: self.search_listener(),
                            fg="black", bg="light gray", width=10)
        btn_search.grid(row=0, column = 10, sticky =NE)

    def search_listener(self):
        self.clear_window()
        self.top_buttons()
        # lbl = Label(self.root, text='Search:', font=self.larger_font)
        # lbl.grid(row=1, column=0, sticky='W')
        text_entered = StringVar

        entry_box = Entry(self.root, textvariable=text_entered, font = self.medium_font)
        self.inputs['search'] = entry_box
        # self.widgets.append((value, entry_box, info[1]))
        btn_search = Button(self.root, text='Search', font=self.medium_font,
                            command= self.search_val,
                            fg="black", bg="light gray", width=10)
        btn_search.grid(row=1, column=10, sticky=E)

        entry_box.grid(row=1, column=0, ipadx= 60,ipady=5, sticky='W')


        print('search')
    def add_listener(self):
        self.clear_window()
        self.top_buttons()
        print('add')

    def clear_window(self):
        """This function clears the window that it is given allowing it to be a blank canvas before the window
        is repopulated with different widgets
        """
        for widget in self.root.winfo_children():
            widget.destroy()

    def search_val(self):
        val =self.inputs.get('search').get()
        db_tools.search_value(val, self.db_conn)
        # lbl = Label(self.root, text='Search:', font=self.larger_font)
        # lbl.grid(row=1, column=0, sticky='W')