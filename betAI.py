import os
import sys
import datetime
import json
def make_bet_json():
	campionati=["premier", "seriea", "liga", "bundesliga"]
	f_json = open("bet.json", "w")
	f_json.write("[") 
	for campionato in campionati:
		f_json.write("{")
		with open(campionato+"/"+campionato+"_bet.json", "r") as f:
			last_line = f.readlines()[-1]
			for line in json.load(f)	:
				f_json.write(line)
				print(line)
				if line != last_line:
					f_json.write(",")
			f_json.write("}")
			if campionato != "bundesliga":
				f_json.write(",")
	f_json.write("]")
	f_json.close()



print("-----------BETTING ARTIFICAL INTELLIGENCE START UPDATE AND TRAINING-----------")
print(datetime.datetime.now())
print("\n")
os.system('python check_update.py premier')
os.system('python check_update.py seriea')
os.system('python check_update.py liga')
os.system('python check_update.py bundesliga')
print("-----------BETTING ARTIFICAL INTELLIGENCE END UPDATE AND TRAINING-----------")
os.system('rm pronostici.txt')
os.system('rm bet.json')
print("-----------BETTING ARTIFICAL INTELLIGENCE START-----------")
os.chdir('./premier')
os.system('python pronostico.py')
os.chdir('../')
os.chdir('./seriea')
os.system('python pronostico.py')
os.chdir('../')
os.chdir('./liga')
os.system('python pronostico.py')
os.chdir('../')
os.chdir('./bundesliga')
os.system('python pronostico.py')
os.chdir('../')
print("-----------BETTING ARTIFICAL INTELLIGENCE STOP-----------")
#make_bet_json()
os.system('python send_mail.py')
