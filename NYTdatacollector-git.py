#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 14 11:47:23 2020

@author: aditigupta
"""
import requests
from requests.exceptions import HTTPError
import csv

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


from urllib.request import urlopen
from bs4 import BeautifulSoup
from tempfile import NamedTemporaryFile
import random


start = 0
end = 0



def execute(querytopic, startdate, enddate):
    dict_data = []
    your_key = "api-key=" + "ADD-YOUR-KEY"
    query = "q=" + querytopic
    facetstuff = "facet_fields=source&facet=true&type_of_material=Editorial"
    end_date = "begin_date="+ startdate + "&end_date=" + enddate #"end_date="+ enddate 
    show = "fl=web_url&fl=pub_date&fl=word_count&fl=headline&fl=byline"
    editorial = "news_desk=Editorial"
    
    
    
    try:
        requestUrl = "https://api.nytimes.com/svc/search/v2/articlesearch.json?"+query+"&"+facetstuff+"&"+end_date+"&"+show+"&"+your_key+"&"+ editorial
        print(requestUrl)
        requestHeaders = {"Accept": "application/json"}
        request = requests.get(requestUrl, headers=requestHeaders)
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        
    except Exception as err:
        print(f'Other error occurred: {err}')
    
    
    jsonResponse = request.json()
    
    
    for i in range(10):
        
        if jsonResponse["response"]["docs"][i]["word_count"] > 0:# and jsonResponse["response"]["docs"][i]["web_url"] not in :
            tempdict = jsonResponse["response"]["docs"][i]
            newdict = {}
            newdict["query"] = querytopic
            newdict["title"] = jsonResponse["response"]["docs"][i]["headline"]["main"]
            newdict["web_url"] = jsonResponse["response"]["docs"][i]["web_url"]
            newdict["pub_date"] = jsonResponse["response"]["docs"][i]["pub_date"]
            newdict["word_count"] =jsonResponse["response"]["docs"][i]["word_count"]
            
            newdict["Writer"] =  jsonResponse["response"]["docs"][i]["byline"]["original"]
            dict_data.append(newdict)
            
    uniquecheck = []
    for i in range(len(dict_data)):
        if dict_data[i]["web_url"] in uniquecheck:
            dict_data.remove(dict_data[i])
        else:
            uniquecheck.append(dict_data[i]["web_url"])
    
    
    return(dict_data)

def usehtml(dict_data):
    csv_columns = ['web_url',"title","Writer",'pub_date','word_count', "query", "content"]
    csv_file = "URLS+.csv"
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in dict_data:
                writer.writerow(data)
    except IOError:
        print("I/O error")
    
    #print()
    

def scrape(dict_data):
    newlist = dict_data
    
    for links in range(len(dict_data)):  
        try:
            url = dict_data[links]["web_url"]
            html = urlopen(url)
            soup = BeautifulSoup(html, 'lxml')
            p_tags = soup.find_all("p")
            
            p_tags_text = [tag.get_text().strip() for tag in p_tags]
            
            sentence_list = [sentence for sentence in p_tags_text if not '\n' in sentence]
            sentence_list = [sentence for sentence in sentence_list if '.' in sentence]
            
            article = ' '.join(sentence_list)
            dict_data[links]["content"] = article
        except:
            
            dict_data[links]["content"] = ""
            print("CHECK \n\n\n")
    return(dict_data)
        
    
def appendtocsv(dict_data):
    with open("URLS+.csv", "a") as csvfile:
        writer = csv.writer(csvfile) 
        for i in range(len(dict_data)):
            
            if dict_data[i]["content"] != "":
                writer.writerow([dict_data[i]['web_url'],dict_data[i]["title"],dict_data[i]['Writer'],dict_data[i]['pub_date'],dict_data[i]['word_count'], dict_data[i]["query"], dict_data[i]["content"]])
        
    

if __name__ == "__main__":
    query = ['employment', 'unemployment', 'GDP', 'inflation', 'price', 'economy', 'market', 'bill', 'Democratic Party', 'Republican Party', 'Education', 'College', 'resources', 'president', 'election', 'poll', 'employment', 'unemployment', 'GDP', 'inflation', 'price', 'economy', 'market', 'bill', 'Democratic Party', 'Republican Party', 'Education', 'College', 'resources', 'president', 'election', 'poll', 'employment', 'unemployment', 'GDP', 'inflation', 'price', 'economy', 'market', 'bill', 'Democratic Party', 'Republican Party', 'Education', 'College', 'resources', 'president', 'election', 'poll', 'employment', 'unemployment', 'GDP', 'inflation', 'price', 'economy', 'market', 'bill', 'Democratic Party', 'Republican Party', 'Education', 'College', 'resources', 'president', 'election', 'poll', 'employment', 'unemployment', 'GDP', 'inflation', 'price', 'economy', 'market', 'bill', 'Democratic Party', 'Republican Party', 'Education', 'College', 'resources', 'president', 'election', 'poll', 'employment', 'unemployment', 'GDP', 'inflation', 'price', 'economy', 'market', 'bill', 'Democratic Party', 'Republican Party', 'Education', 'College', 'resources', 'president', 'election', 'poll', 'employment', 'unemployment', 'GDP', 'inflation', 'price', 'economy', 'market', 'bill', 'Democratic Party', 'Republican Party', 'Education', 'College', 'resources', 'president', 'election', 'poll', 'employment', 'unemployment', 'GDP', 'inflation', 'price', 'economy', 'market', 'bill', 'Democratic Party', 'Republican Party', 'Education', 'College', 'resources']
    start = ['20100101', '20100201', '20100301', '20100401', '20100501', '20100601', '20100701', '20100801', '20100901', '20101001', '20101101', '20101201', '20110101', '20110201', '20110301', '20110401', '20110501', '20110601', '20110701', '20110801', '20110901', '20111001', '20111101', '20111201', '20120101', '20120201', '20120301', '20120401', '20120501', '20120601', '20120701', '20120801', '20120901', '20121001', '20121101', '20121201', '20130101', '20130201', '20130301', '20130401', '20130501', '20130601', '20130701', '20130801', '20140301', '20140501', '20141101', '20150401', '20150501', '20150601', '20160301', '20160501', '20160901', '20190101', '20200101', '20200601']
    end = ['20100128', '20100228', '20100328', '20100428', '20100528', '20100628', '20100728', '20100828', '20100928', '20101028', '20101128', '20101228', '20110128', '20110228', '20110328', '20110428', '20110528', '20110628', '20110728', '20110828', '20110928', '20111028', '20111128', '20111228', '20120128', '20120228', '20120328', '20120428', '20120528', '20120628', '20120728', '20120828', '20120928', '20121028', '20121128', '20121228', '20130128', '20130228', '20130328', '20130428', '20130528', '20130628', '20130728', '20130828', '20140328', '20140528', '20141128', '20150428', '20150528', '20150628', '20160328', '20160528', '20160928', '20190128', '20200128', '20200628']
 
    print(start)
    print(end)
    
    
    random.shuffle(query)
    for i in range(len(start)):
        
        data = execute(query[i],  start[i], end[i] )
        print("done with execute", query[i],  start[i], end[i])
        scrapeddata = scrape(data)
        print("done with scrape", query[i],  start[i], end[i])
        
        appendtocsv(scrapeddata)
        print("round done ", query[i],  start[i], end[i] )
            
 
