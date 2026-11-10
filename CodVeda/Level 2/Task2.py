# -- WEB SCRAPER --
# Scrapes quotes, authors, and tags from quotes.toscrape.com
# and saves them to a CSV file.

import requests                        # type: ignore # sends HTTP requests to get web pages
from bs4 import BeautifulSoup          # type: ignore # parses HTML so we can search through it
import csv                             # reads and writes CSV files


BASE_URL = "http://quotes.toscrape.com"   # the website we're scraping
OUTPUT   = "quotes.csv"                   # the file we'll save results to


# ── STEP 1: FETCH THE PAGE ────────────────────────────────────────────────────

def get_page(url):
    # requests.get() sends a GET request to the URL, just like a browser does.
    # The response object contains the page's HTML, status code, and more.
    try:
        response = requests.get(url, timeout=10)
        # timeout=10 means: give up if the server doesn't respond within 10 seconds.
        # Without this, the program could hang forever on a slow/dead server.

        # raise_for_status() checks if the request succeeded.
        # If the server returned a 404 (not found) or 500 (server error),
        # it raises an exception so we handle it instead of silently getting bad data.
        response.raise_for_status()

        return response.text
        # .text gives us the raw HTML of the page as a plain Python string.

    except requests.exceptions.RequestException as e:
        # This catches ALL network-related errors:
        # - No internet connection
        # - Bad URL / domain doesn't exist
        # - Server returned 404, 500, etc.
        # - Timeout
        print(f"Error fetching {url}: {e}")
        return None   # return None so the rest of the program knows it failed


# ── STEP 2 & 3: PARSE HTML AND EXTRACT DATA ───────────────────────────────────

def scrape_quotes(html):
    # BeautifulSoup takes raw HTML text and builds a tree we can search.
    # 'html.parser' is Python's built-in HTML parser — no extra install needed.
    soup = BeautifulSoup(html, 'html.parser')

    # The website wraps each quote in a <div class="quote">.
    # find_all() returns a list of ALL elements matching that description.
    quote_blocks = soup.find_all('div', class_='quote')

    quotes = []   # we'll collect each quote as a dictionary in this list

    for block in quote_blocks:
        # Inside each quote block:
        # - The quote text is in a <span class="text">
        # - The author is in a <small class="author">
        # - Tags are in <a class="tag"> elements (could be many)

        text   = block.find('span', class_='text').get_text()
        # .find() gets the FIRST matching element inside this block.
        # .get_text() strips the HTML tags and returns just the visible text.

        author = block.find('small', class_='author').get_text()

        tag_elements = block.find_all('a', class_='tag')
        # find_all() returns a list here because there are multiple tags per quote.
        # We join them into one comma-separated string for the CSV.
        tags = ', '.join(tag.get_text() for tag in tag_elements)

        # Each quote becomes a dictionary with three keys.
        # This makes it easy to write to CSV with column names later.
        quotes.append({
            'text':   text,
            'author': author,
            'tags':   tags
        })

    return quotes


# ── STEP 4: SAVE TO CSV ────────────────────────────────────────────────────────

def save_to_csv(quotes, filename):
    try:
        # Open the file in write mode ('w').
        # newline='' prevents extra blank lines on Windows.
        # encoding='utf-8' handles special characters (like curly quotes).
        file = open(filename, 'w', newline='', encoding='utf-8')

        # DictWriter creates a CSV writer that works with dictionaries.
        # fieldnames sets the column headers — they must match the dict keys exactly.
        writer = csv.DictWriter(file, fieldnames=['text', 'author', 'tags'])

        writer.writeheader()
        # writeheader() writes the first row: text, author, tags

        writer.writerows(quotes)
        # writerows() loops through our list and writes one row per quote.

        file.close()
        print(f"Saved {len(quotes)} quotes to '{filename}'.")

    except IOError as e:
        # IOError covers problems writing to disk:
        # - No permission to write in this folder
        # - Disk is full
        print(f"Error saving file: {e}")


# ── MAIN ───────────────────────────────────────────────────────────────────────

def main():
    print(f"Scraping {BASE_URL} ...")

    html = get_page(BASE_URL)

    if html is None:
        # get_page() already printed the error — just stop here.
        return

    quotes = scrape_quotes(html)

    if len(quotes) == 0:
        print("No quotes found. The site structure may have changed.")
        return

    print(f"Found {len(quotes)} quotes.")
    save_to_csv(quotes, OUTPUT)


if __name__ == '__main__':
    main()