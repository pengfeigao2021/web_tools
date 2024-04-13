import pandas as pd
import os
import glob

DATA_DIR = '/Users/AlexG/data/selenium'

def csv2html(files, html_path):
    news = []
    source_list = []
    for p in files:
        name = os.path.splitext(os.path.basename(p))[0]
        source_list.append(name)
        df = pd.read_csv(p)
        list_content = '''
        <ol>
        {}
        </ol>
        '''.format(
            '\n'.join(
                f'<li><a href={url}>{title}</a></li>' for 
                title, url in zip(df['title'], df['url'])))

        news_content = f'''
        <h2 id="{name}">{name}</h2>
        {list_content}
        '''
        news.append(news_content)
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