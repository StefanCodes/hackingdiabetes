Hacking Diabetes
===============

An easy way for you to remotely monitor glucose levels via G4. It creates easy-to-read visualizations for your iOS, and can be configured to send out text/push notifications when the G4 detects dangerous glucose levels.

Compatible with: Dexcom G4 and Raspberry Pi/Linux (Debian/Ubuntu Distros)


--------------
To install and run:

1. Pull repository from Github

2. Navigate to hackingdiabetes/Pi/dexcom_reader_mod and open up send_alerts.py

3. **Change the values of USER_EMAIL, USERNAME, PASSWORD, and SUBJECT to correspond to your own If This Then That configurations. For example, if your IfTTT user e-mail is derp@gmail.com, then change the line:  
USER_EMAIL = 'HHVanTeam4@gmail.com' to USER_EMAIL = 'derp@gmail.com'

4. Connect Dexcom G4 Receiver to computer

5. Open up the command line

6. Navigate to the hackingdiabetes folder

7. ***Enter the command 'sudo python run_project.py'


** This project relies on If This Then That to send out iOS notifications and text messages as alerts. If you do not already have an account, go to https://ifttt.com, create an account, and create two recipes: one for email to SMS, and one for email to iOS. Note that this project currently only works with G-Mail e-mail addresses!

*** Make sure to have python 2.7 installed. If you need to install python, run the command 'apt-get install python2.7'

--------------


This project was pitched and created at Hacking Health Vancouver 2014.
http://www.hackinghealth.ca/events/vancouver/hhvancouver2014/

Project board: http://hh-vancouver.sparkboard.com/project/5374f8140511040200000009
