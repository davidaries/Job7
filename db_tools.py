import random
from icecream import ic
all_dicts={}

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
    # ic(all_dicts)
    tbl_names = get_table_names(conn)
    values = []
    for tbl in tbl_names:
        for d in all_dicts.get(tbl):
            if str(all_dicts.get(tbl).get(d).lower()).__contains__(val.lower()):
                values.append((tbl,d, all_dicts.get(tbl).get(d)))
    return values
    # ex = '''SELECT vocab,term,other FROM English_words WHERE term = %s'''%'~0897926'
    # data = conn.execute(ex)
    # for d in data:
    #     print(d)

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
    vocab = generate_vocab(conn)
    other = 'NA'
    vals_en = '''('%s','%s','%s')''' % (vocab, term, other)
    addition_en = '''INSERT INTO %s (vocab, term, other)VALUES %s''' % (tbl, vals_en)
    conn.execute(addition_en)
    conn.commit()