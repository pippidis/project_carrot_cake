# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 22:36:36 2018

@author: Johannes Lorentzen

Testing scraping of news pages on the net 
"""
'''
import newspaper

hegnar = newspaper.build('http://nrk.no', language='no')


print(hegnar.size())
for article in hegnar.articles:
    print(article.url)
    
for category in hegnar.category_urls():
    print(category)'''
    


import Scrapy
 
 
class HackerNewsItem(scrapy.Item):
    link_title = scrapy.Field()
    url = scrapy.Field()
    sentiment = scrapy.Field()
    text = scrapy.Field()