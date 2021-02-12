from tkinter import *
from tkinter import font as tk_font
import db_tools
from icecream import ic


# from pynput.keyboard import Listener


class database_interactor:

    def __init__(self, connection, root):
        self.db_conn = connection
        db_tools.load_db_data(connection)
        self.root = root
        self.medium_font = tk_font.Font(root=self.root.master, family='Helvetica', size=12, weight=tk_font.BOLD)
        self.larger_font = tk_font.Font(root=self.root.master, family='Helvetica', size=14, weight=tk_font.BOLD)
        self.inputs = {}

    def populate(self):
        self.top_buttons()

    def top_buttons(self):
        print('starting')
        # search DB
        btn_search = Button(self.root, text='Search', font=self.larger_font,
                            command=self.search_listener,
                            fg="black", bg="light gray", width=10)
        btn_search.grid(row=0, column=0, sticky=NW)
        # btn_compare = Button(self.root, text='Compare', font=self.larger_font,
        #                      command=self.compare_listener,
        #                      fg="black", bg="light gray", width=10)
        # btn_compare.grid(row=0, column=5, sticky=NE)
        # add to DB
        btn_add = Button(self.root, text='Add', font=self.larger_font,
                         command=self.add_listener,
                         fg="black", bg="light gray", width=10)
        btn_add.grid(row=0, column=10, sticky=NE)

    def search_listener(self):
        self.clear_window()
        self.inputs.clear()
        self.top_buttons()
        self.root.bind('<Return>', lambda event: self.search_val())

        text_entered = StringVar

        entry_box = Entry(self.root, textvariable=text_entered, font=self.medium_font)
        self.inputs['search'] = entry_box
        # self.widgets.append((value, entry_box, info[1]))
        btn_search = Button(self.root, text='Search', font=self.medium_font,
                            command=self.search_val,
                            fg="black", bg="light gray", width=10)
        btn_search.grid(row=1, column=10, sticky=E)

        entry_box.grid(row=1, column=0, ipadx=100, ipady=5, sticky='W')

        display_box = Text(self.root)
        display_box.grid(row=2, column=0, ipadx=150, ipady=60)
        self.inputs['display'] = display_box

    def add_listener(self):
        self.clear_window()
        self.inputs.clear()
        self.top_buttons()
        tables = []
        tbl_names = db_tools.get_table_names(self.db_conn)
        for tbl in tbl_names:
            if tbl.__contains__('words'):
                tables.append(tbl)
        option = StringVar(self.root)
        self.inputs['add'] = option
        drop_down = OptionMenu(self.root, option, *tables)
        drop_down.grid(row=1, column=0, sticky=W, columnspan=5, ipadx=50, ipady=5)
        btn_add = Button(self.root, text='Add', font=self.medium_font,
                         command=self.add_to_tbl,
                         fg="black", bg="light gray", width=10)
        btn_add.grid(row=1, column=10, sticky=E)

    def add_to_tbl(self):
        self.clear_window()
        self.top_buttons()
        opt = self.inputs.get('add').get()
        self.inputs.clear()
        term_e = StringVar()
        term_s = StringVar()
        code = StringVar()
        if opt == 'English_words':
            Label(self.root, text='Term: ', font=self.medium_font).grid(row=1, column=0)
            entry_box_t = Entry(self.root, textvariable=term_e, font=self.medium_font).grid(row=1, column=1, columnspan =5)
            self.inputs['English_words'] = term_e
        elif opt == 'Spanish_words':
            Label(self.root, text='Término: ', font=self.medium_font).grid(row=1, column=0)
            Label(self.root, text='Term: ', font=self.medium_font).grid(row=1, column=0)
            Entry(self.root, textvariable=term_s, font=self.medium_font).grid(row=1, column=1, columnspan =5)
            Entry(self.root, textvariable=term_e, font=self.medium_font).grid(row=2, column=1, columnspan =5)
            self.inputs['Spanish_words'] = term_s
            self.inputs['English_words'] = term_e
        elif opt == 'UMLS_words':
            Label(self.root, text='Term: ', font=self.medium_font).grid(row=1, column=0)
            Label(self.root, text='Code: ', font=self.medium_font).grid(row=2, column=0)
            Entry(self.root, textvariable=term_e, font=self.medium_font).grid(row=1, column=1, columnspan =5)
            Entry(self.root, textvariable=code, font=self.medium_font).grid(row=2, column=1, columnspan =5)
            self.inputs['UMLS_words'] = term_e
            self.inputs['UMLS_CUI'] = code
        elif opt == 'ICD10_words':
            Label(self.root, text='Term: ', font=self.medium_font).grid(row=1, column=0)
            Label(self.root, text='Code: ', font=self.medium_font).grid(row=2, column=0)
            Entry(self.root, textvariable=term_e, font=self.medium_font).grid(row=1, column=1, columnspan =5)
            Entry(self.root, textvariable=code, font=self.medium_font).grid(row=2, column=1, columnspan =5)
            self.inputs['ICD10_words'] = term_e
            self.inputs['ICD10_codes'] = code
        btn_add = Button(self.root, text='Add', font=self.medium_font,
                         command=self.process_adds,
                         fg="black", bg="light gray", width=10)
        btn_add.grid(row=9, column=5, sticky=W)
    def process_adds(self):
        for i in self.inputs:
            db_tools.add_to_db(self.db_conn,i, self.inputs.get(i).get())
        self.clear_window()
        self.top_buttons()
    # def compare_listener(self):
    #     pass

    def clear_window(self):
        """This function clears the window that it is given allowing it to be a blank canvas before the window
        is repopulated with different widgets
        """
        for widget in self.root.winfo_children():
            widget.destroy()

    def search_val(self):
        val = self.inputs.get('search').get()
        display = self.inputs.get('display')
        display.delete("1.0", "end")
        search_data = db_tools.search_value(val, self.db_conn)
        # ic(search_data)
        for data in search_data:
            self.format_display(data, display)

        # lbl = Label(self.root, text='Search:', font=self.larger_font)
        # lbl.grid(row=1, column=0, sticky='W')

    def format_display(self, data, display):
        dictionary = data[0]
        vocab = data[1]
        term = data[2]
        ins = '%s\n %s\t%s\n' % (dictionary, vocab, term)
        display.insert(INSERT, ins)
        if dictionary == 'ICD10_words':
            dictionary = 'ICD10_codes'
            code = db_tools.get_vocab(dictionary, data[1])
            ins = '%s\n %s\t%s\n' % (dictionary, vocab, code)
            display.insert(INSERT, ins)
        elif dictionary == 'UMLS_words':
            dictionary = 'UMLS_CUI'
            code = db_tools.get_vocab(dictionary, data[1])
            ins = '%s\n %s\t%s\n' % (dictionary, vocab, code)
            display.insert(INSERT, ins)
