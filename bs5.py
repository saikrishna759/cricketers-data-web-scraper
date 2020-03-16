#############################
# Python PlayersStatsList   #
# Version: 0.0.0            #
# Author: saikrishna        #
#############################

from bs4 import BeautifulSoup
import requests
import csv
import bs2
import re
import time
import logging
import threading

t0 = time.time()


y={}
urls = []

#csv file
csv_file = open('project1.csv','w')
y['Names'] = 'names'
for i in range(1970,2020):
    y[str(i)] = str(i)
y['Total'] = 'total'    
w = csv.writer(csv_file)
w.writerow(y.keys())

from bs3 import *
for i in range(65,91):
    urls.append('http://howstat.com/cricket/Statistics/Players/PlayerList.asp?Group='+chr(i))

def selected(urls):
       
        players = []
        names = []
        website = requests.get(urls).text
        soup = BeautifulSoup(website,'lxml')
        table = soup.find('table',class_ = 'TableLined')
        for name in table.find_all('a',class_= 'LinkNormal'):
            nam = name['href'].split('=')
            if nam[0] == "PlayerOverview_ODI.asp?PlayerID":
                players.append(str(nam[1]))               
        

        years = []
        runs_scored =[]
        total_sum = []
        car = []
        for i in range(len(players)):
            try:
                year = []
                runs = []
                my_dict = {}
                career = {}
                
                website1 = requests.get('http://www.howstat.com/cricket/Statistics/Players/PlayerYears_ODI.asp?PlayerID='+players[i]).text
                soup1 = BeautifulSoup(website1,'lxml')
                list1 = soup1.find('div',{'id':'bat'})
                for list0 in list1.find_all('a',class_='LinkNormal'):
                    ino = 0
                    ye = list0.text
                    year.append(list0.text)
                    for element in list0.next_elements:
                            ino = ino+1
                            if ino == 25:
                                list4 = re.findall(r"\d+",element.text)
                                ru = str(list4[0])
                                runs.append(int(list4[0]))
                                break
                    career[ye] = ru
                car.append(career)        
                years.append(year)
                runs_scored.append(runs)
                total_sum.append(sum(runs_scored[i]))

                #creating each row of the csv file
                
                my_dict[players[i]] = dictionary[players[i]]
                m=0
                k=0
                for j in range(len(y.keys())-2):
                   m = m+1
                   if k < len(runs) and list(car[i].keys())[k] == list(y.values())[j+1]:
                       k = k+1
                       my_dict[m] = runs[k-1]
                   else:
                       my_dict[m] = ''     
                my_dict[j+2] = total_sum[i]
                    
                w.writerow(my_dict.values())
                 
            except Exception as e:
                print(e)
                pass
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

csv_file.close()

t1 = time.time()

print("########completed########")
print('time taken in secconds:',t1-t0)
print('time taken in minutes:',(t1-t0)/60)
















