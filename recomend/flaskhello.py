from flask import Flask
from flask import request
import os
import pandas as pd

app = Flask(__name__)

def load_dislike(path='/Users/AlexG/Documents/GitHub/web_tools/recomend/data/dislike.csv'):
    if os.stat(path).st_size == 0:
        print('empty csv file')
        return None
    df = pd.read_csv(path)
    return df

def write_dislike(df, path='/Users/AlexG/Documents/GitHub/web_tools/recomend/data/dislike.csv'):
    df.to_csv(path, index=False)

def add_dislike_to_csv(dislike, path='/Users/AlexG/Documents/GitHub/web_tools/recomend/data/dislike.csv'):
    df = load_dislike(path)
    # add row to df
    if df is not None:
        df = df.append({'title': dislike}, ignore_index=True)
    else:
        df = pd.DataFrame({'title': (dislike,)})
    write_dislike(df, path)
    
@app.route("/adddislike", methods=('POST',))
def add_dislike():
    # load post data
    post_data = request.form['title']
    add_dislike_to_csv(post_data)

    # write to file
    return "<p>add dislike: {}</p>".format(post_data)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"