# lemmus helper functions

import ConfigParser,os,getpass,sh
from github import *

def createNewConfig( configfilename ):
	open(configfilename,'a').close()
	setUsernamePassword(configfilename)
	setStatus(configfilename,'current_repo','None')
	setStatus(configfilename,'current_issue','None')
	setStatus(configfilename,'repo_local_location','None')
	setStatus(configfilename,'repo_meta_local_location','None')
	setStatus(configfilename,'project_type','puppet_submodule')

def getAndCheckGithubLogin():
	#result = True
	print 'Please enter your Github Credentials...:'
	username = raw_input('Username:')
	password = getpass.getpass()
	
	loginSucces = checkGithubLogin(username,password)
	
	return loginSucces,username,password	


def checkGithubLogin(un,pw):
	result = True
	gh = Github(un,pw)
	logintest = gh.get_user().get_repos()
	# github api only checks credentials when checking data
	# it throws a BadCredentialsException if there is a login error
	# so to test the credentials check data in repo
	try:
		logintest[0].name
	except BadCredentialsException:
		result  = False
		print 'ERROR: Error while loggin in at Github. Please check your credentials'
	except GithubException:
		result  = False
		print 'ERROR: Error while login. Maximum number of login attempts exceeded'
		exit(1)
	return result

def getUserNamePassword(configfilename):
	config = ConfigParser.RawConfigParser()
	config.read(configfilename)
	config_data = {}
	config_data['github_username'] = config.get('Credentials','github_username')
	config_data['github_password'] = config.get('Credentials','github_password')
	#config_data['current_repo'] = config.get('Status','current_repo')

	return config_data

def setUsernamePassword(configfilename):
	config = ConfigParser.RawConfigParser()
	config.read(configfilename)
	loginSucces = False
	while loginSucces is False:
		gh_login = getAndCheckGithubLogin()	
		loginSucces = gh_login[0]

	if not config.has_section('Credentials'):
		config.add_section('Credentials')
	#config.add_section('Credentials')
	config.set('Credentials','github_username',gh_login[1])
	config.set('Credentials','github_password',gh_login[2])
	#config.set('Status','current_repo','None')
	configfile = open(configfilename,'wb')
	config.write(configfile)
	os.chmod(configfilename,0600)

def setStatus(configfilename,name,value):
	config = ConfigParser.RawConfigParser()
	config.read(configfilename)
	if not config.has_section('Status'):
		config.add_section('Status')

	config.set('Status',name,value)
	configfile = open(configfilename,'wb')
	config.write(configfile)
	os.chmod(configfilename,0600)

def getStatus(configfilename,name):
	config = ConfigParser.RawConfigParser()
	config.read(configfilename)
	if not config.has_section('Status'):
		print 'ERROR: No section status available ... exiting'
		exit(11)
	if not config.has_option('Status',name):
		print 'ERROR: Option '+name+' not available ... exiting'
		exit(12)
	return config.get('Status',name)

def getGitVersion():
	git = sh.git.bake(_cwd=getStatus(configfilename,'repo_local_location'))
	return git.version().split(' ')[2]	









