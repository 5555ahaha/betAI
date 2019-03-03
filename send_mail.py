import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
 
 
fromaddr = "fonzie93@gmail.com"
toaddr = ["alessandro.ponzo@yahoo.it", "peguz93@gmail.com", "mirko.lanzoni@yahoo.it", "andrea.baridon@hotmail.com"]
msg = MIMEMultipart()
msg['Subject'] = "PRONOSTICI BET A.I."
with open('pronostici.txt', 'r') as myfile:
    data=myfile.read()
body = data
msg.attach(MIMEText(body, 'plain'))
 
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, "h01lc4220n3Dur0")
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()
