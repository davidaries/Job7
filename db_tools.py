import random

def generate_token(conn):
    """:param conn: connection to the database
    :type conn: sqlite3.Connection"""
    used_tokens = []
    vals = conn.execute("SELECT vocab, term, other from English_words")
    for row in vals:
        used_tokens.append(row[0])
    print(used_tokens)
    ran = random.randint(0000000, 9999999)
    if "~%07d" % ran not in used_tokens:
        token = "~%07d" % ran
    else:
        while "~%07d" % ran in used_tokens:
            ran = random.randint(0000000, 9999999)
        token = "~%07d" % ran
    return token

def get_table_names(conn):
    vals = conn.execute("SELECT type, name from sqlite_master")
    tbl_names = []
    for row in vals:
        if row[0] == 'table':
            tbl_names.append(row[1])
    return tbl_names

def search_value(val, conn):
    ex = '''SELECT vocab,term,other FROM English_words WHERE term = %s'''%'~0897926'
    data = conn.execute(ex)
