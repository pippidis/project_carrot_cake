import pandas as pd

class wrangling(object):
    """docstring for wrangling."""
    def __init__(self, arg):
        super(wrangling, self).__init__()
        self.arg =
    def msg_filter(self, msgs, list_of_tickers):
        '''Returns: df with messages from given tickers given a set of messages'''
        for ticker in list_of_tickers:
            print('Ticker: ' + ticker)
            print('Indices: ' + msgs.index[msgs['ISSUER_ID'] == ticker].tolist())
            #print("DF: " + )

        #return filtered_messages
        return
