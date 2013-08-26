#!/usr/bin/python

from github import *
import helper,os,sh


cred = helper.getUserNamePassword(configfilename = os.path.expanduser('~') + '/.lemmus')
gh = Github(cred['github_username'],cred['github_password'])

'''
def getCurrentUserIssues():
	issues = gh.get_user().get_issues()
	issue_counter = 1
	
	for issue in issues:
		d = issue.created_at
		print '-[' + str(issue_counter) + ']----[ %02d' % d.year + '.' + '%02d' % d.month + '.' + '%02d' % d.day +']---------'
		print 'Repository: \t' + issue.repository.name
		print 'Issue Title:\t' + issue.title
		print 'Issue Creator:\t' + issue.user.name
		print '\n'
		#print '[' + str(issue_counter) + ']\t-\t' + issue.title + '\t-\t' + issue.repository.name +'\t-\t'+ issue.user.name
		issue_counter += 1
'''



def initSubmodule(repodir='.'):
	meta_repodir = ''
	if repodir == '.':
		repodir = os.getcwd()

	if not os.path.isfile(os.path.join(repodir,'.git')):
		print 'ERROR: ' + repodir + ' is not a Git submodle ... exiting'
		exit(2)

	for i in range(1,len(repodir.split('/'))-2):
    	meta_repodir += '/' + repodir.split('/')[i]
	#print 'current puppet module dir: ' + cwd

	if not os.path.isdir(meta_repodir+'/.git'):
   		print meta_repodir + ' seems not to be a good puppet meta directory. Reclone you git repo'
    exit(2)

	print 'puppet meta dir: ' + meta_repodir

	
