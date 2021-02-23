import random
from icecream import ic

all_dicts = {}
tbl_special = []

def generate_vocab(conn):
    """creates a ~vocab (~XXXXXXX) (where x is in number 0-9) to be assigned to a database entry by creating a random
    value between 0 and 9999999 (with leading zeros)
    :param conn: connection to the database
    :type conn: sqlite3.Connection"""
    used_vocabs = []
    vals = conn.execute("SELECT vocab, term, other from English_words")
    for row in vals:
        used_vocabs.append(row[0])
    # print(used_vocabs)
    ran = random.randint(0000000, 9999999)
    if "~%07d" % ran not in used_vocabs:
        vocab = "~%07d" % ran
    else:
        while "~%07d" % ran in used_vocabs:
            ran = random.randint(0000000, 9999999)
        vocab = "~%07d" % ran
    return vocab


def get_table_names(conn):
    """returns all of the names of the tables in the database
    :param conn: connection to the database
    :type conn: sqlite3.Connection
    :return: the values of all of the table names
    :rtype: list"""
    vals = conn.execute("SELECT type, name from sqlite_master")
    tbl_names = []
    for row in vals:
        if row[0] == 'table':
            tbl_names.append(row[1])
    return tbl_names


def search_value(val, conn):
    """searches a value from all of the possible values in the database.  Checks and adds ICD10 and UMLS codes if not
    given a ~vocab value
    :param val: value to be searched from the database
    :type val: str
    :param conn: connection to the database
    :type conn: sqlite3.Connection
    :return: the values matched by the search
    :rtype: list
    """
    tbl_names = get_table_names(conn)
    values = []
    if not val:  # Check for no input
        for tbl in tbl_names:
            if tbl not in tbl_special:
                for d in all_dicts.get(tbl):
                    values.append((tbl, d, all_dicts.get(tbl).get(d)))
    else:
        for tbl in tbl_names:
            if tbl not in tbl_special:
                if val[0] != '~':
                    for d in all_dicts.get(tbl):
                        # ic(get_vocab(tbl, d).lower())
                        if str(get_vocab(tbl, d).lower()).__contains__(val.lower()):
                            values.append((tbl, d, get_vocab(tbl, d)))
                else:
                    for d in all_dicts.get(tbl):
                        if d == val:
                            values.append((tbl, d, get_vocab(tbl, d)))
        if val[0] != '~':
            for v in values:
                if v[0] == 'ICD10_words':
                    tbl = 'ICD10_codes'
                    values.append((tbl, v[1], get_vocab(tbl, v[1])))
                if v[0] == 'UMLS_words':
                    tbl = 'UMLS_CUI'
                    values.append((tbl, v[1], get_vocab(tbl, v[1])))

    return values
    # tbl_names = get_table_names(conn)
    # values = []
    # if not val:  # Check for no input
    #     for tbl in tbl_names:
    #         for d in all_dicts.get(tbl):
    #             values.append((tbl, d[0], get_vocab(tbl, d)[1]))
    # else:
    #     for tbl in tbl_names:
    #         if val[0] != '~':
    #             for d in all_dicts.get(tbl):
    #                 if str(get_vocab(tbl, d)[1].lower()).__contains__(val.lower()):
    #                     values.append((tbl, d[0], get_vocab(tbl, d)[1]))
    #         else:
    #             ic(tbl)
    #             ic(all_dicts.get(tbl))
    #             for d in all_dicts.get(tbl):
    #                 ic(d)
    #                 if d[0] == val:
    #                     values.append((tbl, d[0], get_vocab(tbl, d)[1]))
    #     if val[0] != '~':
    #         for v in values:
    #             if v[0] == 'ICD10_words':
    #                 tbl = 'ICD10_codes'
    #                 values.append((tbl, v[1], get_vocab(tbl, v[1])[1]))
    #             if v[0] == 'UMLS_words':
    #                 tbl = 'UMLS_CUI'
    #                 values.append((tbl, v[1], get_vocab(tbl, v[1])[1]))
    #
    # return values


def load_db_data(conn):
    """loads all of the values in the current database and create a dictionary of dictionaries of those values
    :param conn: connection to the database
    :type conn: sqlite3.Connection"""
    all_dicts.clear()
    tbl_names = get_table_names(conn)

    tbl_special.append(tbl_names.pop(tbl_names.index('Categories')))
    tbl_special.append(tbl_names.pop(tbl_names.index('English_synonyms')))
    # ic(tbl_special)
    for tbl in tbl_names:
        ex = "SELECT * from %s" % tbl
        vals = conn.execute(ex)
        lang_dict = {}
        for v in vals:
            lang_dict[v[0]] = v[1]
        all_dicts[tbl] = lang_dict

    # all_dicts.clear()
    # tbl_names = get_table_names(conn)
    for tbl in tbl_special:
        ex = "SELECT * from %s" % tbl
        vals = conn.execute(ex)
        lang_dict = []
        for v in vals:
            lang_dict.append((v[0],v[1]))
        all_dicts[tbl] = lang_dict

def get_categories(vocab):
    dic = 'Categories'
    return [(dic,c[0],c[1]) for c in all_dicts[dic] if c[0] == vocab]
    # for c in all_dicts[dic]:
    #     if c[0] == vocab:
    #         ic(c[0])


def get_synonyms(vocab):
    dic = 'English_synonyms'
    ic(vocab)
    ic(all_dicts[dic])
    return [(dic,c[0],c[1]) for c in all_dicts[dic] if c[0] == vocab]

def get_vocab(dic, vocab):
    """returns a specific vocab value from a specific dictionary
    :return: the value described above
    :rtype: str"""
    if dic not in tbl_special:
        return all_dicts.get(dic).get(vocab)
    else:
        return [all_dicts[dic][1] for v in all_dicts[dic] if v[0] == vocab]
        # for v in all_dicts[dic]:
        #     if v[0] == vocab[0]:
        #         return v[1]


def add_to_db(conn, add_dict):
    """adds values to the database and the dictionary used by the db interactor
    :param conn: connection to the database
    :type conn: sqlite3.Connection
    :param add_dict: The value to be added to the databse
    :type add_dict: dict
    :return: a list of all of the values not added to the db and the dictionary
    :rtype: list
    """
    vocab = generate_vocab(conn)
    keys = add_dict.keys()
    to_process = []
    for k in keys:
        if add_dict.get(k).get().lower() not in [v.lower() for v in all_dicts.get(k).values()]:
            to_process.append([True, k, add_dict[k].get()])
        else:
            to_process.append([False, k, add_dict[k].get()])
    unprocessed = []
    for p in to_process:
        if p[0]:
            other = 'NA'
            vals_en = '''('%s','%s','%s')''' % (vocab, p[2], other)
            addition_en = '''INSERT INTO %s (vocab, term, other)VALUES %s''' % (p[1], vals_en)
            conn.execute(addition_en)
            conn.commit()
            all_dicts.get(p[1])[vocab] = p[2]
        else:
            unprocessed.append([p[1], p[2]])
    return unprocessed


# check existence in DB func
# compare for missing terms func
def compare(tbl1, tbl2, different):
    """Compares and returns the values from two different tables.  if the different value is true, the return is only
    the values that the two dictionaries don't have in common.  Otherwise, both dictionaries are returned in full
    :param tbl1: the first table to be compared
    :type tbl1: str
    :param tbl2: the second table to be compared
    :type tbl2: str
    :param different: a value that says whether the tables should only return the differences
    :type different: bool
    :return: the two lists for the compared tables
    :rtype: list, list
    """
    comp1 = []
    comp2 = []
    if different == 1 and tbl1 and tbl2:
        comp1 = [[v, all_dicts[tbl1].get(v)] for v in all_dicts[tbl1] if v not in all_dicts[tbl2]]
        comp2 = [[v, all_dicts[tbl2].get(v)] for v in all_dicts[tbl2] if v not in all_dicts[tbl1]]
    else:
        if tbl1:
            comp1 = [[v, all_dicts[tbl1].get(v)] for v in all_dicts[tbl1]]
        if tbl2:
            comp2 = [[v, all_dicts[tbl2].get(v)] for v in all_dicts[tbl2]]
    return comp1, comp2
