#!/usr/bin/python

from github import *
import helper,os,sh

global repo

configfilename = os.path.expanduser('~') + '/.lemmus'
cred = helper.getUserNamePassword(configfilename)
gh = Github(cred['github_username'],cred['github_password'])

def getCurrentRepo():
	current_repo = getGithubRepo(helper.getStatus(configfilename,'current_repo'))
	return current_repo

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

def getGithubRepo(reponame):
	org_repos = gh.get_organization('naturalis').get_repos()
	repo = None
	for r in org_repos:
		if str(r.name).strip() == str(reponame).strip():
			repo = r
			break
	return repo

def getAllRepoIssues(repoObject):
	issues = repoObject.get_issues()
	#issue_counter = 1
	for issue in issues:
		d = issue.created_at
		assignee = None
		if assignee is None:
			assignee = 'Nobody'
		else:
			assignee = issue.assignee.name

		print '--------------------------------------------------------------------------------------------'
		print 'Number:\t\t' + str(issue.number)
		print 'Created:\t%02d' % d.year + ' - ' + '%02d' % d.month + ' - ' + '%02d' % d.day
		print 'Title:\t\t' + issue.title
		print 'Assignee:\t' + assignee + '\n'

def getIssue(IssueID):
	repo = getCurrentRepo()
	try:
		issue = repo.get_issue(IssueID)
	except UnknownObjectException:
		print 'Issue with ID: ' + str(IssueID) + ' not found ... exiting'
		exit(2)
	comments = issue.get_comments()
	d = issue.created_at
	assignee = None
	if assignee is None:
		assignee = 'Nobody'
	else:
		assignee = issue.assignee.name
	
	print '-------------------------------------------------------------------------------------------------'
	print 'ID:\t\t' + str(IssueID)
	print 'Created:\t%02d' % d.year + ' - ' + '%02d' % d.month + ' - ' + '%02d' % d.day
	print 'Title:\t\t' + issue.title
	print 'Assignee:\t' + assignee + '\n'
	print 'Description:\t' + issue.body
	for comment in comments:
		print 'Comment by:\t' + comment.user.name
		print 'Comment:\t' + comment.body
		print 'url: ' + comment.html_url

	return issue 

def createIssue():

	issue_title = raw_input('Title:')
	issue_description = raw_input('Description:')

	sure= raw_input('Are you sure you want to this issue for repository ' + helper.getStatus(configfilename,'current_repo') + ' [y/n]:')
	if not sure == 'y':
		print 'Canceld by user input'
	
	assignee = gh.get_user(cred['github_username'])
	repo = getCurrentRepo()

	yours = raw_input('Assign it to you name? [y/n]:')
	if yours == 'y':
		issue = repo.create_issue(issue_title,issue_description,assignee)
		print 'Issue created'
		want_it_now = raw_input('Do you want work on this issue now? [y/n]:')
		if want_it_now == 'y':
			helper.setStatus(configfilename,'current_issue',str(issue.number))
			print 'TO BE IMPLEMENTED: Created branch #' + str(issue.number) + ' in ' + helper.getStatus(configfilename,'current_repo')
			print 'Happy coding!'
	else:
		issue = repo.create_issue(issue_title,issue_description)
		print 'Issue created'
	
	#print str(issue.number)
	#print issue.title
	#print issue.body

	#return issue



def openCurrentIssue():
	repo = getCurrentRepo()
	issueID = helper.getStatus(configfilename,'current_issue')
	try:
		issue = repo.get_issue(int(issueID))
	except UnknownObjectException:
		print 'Issue with ID: ' + str(issueID) + ' not found ... exiting'
		exit(2)
	createBranch('#'+issueID)

def createBranch(branchName):
	git = sh.git.bake(_cwd=helper.getStatus(configfilename,'repo_local_location'))
	git_meta = sh.git.bake(_cwd=helper.getStatus(configfilename,'repo_meta_local_location'))
	
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
			print 'Did not switch to branch ' + branchName
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
			print 'Did not switch to branch ' + branchName
			exit(2)
	
	try:
		git.checkout(branchName)
	except:
		git.checkout('-b',branchName)
	
	try:
		git.push('origin',branchName)
	except:
		print 'WARNING: Unable to push ' + branchName + ' to Github'
	
	#git.branch('--set-upstream','origin',branchName)
	#exit(3)

	

	if int(git.version().split(' ')[2].split('.')[1]) < 8:
		try:
			git.branch('--set-upstream','origin',branchName)
		except:
			print 'WARNING: Unable to set upstream'
	else:
		try:
			git.branch('-u','origin/'+branchName)
		except:
			print 'WARNING: Unable to set upstream'
	










		

