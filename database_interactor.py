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
        self.menu()

    def menu(self):  # finish compare func
        print('starting')
        # search DB
        btn_search = Button(self.root, text='Search', font=self.larger_font,
                            command=self.search_listener,
                            fg="black", bg="light gray")
        btn_search.grid(row=0, column=0, sticky=NW)
        btn_compare = Button(self.root, text='Compare', font=self.larger_font,
                             command=self.compare_listener,
                             fg="black", bg="light gray")
        btn_compare.grid(row=0, column=4, sticky=NE)
        # add to DB
        btn_add = Button(self.root, text='Add', font=self.larger_font,
                         command=self.add_listener,
                         fg="black", bg="light gray")
        btn_add.grid(row=0, column=10, sticky=NE)

    def search_listener(self):

        self.clear_window()
        self.inputs.clear()
        self.root.bind('<Return>', lambda event: self.search_val())

        text_entered = StringVar

        entry_box = Entry(self.root, textvariable=text_entered, font=self.medium_font, width =50)
        entry_box.grid(row=1, column=0, sticky='W')
        self.inputs['search'] = entry_box
        # self.widgets.append((value, entry_box, info[1]))
        btn_search = Button(self.root, text='=>', font=self.medium_font,
                            command=self.search_val,
                            fg="black", bg="light gray")
        btn_search.grid(row=1, column=1, sticky=W)
        btn_menu = Button(self.root, text='Menu', font=self.medium_font,
                          command=self.reset,
                          fg="black", bg="light gray")
        btn_menu.grid(row=9, column=10, sticky=W)


        display_box = Text(self.root)
        display_box.grid(row=2, column=0, columnspan= 15, sticky=W)
        self.inputs['display'] = display_box

    def add_listener(self):
        ic(self.inputs)
        self.clear_window()
        self.inputs.clear()
        tables = []
        tbl_names = db_tools.get_table_names(self.db_conn)
        for tbl in tbl_names:
            if tbl.__contains__('words'):
                tables.append(tbl)
        option = StringVar(self.root)
        self.inputs['add'] = option
        drop_down = OptionMenu(self.root, option, *tables)
        drop_down.grid(row=0, column=0, sticky=W, columnspan=10)
        btn_add = Button(self.root, text='=>', font=self.medium_font,
                         command=self.add_to_tbl,
                         fg="black", bg="light gray")
        btn_add.grid(row=0, column=1, sticky=E)
        btn_menu = Button(self.root, text='Menu', font=self.medium_font,
                          command=self.reset,
                          fg="black", bg="light gray")
        btn_menu.grid(row=9, column=10, sticky=W)

    def add_to_tbl(self):
        self.clear_window()

        opt = self.inputs.get('add').get()
        self.add_listener()

        term_e = StringVar()
        term_s = StringVar()
        code = StringVar()
        if opt == 'English_words':
            Label(self.root, text='Term: ', font=self.medium_font).grid(row=2, column=0)
            Entry(self.root, textvariable=term_e, font=self.medium_font).grid(row=2, column=1, columnspan=5)
            self.inputs['English_words'] = term_e
        elif opt == 'Spanish_words':
            Label(self.root, text='Término: ', font=self.medium_font).grid(row=2, column=0)
            Label(self.root, text='Term: ', font=self.medium_font).grid(row=3, column=0)
            Entry(self.root, textvariable=term_s, font=self.medium_font).grid(row=2, column=1, columnspan=5)
            Entry(self.root, textvariable=term_e, font=self.medium_font).grid(row=3, column=1, columnspan=5)
            self.inputs['Spanish_words'] = term_s
            self.inputs['English_words'] = term_e
        elif opt == 'UMLS_words':
            Label(self.root, text='Term: ', font=self.medium_font).grid(row=2, column=0)
            Label(self.root, text='Code: ', font=self.medium_font).grid(row=3, column=0)
            Entry(self.root, textvariable=term_e, font=self.medium_font).grid(row=2, column=1, columnspan=5)
            Entry(self.root, textvariable=code, font=self.medium_font).grid(row=3, column=1, columnspan=5)
            self.inputs['UMLS_words'] = term_e
            self.inputs['UMLS_CUI'] = code
        elif opt == 'ICD10_words':
            Label(self.root, text='Term: ', font=self.medium_font).grid(row=2, column=0)
            Label(self.root, text='Code: ', font=self.medium_font).grid(row=3, column=0)
            Entry(self.root, textvariable=term_e, font=self.medium_font).grid(row=2, column=1, columnspan=5)
            Entry(self.root, textvariable=code, font=self.medium_font).grid(row=3, column=1, columnspan=5)
            self.inputs['ICD10_words'] = term_e
            self.inputs['ICD10_codes'] = code
        btn_add = Button(self.root, text='Add', font=self.medium_font,
                         command=self.process_adds,
                         fg="black", bg="light gray", width=10)
        btn_add.grid(row=9, column=0, sticky=W)
        btn_menu = Button(self.root, text='Menu', font=self.medium_font,
                          command=self.reset,
                          fg="black", bg="light gray", width=10)
        btn_menu.grid(row=9, column=10, sticky=W)

    def compare_listener(self):
        self.clear_window()
        self.inputs.clear()
        tables1 = []
        tbl_names = db_tools.get_table_names(self.db_conn)
        for tbl in tbl_names:
            if tbl.__contains__('words'):
                tables1.append(tbl)
        option1 = StringVar(self.root)
        self.inputs['option1'] = option1
        drop_down = OptionMenu(self.root, option1, *tables1)
        drop_down.grid(row=0, column=0, sticky=W, columnspan=10)
        option2 = StringVar(self.root)
        self.inputs['option2'] = option2
        drop_down = OptionMenu(self.root, option2, *tables1)
        drop_down.grid(row=0, column=5, sticky=W, columnspan=10)
        checked = IntVar()
        box = Checkbutton(self.root, text='Only different', variable=checked,
                          onvalue=1, offvalue=0, font = self.medium_font)
        self.inputs['different'] = checked
        box.grid(row= 0, column=9, sticky=W)
        btn_menu = Button(self.root, text='Menu', font=self.medium_font,
                          command=self.reset,
                          fg="black", bg="light gray", width=10)
        btn_menu.grid(row=9, column=10, sticky=W)
        btn_compare = Button(self.root, text='Compare', font=self.medium_font,
                          command=self.compare_db,
                          fg="black", bg="light gray", width=10)
        btn_compare.grid(row=9, column=0, sticky=W)

    def compare_db(self):
        results = db_tools.compare(self.inputs.get('option1').get(),self.inputs.get('option2').get(),self.inputs.get('different').get())
        dictionary = self.inputs.get('option1').get()

        display1 = Text(self.root)
        display1.grid(row=2, column=0, columnspan=15, sticky=W)
        display2 = Text(self.root)
        display2.grid(row=2, column=5, columnspan=15, sticky=W)
        for r in results[0]:
            vocab = r[0]
            term = r[1]
            ins = '%s\n %s\t%s\n' % (dictionary, vocab, term)
            display1.insert(INSERT, ins)
        dictionary = self.inputs.get('option2').get()
        for r in results[1]:
            vocab = r[0]
            term = r[1]
            ins = '%s\n %s\t%s\n' % (dictionary, vocab, term)
            display2.insert(INSERT, ins)
    def process_adds(self):
        processed = True
        unprocessed_row = 0
        self.clear_window()
        for i in self.inputs:
            processed = True
            if i != 'add':
                processed = db_tools.add_to_db(self.db_conn, i, self.inputs.get(i).get())
                if not processed:
                    Label(self.root, text = self.inputs.get(i).get()+' not processed for dictionary '+ i,
                          font = self.larger_font).grid(row = unprocessed_row, column =5,sticky = N)
                    unprocessed_row+=1
                    self.root.after(1000, self.reset)
        self.reset()

    def reset(self):
        self.clear_window()
        self.inputs.clear()
        self.menu()

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
            self.format_display(data, display, val)

    def format_display(self, data, display, val):
        dictionary = data[0]
        vocab = data[1]
        term = data[2]
        ins = '%s\n %s\t%s\n' % (dictionary, vocab, term)
        display.insert(INSERT, ins)
        if dictionary == 'ICD10_words' and val[0]!='~':
            dictionary = 'ICD10_codes'
            code = db_tools.get_vocab(dictionary, data[1])
            ins = '%s\n %s\t%s\n' % (dictionary, vocab, code)
            display.insert(INSERT, ins)
        elif dictionary == 'UMLS_words' and val[0]!='~':
            dictionary = 'UMLS_CUI'
            code = db_tools.get_vocab(dictionary, data[1])
            ins = '%s\n %s\t%s\n' % (dictionary, vocab, code)
            display.insert(INSERT, ins)
