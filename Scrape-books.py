import requests
from bs4 import BeautifulSoup
import json
import time
from urllib.parse import urljoin

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"
START_URL = "https://books.toscrape.com/index.html"

def scrape_books():
    books_data = []
    page = 1
    
    # Custom headers to look like a real browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    print(" Starting practice scraping task...")

    while True:
        url = BASE_URL.format(page)
        print(f" Scraping Page {page}...")
        response = requests.get(url, headers=headers)
        
        # If page doesn't exist (status code 404), we reached the end
        if response.status_code != 200:
            print("Reached the last page or encountered an error. Stopping.")
            break
            
        soup = BeautifulSoup(response.content, "html.parser")
        books = soup.find_all("article", class_="product_pod")
        
        if not books:
            break
            
        for book in books:
            # Extract basic info from the thumbnail view
            title = book.h3.a["title"]
            price = book.find("p", class_="price_color").text
            availability = book.find("p", class_="availability").text.strip()
            
            # Extract rating class (e.g., "star-rating Three")
            rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
            rating_classes = book.find("p", class_="star-rating")["class"]
            rating = rating_classes[1] if len(rating_classes) > 1 else "None"
            rating = rating_map.get(rating, 0)
            
            # Construct absolute URL for book details if needed
            relative_url = book.h3.a["href"]
            source_url = urljoin(START_URL, relative_url)
            
            books_data.append({
                "title": title,
                "price": price,
                "rating": rating,
                "availability": availability,
                "source_url": source_url
            })
            
        # Polite delay to avoid overloading the sandbox server
        time.sleep(0.5)
        page += 1

    # Save to JSON format as requested
    output_file = "books_dataset.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(books_data, f, ensure_ascii=False, indent=4)
        
    print(f" Successfully scraped {len(books_data)} books and saved to {output_file}!")

if __name__ == "__main__":
    scrape_books()