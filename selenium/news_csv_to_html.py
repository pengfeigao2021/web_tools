import pandas as pd
import os
import tqdm
import sys
import glob

DATA_DIR = '/Users/AlexG/data/selenium'
sys.path.insert(0, '/Users/AlexG/Documents/GitHub/web_tools/text2vec-base-multilingual')
from cossim import CosineSim

def isduplicate(urls, titles, title, url):
    for t in titles:
        if t.lower() == title.lower():
            return True
        if t.lower().startswith(title.lower()):
            return True
    for u, t in zip(urls, titles):
        if u.lower() == url.lower():
            if len(title) < len(t):
                return True
            else:
                return title < t
    return False
    

def load_dislike(path='/Users/AlexG/Documents/GitHub/web_tools/recomend/data/dislike.csv'):
    if os.stat(path).st_size == 0:
        print('empty csv file')
        return None
    df = pd.read_csv(path)
    return df
    
def dislike_sim(model, dislike_embs, s):
    emb = model.get_emb(s)
    score = None
    for t, emb_t in dislike_embs.items():
        sim = model.cosine(emb, emb_t)
        if score is None or sim > score:
            score = sim
    return score
    
def csv2html(files, html_path):
    df_dislike = load_dislike()
    dislike_titles = set()
    dislike_embs = dict()
    if df_dislike is not None:
        dislike_titles = set(df_dislike['title'])
    sim = CosineSim()
    for t in tqdm.tqdm(dislike_titles, total = len(dislike_titles)):
        emb = sim.get_emb(t)
        dislike_embs[t] = emb

    news = []
    source_list = []
    for p in files:
        name = os.path.splitext(os.path.basename(p))[0]
        source_list.append(name)
        df = pd.read_csv(p)

        # remove duplicates
        dup_count = 0
        titles = []
        urls = []
        valid_indices = {i: True for i in range(len(df))}
        for i in range(len(df)):
            title = df.iloc[i]['title']
            url = df.iloc[i]['url']

            # get other titles
            other_titles = [
                df.iloc[j]['title'] 
                for j, v in valid_indices.items() 
                if v and j != i]
            other_urls = [
                df.iloc[j]['url'] 
                for j, v in valid_indices.items() 
                if v and j != i]
            if isduplicate(other_urls, other_titles, title, url):
                valid_indices[i] = False
                dup_count += 1
                continue
            titles.append(title)
            urls.append(url)
        
        # compute and sort by score
        news_contents = []
        for id, vals in enumerate(zip(titles, urls)):
            title, url = vals
            score = -dislike_sim(sim, dislike_embs, title)
            news_contents.append(
                (
                    title,
                    url,
                    score
                )
            )
        news_contents.sort(key=lambda x: x[2], reverse=True)

        list_content = '''
        <table class="pure-table pure-table-horizontal">
        <thead>
            <tr>
                <th>#</th>
                <th>news</th>
                <th>Click</th>
                <th>Views</th>
                <th>Likes</th>
            </tr>
        </thead>
        <tbody>
          {}
        </tbody>
        </table>
        '''.format(
            '\n'.join(
                f'''<tr>
                      <td>{id}</td>
                      <td>
                        <form action="http://127.0.0.1:5000/adddislike" method="POST" style="position: inline;">
                            <a href={vals[1]}>{vals[0]}</a>
                            <input style="visibility: hidden;" name="title" id="say" value="{vals[0]}" />
                            <button>dislike this</button>
                        </form>
                      </td>
                      <td>0</td>
                      <td>{'-{:.3f}'.format(vals[2])}</td>
                      <td>{'-1' if vals[0] in dislike_titles else '0'}</td>
                    </tr>''' for
                    id, vals in enumerate(news_contents)))

        news_content = f'''
        <h2 id="{name}">{name}</h2>
        {list_content}
        '''
        news.append(news_content)
        
        # duplication count
        print(f'{name} has {dup_count} duplicates')

    content = '''
    <html>
    <head>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/purecss@3.0.0/build/pure-min.css" integrity="sha384-X38yfunGUhNzHpBaEBsWLO+A0HDYOQi8ufWDkZ0k9e0eXz/tH3II7uKZ9msv++Ls" crossorigin="anonymous">
        <link rel="stylesheet" href="styles.css">
        <title>News</title>
    </head>
    <body>
        <div class="pure-g">
            <div class="pure-u-1-3 g1"><p>Tech News</p></div>
            <div class="pure-u-1-3 g2"><p>Updated: 2024-04-13</p></div>
            <div class="pure-u-1-3 g3"><p>Views: 0</p></div>
        </div>
        {}
        <br>
        {}
    </body>
    </html>
    '''.format(
        '\n<br>\n'.join('<a href="#{0}">{0}</a>'.format(s) for s in source_list),
        '\n<br>\n'.join(news)
        )

    # write to html file
    with open(html_path, 'w') as fout:
        fout.write(content)
    
def main():
    csvs = glob.glob(f'{DATA_DIR}/*04-25*.csv')
    html_path = f'{DATA_DIR}/news.html'
    csv2html(csvs, html_path)
    print('done')

# init guard
if __name__ == "__main__":
    main()