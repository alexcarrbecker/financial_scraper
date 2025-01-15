import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import feedparser
import logging
import json
from urllib.parse import quote

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

CONFIG_FILE = "config.json"

def fetch_news(company_name, num_articles=10):
    """Fetch news articles from Google News RSS."""
    try:
        # Encode the company name for the URL
        encoded_company_name = quote(company_name)
        rss_url = f"https://news.google.com/rss/search?q={encoded_company_name}+stock+OR+financial+OR+earnings"
        feed = feedparser.parse(rss_url)
        
        if not feed.entries:
            logging.warning("No articles found for the given company.")
            return []

        news_data = []
        for entry in feed.entries[:num_articles]:
            news_data.append({
                "Title": entry.title,
                "Link": entry.link,
                "Snippet": BeautifulSoup(entry.summary, "html.parser").text,  # Remove HTML tags
                "Date Published": format_date(entry.published),
            })

        return news_data

    except Exception as e:
        logging.error(f"Error fetching news: {e}")
        return []

def format_date(date_str):
    """Format date string to a more readable format."""
    try:
        date_obj = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %Z")
        return date_obj.strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        logging.warning(f"Unable to format date: {date_str}")
        return date_str

def fetch_stock_data(company_symbol, api_key):
    """Fetch stock data using a public API."""
    try:
        # Encode the company symbol for the URL
        encoded_company_symbol = quote(company_symbol)
        api_url = f"https://finnhub.io/api/v1/quote?symbol={encoded_company_symbol}&token={api_key}"
        response = requests.get(api_url)
        response.raise_for_status()

        data = response.json()
        stock_info = {
            "Current Price": data.get("c"),
            "High Price": data.get("h"),
            "Low Price": data.get("l"),
            "Open Price": data.get("o"),
            "Previous Close": data.get("pc"),
        }

        return stock_info

    except Exception as e:
        logging.error(f"Error fetching stock data: {e}")
        return {}


def save_to_csv(data, folder, filename, company_name):
    """Save data to a CSV file in the specified folder with company name in the filename."""
    if not data:
        print("No data to save.")
        return
    
    # Ensure the folder exists
    os.makedirs(folder, exist_ok=True)

    # Add company name to the filename
    company_filename = f"{company_name.replace(' ', '_').lower()}_{filename}"
    file_path = os.path.join(folder, company_filename)

    if os.path.exists(file_path):
        overwrite = input(f"File '{company_filename}' already exists in '{folder}'. Overwrite? (yes/no): ").strip().lower()
        if overwrite != "yes":
            print("File not overwritten.")
            return
    
    try:
        df = pd.DataFrame(data)
        df.to_csv(file_path, index=False)
        print(f"Data saved to {file_path}")
    except Exception as e:
        logging.error(f"Error saving to CSV: {e}")

def get_api_key():
    """Retrieve API key from config file or prompt the user to input one."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
        if "api_key" in config:
            return config["api_key"]
    
    # Prompt user for API key if not found
    api_key = input("Enter your finnhub.io API key: ").strip()
    save_api_key(api_key)
    return api_key

def save_api_key(api_key):
    """Save API key securely to a configuration file."""
    config = {"api_key": api_key}
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)
    print("API key saved for future use.")

def main():
    print("Welcome to the Financial Info Scraper!")
    company_name = input("Enter the company name to fetch news about: ").strip()
    folder_name = company_name.replace(" ", "_").lower()
    num_articles = int(input("Enter the number of articles to fetch (default 10): ") or 10)
    
    # Fetch news
    print("Fetching news...")
    news_data = fetch_news(company_name, num_articles)
    
    if news_data:
        print(f"Fetched {len(news_data)} articles:")
        for article in news_data:
            print(f"- {article['Title']} ({article['Date Published']})\n  {article['Link']}")
        
        save_to_csv(news_data, folder=folder_name, filename="news_data.csv", company_name=company_name)
    else:
        print("No news articles found.")

    # Fetch stock data
    fetch_stock = input("Would you like to fetch stock data? (yes/no): ").strip().lower()
    if fetch_stock == "yes":
        company_symbol = input("Enter the company's stock symbol: ").upper()
        api_key = get_api_key()
        stock_data = fetch_stock_data(company_symbol, api_key)
        
        if stock_data:
            print("Stock Data:")
            for key, value in stock_data.items():
                print(f"{key}: {value}")
            save_to_csv([stock_data], folder=folder_name, filename="stock_data.csv", company_name=company_name)

if __name__ == "__main__":
    while True:
        main()
        repeat = input("\nWould you like to search for another company? (yes/no): ").strip().lower()
        if repeat != "yes":
            print("Goodbye!")
            input("\nPress Enter to exit...")
            break
