# WallStreetBetsScraper



## Macroaxis Watchlist Integration (Optimize Portfolio based on scraped tickers)

![Macroaxis Screenshot](https://raw.githubusercontent.com/jarrettdev/WallStreetBetsScraper/main/resources/Macroaxis_Portfolios.png)



## https://macroaxis.com
## Video Tutorial
https://www.youtube.com/watch?v=0jGBwrQRhtg



## Exploratory Data Analysis
![alt text](https://raw.githubusercontent.com/jarrettdev/WallStreetBetsScraper/main/data/reddit_stocks/data_pics/wsb_pairplot.png)
![alt text](https://raw.githubusercontent.com/jarrettdev/WallStreetBetsScraper/main/data/reddit_stocks/data_pics/wsb_heatmap.png)

## How to run

Sign up for a Macroaxis account.

python -m venv venv



source venv/bin/activate



(source ./venv/Scripts/activate on windows)



pip install -r requirements.txt

Place your reddit api credentials in reddit_credentials.json

https://www.jcchouinard.com/get-reddit-api-credentials-with-praw/

python reddit_stocks_comment_watch.py



## Where is the data stored?

csvs - data/reddit_stocks



visualizations - data/reddit_stocks/data_pics



list of tickers on all exchanges - data/reddit_stocks/exchange_csvs

