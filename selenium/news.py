import pdb
import glob
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

DATA_DIR = '/Users/AlexG/data/selenium'
NEWS = (
    ('https://news.ycombinator.com/', 'hackernews'),
    ('https://www.reddit.com/', 'reddit'),
    ('https://www.engadget.com/', 'engadget'),
    ('https://www.wired.com/', 'wired'),
    ('https://www.bbc.com/news', 'bbc'),
    ('https://www.npr.org/sections/news/', 'npr'),
    ('https://www.theverge.com/', 'theverge'),
    ('https://www.technologyreview.com/', 'technologyreview'),
    ('https://www.techradar.com/', 'techradar'),
)

# driver = webdriver.Chrome()
driver = webdriver.Firefox()
# get current date in "YYYY-MM-DD" format
today = pd.to_datetime('today').strftime('%Y-%m-%d')

for url, n in NEWS:
    driver.get(url)

    # Find all hrefs in the page
    divs = driver.find_elements(By.TAG_NAME, "a")
    doc_urls = []
    doc_url_titles = []
    exceptions = []
    for div in divs:
        try:
            # filter short div.text 
            if div.text is None or len(div.text.split(' ')) <= 3:
                continue
            doc_urls.append(div.get_attribute("href"))
            doc_url_titles.append(div.text)
        except Exception as e:
            print(e)
            exceptions.append(e)

    # number of exceptions
    print(f"Number of exceptions: {len(exceptions)}")

    # Create a pandas dataframe
    df = pd.DataFrame({'url': doc_urls, 'title': doc_url_titles})
    csv_path = f"{DATA_DIR}/{n}_{today}.csv"
    df.to_csv(csv_path, index=False)

# close driver
driver.close()

# summarize to html
import news_csv_to_html
files = glob.glob(f"{DATA_DIR}/*{today}*.csv")
html_path = f"{DATA_DIR}/news_{today}.html"
news_csv_to_html.csv2html(files, html_path)