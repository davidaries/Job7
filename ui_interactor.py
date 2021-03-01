from tkinter import *
from tkinter import font as tk_font
import db_tools
from icecream import ic

"""Successful or failed mini add
Token search for synonyms
remove duplicates from view
Remove categories from 
"""


class database_interactor:
    """Class database_interactor populates the root window with various widgets used for searching the database,
    comparing tables, and adding to the database.  When the interactor first loads, the user is able to choose
    between these three options at the top and upon selecting an option the corresponding widgets will be populated
    to the window.  There is also a menu button added to the bottom of the screen allowing the user to go back and choose
    a different log interaction option.  The user interacts with what has been displayed on the screen and
    database_interactor then makes the corresponding calls to db_tools (to add data to or get data from the database)
    :param self.db_conn: a reference to the established connection with the database
    :type self.db_conn: sqlite3.Connection
    :param self.root: a reference to the root window
    :type self.root: tk Window
    :param self.medium_font:
    :param self.larger_font:
    :param self.inputs"""

    def __init__(self, connection, root):
        self.db_conn = connection
        db_tools.load_db_data(connection)
        self.root = root
        self.medium_font = tk_font.Font(root=self.root.master, family='Helvetica', size=12, weight=tk_font.BOLD)
        self.larger_font = tk_font.Font(root=self.root.master, family='Helvetica', size=14, weight=tk_font.BOLD)
        self.inputs = {}
        self.special_add = {}
        self.lang_to_dict = {'English': 'English_words', 'Espanol': 'Spanish_words'}
        self.lang = StringVar()
        self.lang.set('English')

    def menu(self):  # finish compare func
        """Sets up the main menu of the window with three buttons on the top for navigating to the search functionality,
        the compare functionality, or the add functionality
        """
        btn_search = Button(self.root, text='Search', font=self.larger_font,
                            command=self.search_listener,
                            fg="black", bg="light gray")
        btn_search.grid(row=0, column=0, sticky=NW)
        btn_compare = Button(self.root, text='Compare', font=self.larger_font,
                             command=self.compare_listener,
                             fg="black", bg="light gray")
        btn_compare.grid(row=0, column=4, sticky=N, columnspan=2)
        drop_down = OptionMenu(self.root, self.lang, *self.lang_to_dict.keys())
        drop_down.config(font=self.medium_font)
        drop_down.grid(row=1, column=4, sticky=N, columnspan=2)
        # add to DB
        btn_add = Button(self.root, text='Add', font=self.larger_font,
                         command=self.add_listener,
                         fg="black", bg="light gray")
        btn_add.grid(row=0, column=10, sticky=NE)

    def search_listener(self):
        """When the search functionality the is selected from the menu a search field is added to the window as well
        as a button enables the search (search is also binded to the return key).  Once the user enters a search value
        and enters it, the value is sent to process_adds function to process the values written"""
        self.clear_window()
        self.inputs.clear()
        self.root.bind('<Return>', lambda event: self.search_val())

        text_entered = StringVar()

        entry_box = Entry(self.root, textvariable=text_entered, font=self.medium_font, width=50)
        entry_box.grid(row=1, column=0, sticky='W')
        self.inputs['search'] = entry_box
        # self.widgets.append((value, entry_box, info[1]))
        btn_add_syn = Button(self.root, text='Add Synonym', font=self.medium_font,
                             command=self.syn_add,
                             fg="black", bg="light gray")
        btn_add_syn.grid(row=2, column=1, sticky=W)
        btn_add_syn = Button(self.root, text='Add Category', font=self.medium_font,
                             command=self.add_cat,
                             fg="black", bg="light gray")
        btn_add_syn.grid(row=2, column=2, sticky=W)
        # btn_add_syn.config(state = DISABLED)
        # self.inputs['add_syn'] = btn_add_syn
        # btn_search
        btn_menu = Button(self.root, text='Menu', font=self.medium_font,
                          command=self.reset,
                          fg="black", bg="light gray")
        btn_menu.grid(row=9, column=10, sticky=W)
        display_box = Listbox(self.root, width=100, height=20)
        display_box.grid(row=2, column=0, sticky=W)
        self.inputs['display'] = display_box
        categories_checked = IntVar()
        synonyms_checked = IntVar()
        cat_box = Checkbutton(self.root, text='Categories', variable=categories_checked,
                              onvalue=1, offvalue=0, font=self.medium_font)
        self.inputs['categories'] = categories_checked
        syn_box = Checkbutton(self.root, text='Synonyms', variable=synonyms_checked,
                              onvalue=1, offvalue=0, font=self.medium_font)
        self.inputs['synonyms'] = synonyms_checked
        cat_box.grid(row=1, column=1, sticky=W)
        syn_box.grid(row=1, column=2, sticky=W)

    def syn_add(self):
        """only synonyms for primary languaes
        STILL NEED TO CHECK FOR PRIMARY LANGUAGES AND PROCESS THE ADDS
        IN CURRENT FORM CANNOT USE CURRENT ADD TO DB METHOD, NEED TO REWORK"""
        selected_value = self.inputs['display'].get(ANCHOR)
        add = Tk()
        add.geometry("600x400")
        vocab = '~' + selected_value.split('~')[1][0:7]
        text_entered = StringVar()
        Label(add, text=selected_value).grid(row=0, column=0, sticky=W)
        entry_box = Entry(add, textvariable=text_entered, font=self.medium_font, width=50)
        entry_box.grid(row=1, column=0, sticky='W')
        self.inputs['add'] = entry_box
        btn_add_syn = Button(add, text='Add Synonym', font=self.medium_font,
                             command=lambda: db_tools.add_other(self.db_conn, 'English_synonyms', vocab, entry_box),
                             fg="black", bg="light gray")
        btn_add_syn.grid(row=1, column=1)

    #     ADD ERROR POPUP
    def add_cat(self):
        selected_value = self.inputs['display'].get(ANCHOR)
        add = Tk()
        add.geometry("600x400")
        vocab = '~' + selected_value.split('~')[1][0:7]
        categories = db_tools.get_remaining_categories(vocab)
        ic(categories)
        option = StringVar(add)
        Label(add, text=selected_value).grid(row=0, column=0, sticky=W)
        cat_opt = OptionMenu(add, option, *categories)
        cat_opt.grid(row=1, column=0, sticky='W')
        btn_add_category = Button(add, text='Add Category', font=self.medium_font,
                             command=lambda: db_tools.add_other(self.db_conn, 'Categories', vocab, option),
                             fg="black", bg="light gray")
        btn_add_category.grid(row=1, column=1, sticky='W')

    def add_listener(self):
        """When the add functionality the is selected from the menu, a drop down menu is presented that will allow
        the user to select from the various tables to add the appropriate values.  When the user has selected a table
        to add to, the process adds function is called to handle the adds for that table."""
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
        option.trace('w', self.add_to_tbl)
        drop_down.grid(row=0, column=0, sticky=W, columnspan=10)
        btn_menu = Button(self.root, text='Menu', font=self.medium_font,
                          command=self.reset,
                          fg="black", bg="light gray")
        btn_menu.grid(row=9, column=10, sticky=W)

    def add_to_tbl(self, *args):
        """Adds the appropriate input fields for the different tables, which are then added to the database
        :param args: needs to be included to allow the user to select an item from the drop down and have it call this
        function
        """
        self.clear_window()

        opt = self.inputs.get('add').get()
        self.add_listener()
        Label(self.root, text=opt, font=self.larger_font).grid(row=1, column=0, sticky=W)
        term_e = StringVar()
        term_s = StringVar()
        code = StringVar()
        if opt == 'English_words':
            Label(self.root, text='Term: ', font=self.medium_font).grid(row=2, column=0, sticky=W)
            Entry(self.root, textvariable=term_e, font=self.medium_font).grid(row=2, column=1, columnspan=5, sticky=W)
            self.inputs['English_words'] = term_e
        elif opt == 'Spanish_words':
            Label(self.root, text='Término: ', font=self.medium_font).grid(row=2, column=0, sticky=W)
            Label(self.root, text='Term: ', font=self.medium_font).grid(row=3, column=0, sticky=W)
            Entry(self.root, textvariable=term_s, font=self.medium_font).grid(row=2, column=1, columnspan=5, sticky=W)
            Entry(self.root, textvariable=term_e, font=self.medium_font).grid(row=3, column=1, columnspan=5, sticky=W)
            self.inputs['Spanish_words'] = term_s
            self.inputs['English_words'] = term_e
        elif opt == 'UMLS_words':
            Label(self.root, text='Term: ', font=self.medium_font).grid(row=2, column=0, sticky=W)
            Label(self.root, text='Code: ', font=self.medium_font).grid(row=3, column=0, sticky=W)
            Entry(self.root, textvariable=term_e, font=self.medium_font).grid(row=2, column=1, columnspan=5, sticky=W)
            Entry(self.root, textvariable=code, font=self.medium_font).grid(row=3, column=1, columnspan=5, sticky=W)
            self.inputs['UMLS_words'] = term_e
            self.inputs['UMLS_CUI'] = code
        elif opt == 'ICD10_words':
            Label(self.root, text='Term: ', font=self.medium_font).grid(row=2, column=0, sticky=W)
            Label(self.root, text='Code: ', font=self.medium_font).grid(row=3, column=0, sticky=W)
            Entry(self.root, textvariable=term_e, font=self.medium_font).grid(row=2, column=1, columnspan=5, sticky=W)
            Entry(self.root, textvariable=code, font=self.medium_font).grid(row=3, column=1, columnspan=5, sticky=W)
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
        """When the compare functionality the is selected from the menu, two drop down menus are populated to allow the
        user to choose the tables they are comparing.  Once the user has selected the tables they wish to compare (and
        whether they wish to display only the different values) the compared values are displayed on the Text boxers
        created by the compare db function."""
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
                          onvalue=1, offvalue=0, font=self.medium_font)
        self.inputs['different'] = checked
        box.grid(row=0, column=9, sticky=W)
        btn_menu = Button(self.root, text='Menu', font=self.medium_font,
                          command=self.reset,
                          fg="black", bg="light gray", width=10)
        btn_menu.grid(row=9, column=10, sticky=W)
        btn_compare = Button(self.root, text='Compare', font=self.medium_font,
                             command=self.compare_db,
                             fg="black", bg="light gray", width=10)
        btn_compare.grid(row=9, column=0, sticky=W)

    def add_comp(self):
        selected_value = self.root.focus_get().get(ANCHOR)
        add = Tk()
        add.geometry("600x400")
        # ic(self.inputs['display'].get(ANCHOR))
        vocab = '~' + selected_value.split('~')[1][0:7]
        text_entered = StringVar()
        Label(add, text=selected_value).grid(row=0, column=0, sticky=W)
        entry_box = Entry(add, textvariable=text_entered, font=self.medium_font, width=50)
        entry_box.grid(row=1, column=0, sticky='W')
        self.inputs['add'] = entry_box
        btn_add_syn = Button(add, text='Add Value', font=self.medium_font,
                             command=lambda: db_tools.add_other(self.db_conn, 'English_synonyms', vocab, entry_box),
                             fg="black", bg="light gray")
        btn_add_syn.grid(row=1, column=1)

    def compare_db(self):
        """compares the values between two different dictionaries and adds all of the compared values to two
        text boxes after being formatted for display"""
        results = db_tools.compare(self.inputs.get('option1').get(), self.inputs.get('option2').get(),
                                   self.inputs.get('different').get())
        dictionary = self.inputs.get('option1').get()

        display1 = Listbox(self.root, width=100, height=20)
        display1.grid(row=2, column=0, sticky=W)
        display2 = Listbox(self.root, width=100, height=20)
        display2.grid(row=2, column=5, sticky=W)
        Button(self.root, text='Add', command=self.add_comp, font=self.medium_font).grid(row=1, column=9)
        for r in results[0]:
            vocab = r[0]
            term = r[1]
            ins = '%s %s %s ' % (dictionary, vocab, term)
            display1.insert('end', ins)
        dictionary = self.inputs.get('option2').get()
        for r in results[1]:
            vocab = r[0]
            term = r[1]
            ins = '%s %s %s ' % (dictionary, vocab, term)
            display2.insert('end', ins)

    def process_adds(self):
        """sends all of the add values to the db_tools module to be processed and added to the database.  Displays
        the values not added to the database when values already exist in the database"""
        unprocessed_row = 0
        self.clear_window()
        self.inputs.pop('add')
        unprocessed = db_tools.add_to_db(self.db_conn, self.inputs)
        if unprocessed:
            self.clear_window()
            error = Tk()
            error.geometry("330x400")
            for up in unprocessed:
                Label(error,
                      text=up[1] + '\n not processed for dictionary ' + up[0],
                      font=self.larger_font).grid(row=unprocessed_row, column=5, sticky=N)
                unprocessed_row += 2
            self.root.after(2000, error.destroy)
        self.reset()

    def reset(self):
        """resets all of the values in database_interactor and returns the user to the menu"""
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
        """Displays all of the values returned by the db_tools search function to a text box in the UI"""
        val = self.inputs.get('search').get()
        display = self.inputs.get('display')
        display.delete(0, END)
        search_data = db_tools.search_value(val, self.db_conn)
        for data in search_data:
            self.format_display(data, display)

    def format_display(self, data, display):
        """"formats and writes all of the values to the display seen in the UI
        SHOULD BE ABLE TO REMOVE THE VAL WITH THE NEW HANDLING OF SEARCH, WILL EDIT THIS OUT IF NOT NEEDED
        :param data, the data from the db table to be displayed in the textbox
        :type data: list
        :param display: reference to the display box
        :type display: tk Text
        """
        ic(data)
        dictionary = data[0]
        vocab = data[1]
        term = data[2]
        ins = '%s   %s   %s' % (dictionary, vocab, term)
        display.insert('end', ins)
        if dictionary == 'English_words':
            if self.inputs.get('categories').get() == 1:
                """to be displayed on the same line with all of the various categories on that line
                catagories don't need to be present for the UMLS icd10 only primary langs"""
                cats = db_tools.get_vocab('Categories', vocab)
                ic(cats)
                dic = 'Categories'
                c_dict = self.lang_to_dict.get(self.lang.get())
                if cats:
                    ins = '%s \t\t  %s   %s' % (dic, vocab, ', '.join([db_tools.get_vocab(c_dict, val) for val in cats]))
                    display.insert('end', ins)
            if self.inputs.get('synonyms').get() == 1:
                dic = 'English_synonyms'
                syns = db_tools.get_vocab(dic, vocab)
                if syns:
                    ins = '%s \t\t  %s   %s' % (dic, vocab, ', '.join([val for val in syns]))
                    display.insert('end', ins)

    def succes_or_fail(self, window, val):
        """will be used to display the successful or failed add to the database"""
        pass
