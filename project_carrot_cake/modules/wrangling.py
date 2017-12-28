import os.path
from pathlib import Path
import pandas as pd
from OSE import OSE


class wrangling(object):
    """docstring for wrangling."""
    def __init__(self, arg):
        super(wrangling, self).__init__()
        pass
    def msg_filter(self, msgs, list_of_tickers):
        '''Returns: df with messages from given tickers given a set of messages'''
        print('Filtering messages:')
        temp = []
        for ticker in list_of_tickers:
            print("  Ticker: " + ticker)
            df = msgs[msgs['ISSUER_ID'] == ticker]
            temp.append(df)
        filtered_messages = pd.concat(temp)

        # Create csv with filtered_messages
        filtered_messages.to_csv('../data/filtered_messages.csv')
        return filtered_messages
    def message_category(self, msgs):
        '''Returns dataframe of categorized messages'''
        categories = msgs.CATEGORY.unique()
        print(categories)





## Testing data
# Functions
def find_file(file_name, path=''):
    p = Path(path)
    files = [x for x in p.iterdir() if x.name.find(file_name) >= 0 and not x.name.find('~$')>=0]
    return files


def get_tradable_tickers():
    '''Returns a list of tradable tickers'''
    x = find_file('ticker_information.xlsx', path='../data')
    path = x[0]
    df = pd.read_excel(path)
    return df[ df['TRADE'] == 1 ]


w = wrangling(True)

df = get_tradable_tickers()
tickers = df['TICKER']
#tickers = ['MOE', 'STB']

msgs = pd.read_excel('..\data\messages.xlsx')
print(w.msg_filter(msgs, tickers))
