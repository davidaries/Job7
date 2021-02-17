import random
from icecream import ic

all_dicts = {}


def generate_vocab(conn):
    """:param conn: connection to the database
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
    vals = conn.execute("SELECT type, name from sqlite_master")
    tbl_names = []
    for row in vals:
        if row[0] == 'table':
            tbl_names.append(row[1])
    return tbl_names


def search_value(val, conn):
    tbl_names = get_table_names(conn)
    values = []
    if not val: # Check for no input
        for tbl in tbl_names:
            for d in all_dicts.get(tbl):
                values.append((tbl, d, all_dicts.get(tbl).get(d)))
    else:
        for tbl in tbl_names:
            if val[0] != '~':
                for d in all_dicts.get(tbl):
                    if str(all_dicts.get(tbl).get(d).lower()).__contains__(val.lower()):
                        values.append((tbl, d, all_dicts.get(tbl).get(d)))
            else:
                for d in all_dicts.get(tbl):
                    if d == val:
                        values.append((tbl, d, all_dicts.get(tbl).get(d)))
    return values

def load_db_data(conn):
    all_dicts.clear()
    tbl_names = get_table_names(conn)
    for tbl in tbl_names:
        ex = "SELECT * from %s" % tbl
        vals = conn.execute(ex)
        lang_dict = {}
        for v in vals:
            lang_dict[v[0]] = v[1]
        all_dicts[tbl] = lang_dict
    # ic(all_dicts)


def get_vocab(dic, vocab):
    return all_dicts.get(dic).get(vocab)


def add_to_db(conn, tbl, term):
    process = True
    for i in all_dicts.get(tbl):
        if term == all_dicts.get(tbl).get(i).lower():
            process = False
    if process:
        vocab = generate_vocab(conn)
        other = 'NA'
        vals_en = '''('%s','%s','%s')''' % (vocab, term, other)
        addition_en = '''INSERT INTO %s (vocab, term, other)VALUES %s''' % (tbl, vals_en)
        conn.execute(addition_en)
        conn.commit()
        all_dicts.get(tbl)[vocab] = term
    ic(process)
    return process


# check existence in DB func
# compare for missing terms func
def compare(tbl1, tbl2, different):
    comp1 = []
    comp2 = []
    if different == 1 and tbl1 and tbl2:
        for v in all_dicts.get(tbl1):
            if v not in all_dicts.get(tbl2):
                comp1.append((v, all_dicts.get(tbl1).get(v)))
        for v in all_dicts.get(tbl2):
            if v not in all_dicts.get(tbl1):
                comp2.append((v, all_dicts.get(tbl2).get(v)))

    else:
        if tbl1:
            for v in all_dicts.get(tbl1):
                comp1.append((v, all_dicts.get(tbl1).get(v)))
        if tbl2:
            for v in all_dicts.get(tbl2):
                comp2.append((v, all_dicts.get(tbl2).get(v)))
    return comp1, comp2
