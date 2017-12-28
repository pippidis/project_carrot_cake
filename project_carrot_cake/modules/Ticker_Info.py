# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 17:11:28 2017

@author: Johannes Lorentzen
"""
import os.path
from pathlib import Path
import pandas as pd
from OSE import OSE


#Find the data folder: 

def find_folder(folder_name, path):
    '''Finds the subfolder with the given name, if multiple, multiple is given.'''
    pass
    
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



df = get_tradable_tickers()

OSE = OSE()

tickers = df['TICKER']
df = OSE.master_df(tickers)
df.to_csv('..\data\EOD.csv')


#Get messages: 

tot_msg = 451000
'''
created = False
for i in range(0, 10): # does it in 1000 msg batches
    r = range(i*1000,(i+1)*1000)
    print('----------- ' + str(i*1000) + ' -> ' + str((i+1)*1000) + ' -----------')
    [df, not_collected] = OSE.get_NewsWebMessages(r)
    if created:
        df_msg.append(df)
    elif df.empty:
        pass
    else:
        df_msg = df
        created = True
print(df_msg)

'''
#tot_msg = 451000
#r = range(1442,1450)
#[df_msg, not_collected] = OSE.get_NewsWebMessages(r)
#df_msg.to_csv('..\\data\\messages.csv')

    

#[df, not_collected] = OSE.get_NewsWebMessages(range(31100,36400))
#df.to_excel('..\\data\\messages.xlsx')


'''
for ticker in df['TICKER']:
    print(ticker)
    df2 = OSE.get_EOD(ticker)
    df2.to_excel('..\\data\\EOD\\EOD_' +  ticker.replace(' ', '_') + '.xlsx')
'''




'''
u = pd.read_excel(file[0])
print(str(file[0]))
u.to_excel(str(file[0]))
class TICKER():
    
    def __init__(self):
        pass
    
''' 