import random
from icecream import ic
import json

all_dicts = {}
tbl_special = []
cat_test = {}


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
        values.extend([(tbl, d, get_vocab(tbl, d)) for tbl in tbl_names for d in all_dicts.get(tbl)])
    else:
        for tbl in tbl_names:
            if tbl not in tbl_special:
                if val[0] != '~':
                    for d in all_dicts.get(tbl):
                        ic(get_vocab(tbl, d))
                        if str(get_vocab(tbl, d).lower()).__contains__(str(val).lower()):
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
    syns = [v[0] for v in all_dicts['English_synonyms'] if val.lower() in [v[1].lower()]]
    values.extend([('English_words', s, get_vocab('English_words', s)) for s in syns])
    return values


def load_db_data(conn):
    """loads all of the values in the current database and create a dictionary of dictionaries of those values
    :param conn: connection to the database
    :type conn: sqlite3.Connection"""
    all_dicts.clear()
    tbl_names = get_table_names(conn)
    tbl_special.append(tbl_names.pop(tbl_names.index('Categories')))
    tbl_special.append(tbl_names.pop(tbl_names.index('English_synonyms')))
    for tbl in tbl_names:
        ex = "SELECT * from %s" % tbl
        vals = conn.execute(ex)
        lang_dict = {}
        for v in vals:
            if v[2]:
                lang_dict[v[0]] = process_blob(v)
            else:
                lang_dict[v[0]] = v[1]
        all_dicts[tbl] = lang_dict

    for tbl in tbl_special:
        ex = "SELECT * from %s" % tbl
        vals = conn.execute(ex)
        lang_dict = {}
        for v in vals:
            ic(v)
            if v[0] in lang_dict.keys():
                lang_dict[v[0]].append(v[1])
            else:
                lang_dict[v[0]] = [v[1]]
        ic(lang_dict)
        all_dicts[tbl] = lang_dict


def get_remaining_categories(vocab):
    dic = 'English_words'
    existing_cats = []
    if vocab in all_dicts['Categories'].keys():
        existing_cats = all_dicts['Categories'].get(vocab)
    cats = [(c, all_dicts[dic][c][0]) for c in all_dicts[dic]
            if type(all_dicts[dic][c]) is list and all_dicts[dic][c][1].get('category') and c not in existing_cats]
    ic(existing_cats, cats)
    return cats


def add_category_to_db(value, conn):
    dic = 'English_words'
    list_vals = [get_vocab(dic, v).lower() for v in all_dicts[dic].keys()]
    other = '''{"category": true}'''
    if value.get().lower() not in list_vals:
        vocab = generate_vocab(conn)
        addition_en = '''INSERT INTO %s (vocab, term, other)VALUES %s''' % (dic, (vocab, value.get(), other))
        all_dicts[dic][vocab]= [value.get(), other]
    else:
        vocab = [v for v in all_dicts[dic].keys() if get_vocab(dic, v).lower() == value.get()][0]
        if list(all_dicts[dic][vocab]):
            return 'already in'
        addition_en = '''UPDATE %s SET other = '%s' WHERE vocab = '%s' ''' % (dic, other, vocab)
        pblob = process_blob((vocab, value.get(), other))
        ic(pblob)
        all_dicts[dic][vocab] = pblob
    conn.execute(addition_en)
    conn.commit()
    return 'added to'

def add_other(conn, dic, vocab, value):
    ic(dic, vocab, value.get())
    if value.get().__contains__('~'):
        value = '~' + value.get().split('~')[1][0:7]
        ic(value)
    else:
        value = value.get()
    ic(value,vocab)
    if vocab in all_dicts[dic].keys():
        ic(all_dicts[dic][vocab])
        if value.lower() not in [v.lower() for v in all_dicts[dic][vocab]]:
            addition_en = '''INSERT INTO %s (vocab, term)VALUES %s''' % (dic, (vocab, value))
            conn.execute(addition_en)
            conn.commit()
            all_dicts[dic][vocab].append(value)
        else:
            return 'already in'
    else:
        addition_en = '''INSERT INTO %s (vocab, term)VALUES %s''' % (dic, (vocab, value))
        conn.execute(addition_en)
        conn.commit()
        all_dicts[dic][vocab] = [value]
    return 'added to'


def get_vocab(dic, vocab):
    """returns a specific ~vocab value from a specific dictionary
    :return: the value described above
    :rtype: str"""
    if type(all_dicts[dic].get(vocab)) is list and dic not in tbl_special:
        return all_dicts[dic].get(vocab)[0]
    else:
        return all_dicts[dic].get(vocab)


def add_to_db(conn, add_values):
    """adds values to the database and the dictionary used by the db interactor
    :param conn: connection to the database
    :type conn: sqlite3.Connection
    :param add_values: The value to be added to the database
    :type add_values: dict
    :return: a list of all of the values not added to the db and the dictionary
    :rtype: list
    """
    ic(add_values)
    vocab = generate_vocab(conn)
    keys = add_values.keys()
    to_process = []
    for k in keys:
        if add_values.get(k).get().lower() not in [get_vocab(k, v).lower() for v in all_dicts[k]]:
            to_process.append([True, k, add_values[k].get()])
        else:
            to_process.append([False, k, add_values[k].get()])
    unprocessed = []
    for p in to_process:
        if p[0]:
            vals_en = '''('%s','%s')''' % (vocab, p[2])
            addition_en = '''INSERT INTO %s (vocab, term)VALUES %s''' % (p[1], vals_en)
            conn.execute(addition_en)
            conn.commit()
            all_dicts.get(p[1])[vocab] = p[2]
        else:
            unprocessed.append([p[1], p[2]])
    return unprocessed


def process_blob(val):

    converted = json.loads(val[2])
    ic(val, [val[1], converted])
    return [val[1], converted]


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
