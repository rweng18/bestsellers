import requests
from bs4 import BeautifulSoup as BS

def get_list_urls(url):
    try:
        print('You are trying to parse a Wiki page.')
        page = requests.get(url)
        content = BS(page.content, 'html.parser')

    except:
        print('You failed to parse page')

    # Get all URLs to lists of NYTimes Fiction Bestsellers lists
    urls = content.find_all('a', href = True)
    links = [url['href'] for url in urls if url['href'].startswith('/wiki/The') and 'Fiction' in url['href']]
    all_urls = sorted(list(set(links)))

    return all_urls


def parse_table(bestseller_url):

    url = "https://en.wikipedia.org" + bestseller_url

    try:
        print('You are trying to parse a Wiki page.')
        page = requests.get(url)
        content = BS(page.content, 'html.parser')
    except:
        print('You failed to parse the wiki.')

    books = {}
    for row in table_rows:

        row_content = row.find_all('td')
        cur_book = ()

        # If full row of information, collect date, title, author
        if len(row_content) == 3:
            date = row_content[0].text.strip()
            title = row_content[1].text.strip()
            author = row_content[2].text.strip()
            key = (title.lower().title(), author)

            # If book in dictionary, add new date, else add new book
            if key in books.keys():
                books[key].append(date)

            else:
                books[key] = [date]

            cur_book = key # save current book in case of multiweek streaks

        # If book was on the list for multiple weeks, add new date
        elif len(row_content) == 1:
            date = row_content[0].text.strip()
            books[key].append(date)

        elif len(row_content) < 3:
            print(row_content)

    return books
