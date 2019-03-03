import urllib2
from bs4 import BeautifulSoup
from datetime import datetime
import re
import csv
import os
import sys
import pickle

def case(argument):
                switcher = {
                    'premier': 'http://www.football-data.co.uk/englandm.php',
                    'seriea': 'http://www.football-data.co.uk/italym.php',
                    'liga': 'http://www.football-data.co.uk/spainm.php',
                    'bundesliga': 'http://www.football-data.co.uk/germanym.php'
                }
                return switcher.get(argument, "Errore")


page = urllib2.urlopen(case(sys.argv[1]))
soup = BeautifulSoup(page, 'html.parser')
date = soup.find('i', text= re.compile("\d\d\/\d\d\/\d\d")).text
date = datetime.strptime(date.split("	")[1], '%d/%m/%y').strftime('%d/%m/%Y')
pickle_read = open(sys.argv[1]+'/data/last_date.pkl','rb')
last_date = pickle.load(pickle_read)
print("Last update: "+ last_date["date"])
print("New update: "+ date)
if last_date['date'] != date:
	print('\n=========>\t Start '+sys.argv[1]+' update\n')
        os.chdir(sys.argv[1])
        os.system('python predict.py > /dev/null 2>&1')
	pickle_write = open('data/last_date.pkl','wb')
	pickle.dump({'date': date},pickle_write)
	print('\n=========>\t Update '+sys.argv[1]+' finished\n')
        os.chdir('../')
else:
	print('\n=========>\t Dataset '+sys.argv[1]+' already updated\n')
