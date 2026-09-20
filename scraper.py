"""
Book Scraper
------------
Scrapes book data (title, price, rating, availability) from
books.toscrape.com — a public sandbox site built for scraping practice.

Exports results to CSV, JSON, or Excel.

Usage:
    python scraper.py --pages 3 --format csv
    python scraper.py --pages 5 --format json
    python scraper.py --format excel
"""

import argparse
import csv
import json
import sys
import time
from dataclasses import dataclass, asdict

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"
HEADERS = {"User-Agent": "Mozilla/5.0 (educational scraping demo)"}

RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


@dataclass
class Book:
    title: str
    price: float
    rating: int
    in_stock: bool


def fetch_page(page_number: int) -> BeautifulSoup:
    """Fetch and parse a single catalogue page."""
    url = BASE_URL.format(page_number)
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def parse_books(soup: BeautifulSoup) -> list[Book]:
    """Extract book data from a parsed catalogue page."""
    books = []
    for article in soup.select("article.product_pod"):
        title = article.h3.a["title"]

        price_text = article.select_one(".price_color").text
        price = float(price_text.replace("£", "").strip())

        rating_class = article.select_one("p.star-rating")["class"]
        rating_word = [c for c in rating_class if c != "star-rating"][0]
        rating = RATING_MAP.get(rating_word, 0)

        availability = article.select_one(".instock.availability").text.strip()
        in_stock = "In stock" in availability

        books.append(Book(title=title, price=price, rating=rating, in_stock=in_stock))
    return books


def scrape(num_pages: int) -> list[Book]:
    """Scrape the given number of catalogue pages, with basic error handling."""
    all_books = []
    for page in range(1, num_pages + 1):
        try:
            soup = fetch_page(page)
            page_books = parse_books(soup)
            if not page_books:
                print(f"No books found on page {page} — stopping early.")
                break
            all_books.extend(page_books)
            print(f"Scraped page {page}: {len(page_books)} books")
            time.sleep(0.5)  # be polite to the server
        except requests.RequestException as e:
            print(f"Failed to fetch page {page}: {e}", file=sys.stderr)
            break
    return all_books


def save_csv(books: list[Book], filename: str = "books.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "price", "rating", "in_stock"])
        writer.writeheader()
        for book in books:
            writer.writerow(asdict(book))
    print(f"Saved {len(books)} books to {filename}")


def save_json(books: list[Book], filename: str = "books.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump([asdict(book) for book in books], f, indent=2)
    print(f"Saved {len(books)} books to {filename}")


def save_excel(books: list[Book], filename: str = "books.xlsx"):
    try:
        from openpyxl import Workbook
    except ImportError:
        print("openpyxl not installed — run: pip install openpyxl", file=sys.stderr)
        return
    wb = Workbook()
    ws = wb.active
    ws.title = "Books"
    ws.append(["Title", "Price (£)", "Rating", "In Stock"])
    for book in books:
        ws.append([book.title, book.price, book.rating, book.in_stock])
    wb.save(filename)
    print(f"Saved {len(books)} books to {filename}")


def main():
    parser = argparse.ArgumentParser(description="Scrape book data from books.toscrape.com")
    parser.add_argument("--pages", type=int, default=3, help="Number of catalogue pages to scrape")
    parser.add_argument("--format", choices=["csv", "json", "excel"], default="csv", help="Output format")
    args = parser.parse_args()

    print(f"Starting scrape: {args.pages} page(s), output format = {args.format}")
    books = scrape(args.pages)

    if not books:
        print("No data scraped.", file=sys.stderr)
        sys.exit(1)

    if args.format == "csv":
        save_csv(books)
    elif args.format == "json":
        save_json(books)
    elif args.format == "excel":
        save_excel(books)


if __name__ == "__main__":
    main()
