#import packages
import praw
import os
import json
import csv
import time
from datetime import datetime
import ticker_scrape
import re
import prices
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class RedditChecker:

    main_dir = './data/reddit_stocks'
    #Client edits these parameters
    #============================================
    with open('reddit_credentials.json', 'r') as creds_file:
        creds = json.load(creds_file)
        client_id = creds['client_id']
        client_secret = creds['client_secret']
    def __init__(self):
        self.reddit = praw.Reddit(client_id=self.client_id,
                                  client_secret=self.client_secret,
                                  user_agent='wsb_bot')
    #============================================

    ticker_scrape.get_tickers()
    print('Tickers scraped')
    #Initialize known stocks (NYSE, AMEX, NASDAQ)
    ################################################
    nyse_df = pd.read_csv(f'{main_dir}/exchange_csvs/NYSE.csv')
    amex_df = pd.read_csv(f'{main_dir}/exchange_csvs/AMEX.csv')
    nasdaq_df = pd.read_csv(f'{main_dir}/exchange_csvs/NASDAQ.csv')

    nyse_stocks = list(nyse_df['symbol'])
    amex_stocks = list(amex_df['symbol'])
    nasdaq_stocks = list(nasdaq_df['symbol'])

    all_stocks = list(set(nyse_stocks + amex_stocks + nasdaq_stocks))
    # **
    blocklist = ['EPS', 'WSB', 'OEM', 'ATM', 'GDP', 'RGB', 'LFG']
    for stock in blocklist:
        try:
            all_stocks.remove(f'{stock}')
        except:
            pass

    #reddit instance
    reddit = praw.Reddit(client_id = client_id, client_secret = client_secret, user_agent = 'Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0')
    subreddit = None
    new_posts = set()
    #store post id to avoid duplicates
    post_id = None
    old_posts = set()
    def run(self):
        while True:
            # datetime object containing current date and time
            now = datetime.now()
            #print("now =", now)
            # dd/mm/YY H:M:S
            dt_string = now.strftime("%m-%d-%Y-%H_%M")
            current_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
            #print("date and time =", dt_string)
            #define how many posts to show each refresh
            self.subreddit = self.reddit.subreddit('WallStreetBets')
            self.new_posts = self.subreddit.hot(limit = 50)
            #btc_res = requests.get(btc_url, headers=headers)
            #content = BeautifulSoup(btc_res.text, 'lxml')
            #print(content)
            #btc_price = content.find('input', {'class' : 'newInput inputTextBox alertValue'})['value']
            #print(btc_price)
            price_item = prices.get_indicies()
            for post in self.new_posts:
                stocks = []
                downvotes = int(float(post.ups)/float(post.upvote_ratio) - post.ups)
                p_time = int(post.created_utc)
                p_time = datetime.utcfromtimestamp(p_time).strftime('%Y-%m-%d %H:%M:%S')
                post_text = post.title.replace('.', '').replace('$', '').replace('!', '')
                potential_stocks = re.findall(r'\b[A-Z]{3,}\b[.!?]?', post_text)
                if self.all_stocks:
                    for stock in potential_stocks:
                        print(stock)
                        if stock in self.all_stocks:
                            stocks.append(stock)
                item = {
                    "Date" : p_time,
                    "Author" : post.author,
                    "Title" : post.title,
                    "Comments" : len(post.comments),
                    "Upvote Ratio" : post.upvote_ratio,
                    "Tickers" : " ".join(stocks)
                }
                item.update(price_item)
                item.update({
                    "Upvotes" : post.ups,
                    "Downvotes" : downvotes,
                    "Pinned" : post.pinned,
                    "Is Video" : post.is_video,
                    "Num Reports" : post.num_reports,
                    "Link" : post.url,
                    "Date Of Extraction" : current_time_str
            })

                csv_string = f'{dt_string}_wsb.csv'
                self.to_csv(item, csv_string)
            #sleep for 35 minutes
            self.combine_csvs()
            self.plot_csv()
            print('sleeping for 35 minutes...')
            time.sleep(2100)

    def to_csv(self, item, filename):
        # Check if "playlists.csv" file exists
        file_exists = os.path.isfile(f'{self.main_dir}/comment data/{filename}')
        if not os.path.exists(f'{self.main_dir}/comment data'):
            os.makedirs(f'{self.main_dir}/comment data')
        # Append data to CSV file
        with open(f'{self.main_dir}/comment data/{filename}', 'a') as csv_file:
            # Init dictionary writer
            writer = csv.DictWriter(csv_file, fieldnames=item.keys())
            # Write header only ones
            if not file_exists:
                writer.writeheader()
            # Write entry to CSV file
            writer.writerow(item)

    def combine_csvs(self):
        #check if comment data dir exists
        if not os.path.exists(f'{self.main_dir}/comment data/'):
            os.makedirs(f'{self.main_dir}/comment data/')
        #create a list of all the csvs in the comment data folder
        csvs = os.listdir(f'{self.main_dir}/comment data/')
        #create a list of all the dataframes from the csvs
        frames = [pd.read_csv(f'{self.main_dir}/comment data/'+csv, low_memory=False) for csv in csvs]
        #concatenate all the dataframes into one dataframe
        df = pd.concat(frames)
        df = df.drop_duplicates('Link')
        #export the dataframe to a csv
        df.to_csv(f'{self.main_dir}/combined_csvs.csv', index=False)
        print('combined csvs')

    def plot_csv(self):
        df = pd.read_csv(f'{self.main_dir}/combined_csvs.csv')
        pairplot = sns.pairplot(df)
        #heatmap = sns.heatmap(df.corr(), annot=True)
        plt.show()
        if not os.path.exists(f'{self.main_dir}/data_pics/'):
            os.makedirs(f'{self.main_dir}/data_pics/')
        pairplot.savefig(f'{self.main_dir}/data_pics/wsb_pairplot.png')
        sns.heatmap(df.corr(), annot=True).get_figure().savefig(f'{self.main_dir}/data_pics/wsb_heatmap.png')
           

if __name__ == '__main__':
    RedditChecker = RedditChecker()
    RedditChecker.run()
    
