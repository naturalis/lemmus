#!/usr/bin/python
__all__ = ['issue','init']



try:
	import sys
except ImportError:
	print 'Error while import [sys] module \nConsider checking your pc since os should really be there you fool!'
	exit(1)

# checking which version we are using. 
if sys.version_info >= (3,0):
	print 'This is written in python 2, please use that'
	exit(3)

	

try:
	import sh
except ImportError:
	print 'Error while importing [sh] module \n Consider installing it by running: \npip install sh'
	exit(1)

try:
	import os
except ImportError:
	print 'Error while import [os] module \n Consider checking your pc since os should really be there you fool!'
	exit(1)

try:
	import getpass
except ImportError:
	print 'Error while importing [getpass] module \n Consider installing it by running: \npip install getpass'
	exit(1)

try: 
	from github import *
except ImportError:
	print 'Error while importing [github] module \n Consider installing it by running: \npip install PyGithub'
	exit(1)

try: 
	import ConfigParser
except ImportError:
	print 'Error while import [ConfigParser] module \nConsider checking your pc since os should really be there you fool!'
	exit(1)

try: 
	import helper
except ImportError:
	print 'Error while import [helper] module \nConsider checking your pc since os should really be there you fool!'
	exit(1)

global configfilename
configfilename = os.path.expanduser('~') + '/.lemmus'

def getConfigFilename():
	return configfilename

if not os.path.isfile(configfilename):
	print 'No config file found. Creating one'
	helper.createNewConfig(configfilename)


current_config = helper.getUserNamePassword(configfilename)

if not helper.checkGithubLogin(current_config['github_username'],current_config['github_password']):
	helper.setUsernamePassword(configfilename)

