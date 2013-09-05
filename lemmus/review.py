#!/usr/bin/python

from github import *
import helper,os,sh

global repo

configfilename = os.path.expanduser('~') + '/.lemmus'
cred = helper.getUserNamePassword(configfilename)
gh = Github(cred['github_username'],cred['github_password'])

def mergeWithMaster():
	git = sh.git.bake(_cwd=helper.getStatus(configfilename,'repo_local_location'))
	git_meta = sh.git.bake(_cwd=helper.getStatus(configfilename,'repo_meta_local_location'))
	issue = helper.getStatus(configfilename,'current_issue')
	print 'You will merge ticket #' + issue + ' of repository ' + helper.getStatus(configfilename,'current_repo') + ' to the master and meta master.'
	if not raw_input('Continue? [y/n]') == 'y':
		print 'Canceld by user input'
		exit(2)
	
	try:
		git_meta.checkout('master')
	except:
		print 'FATAL: Unable to switch to master branch of meta repository. .. exiting'
		exit(2)
	
	try:
		git_meta.pull()
	except:
		print 'WARNING: Unable to pull latest updates of master of the meta repository on Github'
		if not raw_input('Continue? [y/n]') == 'y':
			print 'Canceld by user input'
			exit(2)

	try:
		git_meta.checkout('#'+issue)
	except:
		print 'FATAL: Unable to switch to #'+issue+' branch of meta repository. .. exiting'
		exit(2)
	
	try:
		git_meta.pull()
	except:
		print 'WARNING: Unable to pull latest updates of #'+issue+' of the meta repository on Github'
		if not raw_input('Continue? [y/n]') == 'y':
			print 'Canceld by user input'
			exit(2)

	try:
		git.checkout('master')
	except:
		print 'FATAL: Unable to switch to master branch of submodule ... exiting'
		exit(2)
	
	try:
		git.pull()
	except:
		print 'WARNING: Unable to pull latest updates of master of the submodule on Github'
		if not raw_input('Continue? [y/n]') == 'y':
			print 'Canceld by user input'
			exit(2)

	try:
		git.checkout('#'+issue)
	except:
		print 'FATAL: Unable to switch to #'+issue+' branch of submodule ... exiting'
		exit(2)
	
	try:
		git.pull()
	except:
		print 'WARNING: Unable to pull latest updates of #'+issue+' of the submodule on Github'
		if not raw_input('Continue? [y/n]') == 'y':
			print 'Canceld by user input'
			exit(2)
	
	print 'Merging master --> #' + issue
	git.merge('master')
	print 'Merging #' + issue + ' --> master'
	git.checkout('master')
	

	
	

	print 'Updating submodule link to head of submodule'
	git_meta.checkout('master')
	git_meta.add(helper.getStatus(configfilename,'repo_local_location'))
	git_meta.commit('-a',m='Changed reference of module ' + helper.getStatus(configfilename,'current_repo') + 'to HEAD of #' + issue)

	# if think it needs to be this, but it is contra with workflow documentation
	if not raw_input('Push changes to Github? [y/n]') == 'y':
		print 'Canceld by user'
		exit(2)

	git.push('master')
	git_meta.push('master')

def deleteBrach():
	print 'To be implemented'
