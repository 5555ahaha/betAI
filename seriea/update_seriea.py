from datetime import datetime
import csv
import os
import time
import re

#AGGIORNA L'ULTIMA STAGIONE
os.system('rm /tmp/outseriea.csv')
os.system('rm data/seriea.csv')
stagioni={'0809', '0910', '1011', '1112', '1213', '1314', '1415', '1516', '1617', '1718', '1819'}
fout=open("data/seriea.csv","w")
os.system('mkdir seasons')
for season in stagioni:
	os.system('wget -O seasons/'+season+'.csv http://www.football-data.co.uk/mmz4281/'+season+'/I1.csv')
	time.sleep(0.2)
# first file:
for line in open("seasons/0809.csv"):
	if re.match("^,,,,*", line):
		continue
	fout.write(line)
# now the rest:
stagioni.remove('0809')
for season in stagioni:
    f = open('seasons/'+season+'.csv')
    f.next() # skip the header
    for line in f:
        if re.match("^,,,,*", line):
    		continue
        fout.write(line)
fout.close()
data = csv.reader(open('data/seriea.csv','r'))
header = data.next()
datafy = csv.writer(open('/tmp/outseriea.csv', 'w'))
for row in data:
	try:
		if datetime.strptime(row[1], '%d/%m/%y'):
			row[1]=datetime.strptime(row[1], '%d/%m/%y').strftime('%d/%m/%Y')
			datafy.writerow(row)
	except ValueError:
		datafy.writerow(row)
		continue

datafy = csv.reader(open('/tmp/outseriea.csv', 'r'))
datafy = sorted(datafy, key = lambda row: datetime.strptime(row[1], "%d/%m/%Y"), reverse=False)
with open('data/seriea.csv', 'w') as stream:
	writer = csv.writer(stream)
	writer.writerow(header)
	writer.writerows(datafy)
os.chdir('../')
os.system('rm -rf seasons')