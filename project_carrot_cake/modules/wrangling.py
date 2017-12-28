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
        print('Filtering messages...')
        temp = []
        for ticker in list_of_tickers:
            #print("  Ticker: " + ticker)
            df = msgs[msgs['TICKER'] == ticker]
            temp.append(df)
        filtered_messages = pd.concat(temp)

        # Create csv with filtered_messages
        filtered_messages.to_csv('../data/filtered_messages.csv')
        return filtered_messages
    def message_category(self, msgs):
        '''Returns dataframe of categorized messages'''
        categories = msgs.CATEGORY.unique()
        # ticker, date, category 1, ..., category n
        temp = []
        for inded, msg in msgs.iterrows():

            x = {'TICKER': msg['TICKER'], 'DATE': msg['DATE'], 'MSG_ID': msg['MSG_ID']}
            for category in categories:
                if msg['CATEGORY'] == category:
                    x[category] = 1
                else:
                    x[category] = 0
                    
            #Checking for attachments
            if msg['ATTACHMENT_ID'] >0:
                x['HAS_ATTACHMENT'] = 1
            else:
                x['HAS_ATTACHMENT'] = 0
                
            temp.append(x)
        return pd.DataFrame(temp)



        #for category in categories:
            #print('Category: ' + category)
            #x = msgs[msgs['CATEGORY'] = category]
            # if category = 'category', set 1 in column 'category'

    def coalesce(self, msgs, period='day'):
        ''' Returns sum of messages per period per ticker '''
        tickers = msgs.TICKER.unique()
        days = msgs["DATE"].map(pd.Timestamp.date).unique()

        temp = []
        for day in days: 
            print(day)
            for ticker in tickers: 
                f = (msgs['DATE'].map(pd.Timestamp.date) == day) & (msgs['TICKER'] == ticker)
                df = msgs[f]
                x = {'DATE':day, 'TICKER':ticker, 'NUMBER_OF_MESSAGES':len(df)} 
                for column in df:
                    #f = (column == 'DATE') or (column == 'TICKER') or (column == 'MSG_ID')
                    f = (column in ['DATE', 'TICKER', 'MSG_ID'])
                    if not f:
                        x[column] = df[column].sum()
                temp.append(x)
        return pd.DataFrame(temp)




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
msgs = w.msg_filter(msgs, tickers)

cat = w.message_category(msgs)
cat.to_excel('..\data\messages_category.xlsx')

coal = w.coalesce(cat)
coal.to_excel('..\data\messages_coal.xlsx')

