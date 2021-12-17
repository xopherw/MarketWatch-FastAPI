import requests, bs4
from finance import finance as f

def request(url):
    r = requests.get(url).text
    soup = bs4.BeautifulSoup(r, 'html.parser')
    return soup

class marketwatch:

    def __init__(self, ticker):
        self.ticker = ticker

    def url(self, endpoint=''):
        url = f'https://www.marketwatch.com/investing/stock/{self.ticker}'
        r = request(url + endpoint)
        return r

    def accounting(self, finance, period=''):
        financials = f'/financials/{finance}'
        return self.url(financials + f'/{period}') if (period == 'quarter') else self.url(financials)

    # This is to get basic data like current price, open, close, high, low, volumes etc
    def data(self):
        try:
            # info basically scraped the most information needed except "close" due to MarketWatch website design
            info = [i.get_text() for i in self.url().find_all('span', {'class' : 'primary'})]
            close = [i.get_text() for i in self.url().find_all('td', {'class' : 'table__cell u-semi'})]
            data = {
                    'status'        :   self.url().find_all('div', { 'class' : 'status' })[0].get_text(),
                    'price'         :   round(float(self.url().find_all('bg-quote', { 'class' : 'value' })[0].get_text().replace('$', '').replace(',','')),2),
                    'open'          :   round(float(info[6].replace('$', '').replace(',','')),2) if info[6] != "N/A" else "N/A",
                    'high'          :   round(float(info[3].replace('$', '').replace(',','')),2) if info[3] != "N/A" else "N/A",
                    'low'           :   round(float(info[2].replace('$', '').replace(',','')),2) if info[2] != "N/A" else "N/A",
                    'close'         :   round(float(close[0].replace('$', '').replace(',','')),2) if info[0] != "N/A" else "N/A",
                    'dividend'      :   round(float(info[-5].replace('$', '').replace(',','')),2) if info[-5] != "N/A" else "N/A",
                    'volume'        :   info[1].split(':')[-1].strip() if info[1] != "N/A" else "N/A",
                    'market_cap'    :   info[9] if info[9] != "N/A" else "N/A",
                    'pe_ratio'      :   round(float(info[14]),2) if info[14] != "N/A" else "N/A",
                    'beta'          :   round(float(info[12]),2) if info[12] != "N/A" else "N/A"
            }
            return data
        except requests.ConnectionError:
            return 500
        except:
            return 400

    def financial_data(self, finance, period=''):
        try:
            data = {}

            # Date remain on "income state" since it's just the "period" that changes it
            date = [i.get_text() for i in self.accounting(f.income, period).findAll('th', {'class' : 'overflow__heading'})][1:6]
            width = len(date)

            # Each items, and values list will call it differently due to website design stuctures. If changed, use the "accounting" method to trace it and update.
            if(finance == 'cash'):
                items = [i.get_text() for i in self.accounting(f.cash, period).findAll('div', { 'class' : 'cell__content' })[9::8] if(i.get_text() != 'Item')]
                values = [i.get_text() for i in self.accounting(f.cash, period).findAll( 'span' )[93:385] if (i.get_text() not in ['Financing Activities', 'Investing Activities'])]
            elif(finance == 'balance'):
                items = [i.get_text() for i in self.accounting(f.balance, period).findAll('div', { 'class' : 'cell__content' })[9::8] if(i.get_text() != 'Item')]
                values = [i.get_text() for i in self.accounting(f.balance, period).findAll( 'span' )[93:489] if (i.get_text() not in ["Liabilities & Shareholders' Equity"])]
            else:
                items = [i.get_text() for i in self.accounting(f.income, period).findAll('div', { 'class' : 'cell__content' })[9::8] if(i.get_text() != 'Item')]
                values = [i.get_text() for i in self.accounting(f.income, period).findAll( 'span' )[92:377]]

            # To insert metadata
            for idx, key in enumerate(items):
                data[key] = {}
                for year, num in zip(date, values[idx * width:]):
                    data[key][year] = num

            # If parameters dont meet requirement, return 400 code
            return data if( data != {}) else 400
        except requests.ConnectionError:
            return 500