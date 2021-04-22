def multipleReplace(table, s):
    for key in table:
        s = s.replace(key, table[key])
    return s

