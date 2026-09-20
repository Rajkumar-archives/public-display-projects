# Book Scraper

A Python web scraper that extracts book data (title, price, rating, stock
status) from [books.toscrape.com](https://books.toscrape.com) — a public
sandbox site built specifically for scraping practice — and exports it to
CSV, JSON, or Excel.

This project demonstrates the kind of custom scraper I build for clients:
clean, documented code with error handling, configurable output formats,
and respectful request pacing.

## Features

- Scrapes any number of catalogue pages
- Extracts title, price, star rating, and stock availability
- Exports to **CSV**, **JSON**, or **Excel (.xlsx)**
- Basic error handling (network failures won't crash the whole run)
- Polite scraping (delay between requests)

## Requirements

- Python 3.10+
- `requests`, `beautifulsoup4`, `openpyxl`

Install dependencies:

```bash
pip install requests beautifulsoup4 openpyxl
```

## Usage

```bash
# Scrape 3 pages, save as CSV (default)
python scraper.py --pages 3

# Scrape 5 pages, save as JSON
python scraper.py --pages 5 --format json

# Save as Excel
python scraper.py --pages 3 --format excel
```

## Example output (CSV)

| title                                  | price | rating | in_stock |
|-----------------------------------------|-------|--------|----------|
| A Light in the Attic                    | 51.77 | 3      | True     |
| Tipping the Velvet                      | 53.74 | 1      | True     |
| Sapiens: A Brief History of Humankind   | 54.23 | 5      | True     |

## How it works

1. `fetch_page()` requests a single catalogue page and parses it with
   BeautifulSoup.
2. `parse_books()` extracts each book's data from the page's HTML structure.
3. `scrape()` loops over the requested number of pages, handling request
   failures gracefully instead of crashing.
4. Results are written out with `save_csv()`, `save_json()`, or
   `save_excel()`.

## Notes

This scrapes a site built for practicing web scraping, so it's safe to run
freely. For real-world projects, I adapt this same structure to any target
site — including sites requiring pagination, login, or JavaScript rendering
(via Selenium).

---

*Built as a portfolio example. Available for custom scraping work on
[Fiverr].*
