#############################
# Python PlayerNameSelector #
# Version: 0.0.0            #
# Author: saikrishna        #
#############################


from bs4 import BeautifulSoup
import requests
import bs2
import re
import csv
import logging
import threading
urls = []
dictionary = {}
for i in range(65,91):
    urls.append('http://howstat.com/cricket/Statistics/Players/PlayerList.asp?Group='+chr(i))
def selected(urls):
        
        players = []  
        names = []
        
        website = requests.get(urls).text
        soup = BeautifulSoup(website,'lxml')
        soup3 = BeautifulSoup(website,'lxml')
        print('###')
        table = soup.find('table',class_ = 'TableLined')
        for name in table.find_all('a',class_= 'LinkNormal'):
            nam = name['href'].split('=')
            if nam[0] == "PlayerOverview_ODI.asp?PlayerID":
                players.append(str(nam[1]))                  
        for i in range(len(players)):
        
            
            website = requests.get('http://howstat.com/cricket/Statistics/Players/PlayerOverview_ODI.asp?PlayerID='+players[i]).text
            soup = BeautifulSoup(website,'lxml')
            s = soup.find('table')
            for s3 in s.find_all('td',class_ = 'TextGreenBold12'):
                    name = s3.text
                    name1 = name.split('(')
                    word1 = re.split("[^a-zA-Z]*",name1[0])
                    full_name = ''.join(word1)
                    
                    
                    dictionary[players[i]] = full_name

#USING MULTI THREADING TO MAKE PROCESS FASTER                  
   
threads = list()
for index in range(26):
            
            logging.info("Main    : create and start thread %d.", index)
            x = threading.Thread(target=selected, args = (urls[index],))
            threads.append(x)
            x.start()
for index, thread in enumerate(threads):
            logging.info("Main    : before joining thread %d.", index)
            thread.join()
            logging.info("Main    : thread %d done", index)            

