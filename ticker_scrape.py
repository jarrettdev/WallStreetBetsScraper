import requests
import csv
import os
headers = {"User-Agent" : "Mozilla/5.0 CK={} (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko"}
exchanges = ['NYSE','AMEX','NASDAQ']
main_dir = './data/reddit_stocks'

def get_tickers():
    print('grabbing tickers')
    #Check if directory exists
    if not os.path.exists(f'{main_dir}/exchange_csvs'):
        os.makedirs(f'{main_dir}/exchange_csvs')
    for exchange in exchanges:
        res = requests.get(f'https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=25&offset=0&exchange={exchange}&download=true', headers=headers)
        print(res)
        json_data = res.json()
        rows = json_data["data"]["rows"]
        with open(f"{main_dir}/exchange_csvs/{exchange}.csv", 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames = json_data["data"]["headers"].keys())
            writer.writeheader()
            writer.writerows(rows)
