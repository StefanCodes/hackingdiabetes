""" PYTHON SCRIPT FOR PI TO SEND AN E-MAIL
TO IfThisThenThat WHEN TRIGGERED"""

import smtplib
from email.mime.text import MIMEText

def send_alerts(sub):
	#CONSTANTS
	#Change for your own use
	USER_EMAIL = 'HHVanTeam4@gmail.com'
	USERNAME = 'HHVanTeam4'
	PASSWORD = 'ThisIsSparta!'
	TRIGGER_EMAIL = 'trigger@ifttt.com'
	SUBJECT = sub
	CONTENT = ''

	#Construct RFC 2822 message
	msg = MIMEText(CONTENT)
	msg['From'] = USER_EMAIL
	msg['To'] = TRIGGER_EMAIL
	msg['Subject'] = SUBJECT

	#Provide email username and password
	#If the e-mail is not g-mail, will need to change server

	try:
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.ehlo()
		server.starttls()
		server.ehlo()
		server.login(USERNAME, PASSWORD)
		text = msg.as_string()
		server.sendmail(USER_EMAIL, TRIGGER_EMAIL, text)
		server.quit()
	except:
		print "ERROR: Couldn't log into e-mail account; make sure you are using G-Mail and that the information under #CONSTANTS is correct"
		pass