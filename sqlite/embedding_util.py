import numpy as np
import json
import sqlite3

dbpath = '/Users/AlexG/Documents/GitHub/web_tools/sqlite/title_embedding.db'
def write():
    con = sqlite3.connect('/Users/AlexG/Documents/GitHub/web_tools/sqlite/example.db')
    cur = con.cursor()

    # Create table
    # cur.execute('''CREATE TABLE stocks
    #             (date text, trans text, symbol text, qty real, price real)''')

    # Insert a row of data
    # cur.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
    cur.execute("INSERT INTO stocks VALUES (?,?,?,?,?)", ('2024-04-24','SELL','RHAT',1,0.1357))

    # Save (commit) the changes
    con.commit()

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    con.close()

def read():
    con = sqlite3.connect('/Users/AlexG/Documents/GitHub/web_tools/sqlite/example.db')
    cur = con.cursor()

    cur.execute('select * from stocks')
    res = cur.fetchall()
    print(res)
    # Create table
    # cur.execute('''CREATE TABLE stocks
    #             (date text, trans text, symbol text, qty real, price real)''')

    # # Insert a row of data
    # cur.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

    # # Save (commit) the changes
    # con.commit()

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    con.close()

def create_table(path=dbpath):
    con = sqlite3.connect(path)
    cur = con.cursor()

    # Create table
    cur.execute('''CREATE TABLE title_embedding
                (title text, version text, embedding blob)''')
    con.commit()
    cur.close()

def write(title, embedding, version="0", path=dbpath):
    con = sqlite3.connect(path)
    cur = con.cursor()

    # Insert a row of data
    embdata = np.array(embedding, dtype=np.float64).tobytes()
    cur.execute("INSERT INTO title_embedding VALUES (?,?,?)", 
                (title, version, embdata))

    # Save (commit) the changes
    con.commit()

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    con.close()

def array2bytes():
    arr = np.linspace(0, 1, 100)
    # print(arr)
    byte_arr = arr.tobytes()
    print(type(byte_arr))
    # print byte array byte_arr
    # print(byte_arr)

    print('sizes:')
    print('np: ', arr.size, arr.dtype, arr.itemsize)
    print(len(byte_arr))
    text = json.dumps(arr.tolist())
    # print(text)
    print(len(text))
    print(len(text.encode('utf-8')))

def read_embedding(title, version="0", path=dbpath):
    con = sqlite3.connect(path)
    cur = con.cursor()
    cur.execute('select * from title_embedding where title=? and version=?', (title, version))
    res = cur.fetchall()
    con.close()
    return [(v[0], v[1], np.frombuffer(v[2])) for v in res]

def read_all_embedding(version="0", path=dbpath):
    con = sqlite3.connect(path)
    cur = con.cursor()
    cur.execute('select * from title_embedding where version=?', (version,))
    res = cur.fetchall()
    con.close()
    return [(v[0], v[1], np.frombuffer(v[2])) for v in res]
    

if __name__ == '__main__':
    # create_table()
    # res = read_embedding('hello1', path='/Users/AlexG/Documents/GitHub/web_tools/sqlite/example.db')
    res = read_all_embedding()
    print(len(res))
    # print([v[0] for v in res])
    print(res[0][2])
    print(len(res[0][2]))