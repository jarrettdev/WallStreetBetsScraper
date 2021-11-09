import requests
from bs4 import BeautifulSoup

def get_indicies():
    base_url = 'https://www.investing.com/indices/usa-indices'

    headers = {
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0"
    }

    res = requests.get(base_url, headers=headers)

    dow_last = None
    dow_pt_change = None
    dow_pct_change = None
    nasdaq_last = None
    nasdaq_pt_change = None
    nasdaq_pct_change = None
    sp_500_last = None
    sp_500_pt_change = None
    sp_500_pct_change = None

    content = BeautifulSoup(res.text, 'lxml')

    table_whole = content.find('table')

    body = table_whole.find('tbody')

    rows = body.findAll('td')
    #print([row.text for row in rows])
    if 'dow' in rows[1].text.lower():
        dow_last = rows[2].text
        dow_pt_change = rows[5].text
        dow_pct_change = rows[6].text
    if 'nasdaq' in rows[19].text.lower():
        nasdaq_last = rows[20].text
        nasdaq_pt_change = rows[23].text
        nasdaq_pct_change = rows[24].text
    if 's&p' in rows[28].text.lower():
        sp_500_last = rows[29].text
        sp_500_pt_change = rows[32].text
        sp_500_pct_change = rows[33].text
    '''
    print(f'Dow_last : {dow_last} | Dow_point_change : {dow_pt_change} | dow_percent_change : {dow_pct_change}')
    print(f'nasdaq_last : {nasdaq_last} | nasdaq_point_change : {nasdaq_pt_change} | nasdaq_percent_change : {nasdaq_pct_change}')
    print(f'sp_500_last : {sp_500_last} | sp_500_point_change : {sp_500_pt_change} | sp_500_percent_change : {sp_500_pct_change}')
    '''
    
    #print(rows)


    items = {
        "DOW Last" : dow_last,
        "DOW Pt Change" : dow_pt_change,
        "DOW Pct Change" : dow_pct_change,
        "NASDAQ Last" : nasdaq_last,
        "NASDAQ Pt Change" : nasdaq_pt_change,
        "NASDAQ Pct Change" : nasdaq_pct_change,
        "S&P 500 Last" : sp_500_last,
        "S&P 500 Pt Change" : sp_500_pt_change,
        "S&P 500 Pct Change" : sp_500_pct_change
    }

    return items

get_indicies()
