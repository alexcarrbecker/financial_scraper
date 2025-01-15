Financial Info Scraper

Description:

The Financial Info Scraper is a Python script that fetches financial news and stock data for a specified company. It uses the Google News RSS feed for news articles and the Finnhub API for stock data.
The program saves the fetched data into a folder named after the company. Files include the company name in the filenames for better organization. It also handles API key storage securely for future use.

Features:

  Fetches up-to-date financial news about a company.
  
  Retrieves real-time stock data using the Finnhub API.
  
  Saves data into a folder named after the company.
  
  Prevents overwriting files by prompting the user.
  
  Stores the Finnhub API key securely for future runs.
  

Input Details:

  Enter the company name to fetch financial news.
  
  Specify the number of news articles to fetch (optional).
  
  Choose whether to fetch stock data.
  
  If fetching stock data, enter the stock symbol (e.g., AAPL for Apple).
  
  If an API key is not found, input your Finnhub API key when prompted.
  

Check Saved Data:

  The script creates a folder with the company name.
  
  News data and stock data are saved as CSV files in the folder.
  
