# -*- coding: utf-8 -*-
"""
Created on Sun Dec 24 15:26:32 2017

@author: Johannes Lorentzen 

Contains the OSE class, a class that downloads data from the Oslo Stock Exchange
    (OSE).


Finne antall akser: http://www.netfonds.no/quotes/about.php?paper=PLCS.OSE
Alt er lagret i HTML så lett å hente data fra dem

"""
import urllib.request
import urllib.error
import pandas as pd
import os
import datetime

class OSE():
    '''This class downloads data from the Oslo Stock Exhange (OSE)'''

    def __init__(self):
        pass

    def get_EOD(self, ticker=''):
        filename = 'tempfile_downloading.xlsx'
        URL = self.EOD_URL(ticker)
        self.get_excel(URL, filename=filename, path='', i=1)
        df = self.read_excel(filename=filename)
        self.del_excel(filename=filename)
        return df



    def EOD_URL(self, ticker='', start=0, stop='now', filename='data.xlsx'):
        '''Returns compleate URL to download EOD data from OSE'''

        ticker = ticker.replace(' ', '%20') # To remove whitespace
        if ticker[-4:] is not '.OSE':
           ticker = ticker + '.OSE'

        URL = []
        # Creates the URL:
        URL.append('https://www.oslobors.no/ob/servlets/excel?')
        URL.append('type=history')
        URL.append('&columns=DATE%2C+CLOSE_CA%2C+BID_CA%2C+ASK_CA%2C+HIGH_CA%2C+LOW_CA%2C+TURNOVER_TOTAL%2C+VOLUME_TOTAL_CA%2C+TRADES_COUNT%2C+TRADES_COUNT_TOTAL%2C+VWAP_CA')

        # Define formating
        URL.append('&format[DATE]=dd-mm-YYYY')
        URL.append('&format[CLOSE_CA]=%23%2C%23%230.00%23%23%23')
        URL.append('&format[BID_CA]=%23%2C%23%230.00%23%23')
        URL.append('&format[ASK_CA]=%23%2C%23%230.00%23%23')
        URL.append('&format[HIGH_CA]=%23%2C%23%230.00%23%23%23')
        URL.append('&format[LOW_CA]=%23%2C%23%230.00%23%23%23')
        URL.append('&format[TURNOVER_TOTAL]=%23%2C%23%230')
        URL.append('&format[VOLUME_TOTAL_CA]=%23%2C%23%230')
        URL.append('&format[TRADES_COUNT]=%23%2C%23%230')
        URL.append('&format[TRADES_COUNT_TOTAL]=%23%2C%23%230')
        URL.append('&format[VWAP_CA]=%23%2C%23%230.00%23%23%23')

        # Define Headers
        URL.append('&header[DATE]=DATE')
        URL.append('&header[CLOSE_CA]=CLOSE_CA')
        URL.append('&header[BID_CA]=BID_CA')
        URL.append('&header[ASK_CA]=ASK_CA')
        URL.append('&header[HIGH_CA]=HIGH_CA')
        URL.append('&header[LOW_CA]=LOW_CA')
        URL.append('&header[TURNOVER_TOTAL]=TURNOVER_TOTAL')
        URL.append('&header[VOLUME_TOTAL_CA]=VOLUME_TOTAL_CA')
        URL.append('&header[TRADES_COUNT]=TRADES_COUNT')
        URL.append('&header[TRADES_COUNT_TOTAL]=TRADES_COUNT_TOTAL')
        URL.append('&header[VWAP_CA]=VWAP_CA')

        # Other information
        URL.append('&view=DELAYED')
        URL.append('&source=feed.ose.quotes.INSTRUMENTS')
        URL.append('&filter=ITEM_SECTOR%3D%3Ds' + str(ticker) + '%26%26DELETED!%3Dn1')
        URL.append('&stop=' + str(stop))
        URL.append('&start=' + str(start))
        URL.append('&space=DAY')
        URL.append('&ascending=true')
        URL.append('&filename=' + str(filename))  # Filename must be last due to other implementation in download

        return "".join(URL)

    def get_excel(self, URL, filename='data.xlsx', path='', i=1):
        '''Download the excel file and returns the path for the file
            It is implemented to try 10 times, if not, it gives up'''

        max_tries = 10
        try:
            urllib.request.urlretrieve(URL, filename)
            pass
        except urllib.error.URLError as e:
            if hasattr(e, 'reason'):
                print('We failed to reach a server. - trying again...  [' + str(i) + ' of ' + str(max_tries) + ' tries]' )
                print('Reason: ', e.reason)
            elif hasattr(e, 'code'):
                print('The server couldn\'t fulfill the request.')
                print('Error code: ', e.code)
            if i < max_tries:
                self.get_excel(URL, filename=filename, path=path, i=i+1)
                pass
            else:
                print('Tried ' + str(i) + ' - Giving up')
                return(False)
        else:
            # everything is fine
            return(True)



    def read_excel(self, filename):
        '''Reads the excel file and returns a pandas dataframe with the information'''
        try:
            data_frame = pd.read_excel(filename, sheetname=0)
        except TypeError  as e:
            print('Problem reading the Excel file from OSE:  - TypeError')
            print('Reason: ' + str(e))
            return -1
        except ValueError as e:
            print('Problem reading the Excel file from OSE:  - ValueError')
            print('Reason: ' + str(e))
            return -1
        except IOError as e:
            print('Problem reading the Excel file from OSE:  - IOError')
            print('Reason: ' + str(e))
            return -1

        return(data_frame)

    def del_excel(self, filename):
        '''Deletes the excel file'''
        try:
            os.remove(filename)
        except:
            print('Could not delete the file - it is not that importatnt anyway')

    def get_NewsWebMessage(self, MSG_ID, timeout=0.1):
        '''Returns data from NewsWeb message
            There is a lot of customasation for the different types of information..
        '''

        msg = {'MSG_ID':MSG_ID}

        #Downloads the html
        msg['URL'] = 'http://www.newsweb.no/newsweb/search.do?messageId=' + str(MSG_ID) + '&siteLanguage=no'
        try:
            fp = urllib.request.urlopen(msg['URL'], timeout=timeout )
            byte_html = fp.read()
            html = byte_html.decode("utf8")
            fp.close()
        except:
            return -1

        # Checking if the message exsists
        if html.find('Beklager, ingen melding funnet med') > 0:
            return -2

        #Exstract the date:
        start = html.find('<td class="messageDetailTextInvert">') + len('<td class="messageDetailTextInvert"') + 1
        date_length = len('30.11.2017 13:57')
        date = html[start:start+date_length]
        msg['DATE'] = pd.to_datetime(date)

        #Exstract "Utsteder":
        key_start = '<tr><td class="messageDetailTitle">Utsteder</td>'
        key_end = '<td class="messageDetailTitleInvert">UtstederID</td>'
        msg['ISSUER'] = self._msg_exstract(html, key_start, key_end, 44, -24)

        #Extract Ticker / Utsteder ID:
        key_start = '<tr><td class="messageDetailTitleInvert">UtstederID</td>'
        key_end = '<tr><td class="messageDetailTitle">Instrument</td>'
        msg['ISSUER_ID'] = self._msg_exstract(html, key_start, key_end, 50, -20)

        #Exstract Intrument
        key_start = '<tr><td class="messageDetailTitle">Instrument</td>'
        key_end = '<tr><td class="messageDetailTitleInvert">Marked</td>'
        msg['INSTRUMENT'] = self._msg_exstract(html, key_start, key_end, 44, -20).strip()

        #Exstract Market / Marked
        key_start = '<tr><td class="messageDetailTitleInvert">Marked</td>'
        key_end = '<tr><td class="messageDetailTitle">Kategori</td>'
        msg['MARKET'] = self._msg_exstract(html, key_start, key_end, 50, -20)

        #Exstract CATEGORY / Kategori  - In norwegian
        key_start = '<tr><td class="messageDetailTitle">Kategori</td>'
        key_end = '<tr><td class="messageDetailTitle">Informasjonspliktig</td>'
        msg['CATEGORY'] = self._msg_exstract(html, key_start, key_end, 69, -55)

        #Exstract information requirements
        if html.find('Informasjonspliktige opplysninger') > 0:
            msg['MANDATORY_NOTIFICATION'] = 1
        else:
            msg['MANDATORY_NOTIFICATION'] = 0

        if html.find('Lagringspliktig melding') > 0:
            msg['OAM_ANNOUNCEMENT'] = 1
        else:
            msg['OAM_ANNOUNCEMENT'] = 0


        #Exstract attachment information
        if html.find('href="attachment.do?name=')<0:
            msg['ATTACHMENT_ID'] = ''
            msg['ATTACHMENT_NAME'] = ''
            msg['ATTACHMENT_URL'] = ''
        else:
            key_start = '&attId='
            key_end = 'src="images/ico_pdf.gif">'
            msg['ATTACHMENT_ID'] = self._msg_exstract(html, key_start, key_end, 0, -7)

            key_start = 'href="attachment.do?name='
            key_end = '&attId='
            msg['ATTACHMENT_NAME'] = self._msg_exstract(html, key_start, key_end, 0, -0)

            msg['ATTACHMENT_URL'] = 'http://www.newsweb.no/newsweb/attachment.do?name=' + msg['ATTACHMENT_NAME'] + '&attId=' + str(msg['ATTACHMENT_ID'])
        if len(msg['ATTACHMENT_ID']) > 15 or len(msg['ATTACHMENT_NAME']) > 150: #Some have errors.
            msg['ATTACHMENT_ID'] = ''
            msg['ATTACHMENT_NAME'] = ''
            msg['ATTACHMENT_URL'] = ''

        #Exstract title
        key_start = '<tr><td class="messageDetailTitle">Tittel</td>'
        key_end = '<tr><td class="messageDetailTitleInvert">Tekst</td>'
        msg['TITLE'] = self._msg_exstract(html, key_start, key_end, 44, -20)

        #Exstract message text
        key_start = '<div class="messageText"><pre class="wraptext">'
        key_end = '</pre></div></td></tr>'
        x = self._msg_exstract(html, key_start, key_end, 0, -0)
        x = x.replace('\n', ' ')
        x = x.replace('\r', ' ')

        if x.find('<br /><br />')>0:
            msg['TEXT'] = x[:-12]
        else:
            msg['TEXT'] = x

        return msg

    def _msg_exstract(self, string, key_start, key_end, start_offset=0, end_offset=0):
        '''Made to make the exstraction simpler'''
        start = string.find(key_start) + len(key_start) + start_offset
        end = string.find(key_end) + end_offset
        return string[start:end]

    def get_new_NewsWebMessages(self, MSG_ID_last, msg_per_day=1000):
        '''Returns a dataframe with the new messages that is newver then the
            one given in the input. It assumes a given max number of new messages
            per day. '''

        #Finds the number of expected messages:
        msg = self.get_NewsWebMessage(MSG_ID_last)
        dt = datetime.datetime.today()-msg['DATE']
        number_of_messages = dt.days*msg_per_day

        #Get the messages:
        MSG_IDs = range(MSG_ID_last + 1, MSG_ID_last + number_of_messages)
        df = self.get_NewsWebMessages(MSG_IDs)
        return df

    def get_NewsWebMessages(self, MSG_IDs, timeout=0.01, max_timeout=5):
        '''Returns a dataframe with the requried messages'''
        data = []
        not_collected = []
        for MSG_ID in MSG_IDs:
            msg = self.get_NewsWebMessage(MSG_ID=MSG_ID)
            if msg is -2:
                print('Error: No message for # ' + str(MSG_ID))
            elif msg is -1:
                print('Error: Message # ' + str(MSG_ID) + ' - Was not able to establish conection')
                not_collected.append(MSG_ID)
            else:
                print('Message # ' + str(MSG_ID) + ' collected')
                data.append(msg)
        df = pd.DataFrame(data)
        if len(not_collected) > 0 and timeout < max_timeout: #Trying again on missed messages
            print('---- Trying again for missed messages [Missing = ' + str(len(not_collected)) +' - Timeout = ' +str(timeout+ 0.1)+ ' ] -----')
            [df_missed, x] = self.get_NewsWebMessages(not_collected, timeout= timeout + 0.1)
            df.append(df_missed)

        return df, not_collected

    def master_df(self, tickers):
        '''Creates tha master dataframe for all EOD information'''
        temp = []
        for ticker in tickers:
            print(ticker)
            df = self.get_EOD(ticker)
            df['TICKER'] = [ticker for x in range(0,len(df))]
            temp.append(df)
        EOD = pd.concat(temp)
        return EOD

    def get_company_data(self, ticker=''):
        '''Downloads the complany data from OSE'''


        c_d = {'TICKER':ticker} #Company_data

        ticker = ticker.replace(' ', '%20') # To remove whitespace
        if ticker[-4:] is not '.OSE':
           ticker = ticker + '.OSE'

        #Downloads the html
        msg['URL'] = 'https://www.oslobors.no/markedsaktivitet/#/details/' + ticker +'/data'
        try:
            fp = urllib.request.urlopen(msg['URL'], timeout=timeout )
            byte_html = fp.read()
            html = byte_html.decode("utf8")
            fp.close()
        except:
            return -1

        # Checking if the message exsists
        if html.find('Beklager, ingen melding funnet med') > 0:
            return -2

        #Exstract the date:
        start = html.find('<td class="messageDetailTextInvert">') + len('<td class="messageDetailTextInvert"') + 1
        date_length = len('30.11.2017 13:57')
        date = html[start:start+date_length]
        msg['DATE'] = pd.to_datetime(date)


#u = pd.read_csv('ticker_list.csv', sep=';')
#tickers = u['TICKER']
#OSE = OSE()

#OSE.get_new_NewsWebMessages(441514, msg_per_day=30)

#[df, not_collected] = OSE.get_NewsWebMessages(range(31100,36400))
#df.to_excel('messages.xlsx')
