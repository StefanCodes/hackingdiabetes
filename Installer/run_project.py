"""If dependencies have not been installed/set up,
set them up. Then, run the program"""

import os

#install pip and virtual env
os.system('apt-get install python-pip')
os.system('pip install virtualenv')

#set up and run virtuanenv environment
os.chdir(os.getcwd() + "/Pi")
os.system('virtualenv venv')
os.system('chmod 777 venv')
os.system('chmod 777 venv/bin/activate')
os.system('venv/bin/activate')

#install all remaining requirements
os.system('apt-get install python-numpy')
os.system('apt-get install python-setuptools')
os.system('easy_install --upgrade pytz')
os.system('pip install pyserial')
os.system('pip install requests')

#run other scripts
os.system('python dexcom_reader_mod/agent.py')
