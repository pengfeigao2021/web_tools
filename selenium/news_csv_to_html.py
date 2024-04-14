import pandas as pd
import os
import glob

DATA_DIR = '/Users/AlexG/data/selenium'

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
    

def csv2html(files, html_path):
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
        
        list_content = '''
        <ol>
        {}
        </ol>
        '''.format(
            '\n'.join(
                f'<li><a href={url}>{title}</a></li>' for 
                title, url in zip(titles, urls)))

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
    <title>News</title>
    </head>
    <body>
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
    csvs = glob.glob(f'{DATA_DIR}/*.csv')
    html_path = f'{DATA_DIR}/news.html'
    csv2html(csvs, html_path)
    print('done')

# init guard
if __name__ == "__main__":
    main()