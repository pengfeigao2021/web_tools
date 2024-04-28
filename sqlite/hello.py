import numpy as np
import json
import sqlite3

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

def write_emb():
    con = sqlite3.connect('/Users/AlexG/Documents/GitHub/web_tools/sqlite/example.db')
    cur = con.cursor()

    # Create table
    cur.execute('''CREATE TABLE title_embedding
                (title text, version text, embedding blob)''')

    # Insert a row of data
    cur.execute("INSERT INTO title_embedding VALUES (?,?,?)", 
                ("hello", "0", np.random.rand(100).tobytes()))

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


def read_emb():
    con = sqlite3.connect('/Users/AlexG/Documents/GitHub/web_tools/sqlite/example.db')
    cur = con.cursor()

    cur.execute('select * from title_embedding')
    res = cur.fetchall()
    print(res)
    for row in res:
        print(row[0])
        print(row[1])
        print(np.frombuffer(row[2]))
    con.close()
    
# write()
# write_emb()
# read()
read_emb()
# array2bytes()