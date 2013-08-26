#!/usr/bin/python

from github import *
import helper,os


cred = helper.getUserNamePassword(configfilename = os.path.expanduser('~') + '/.lemmus')
gh = Github(cred['github_username'],cred['github_password'])

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


		

