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
	try:
		repo = gh.get_organization('naturalis').get_repo(reponame)
	except:
		print 'Cannot find repository: ' + reponame
		exit(2)
	return repo
	#repo = None
	#for r in org_repos:
	#	if str(r.name).strip() == str(reponame).strip():
	#		repo = r
	#		break
	#return repo

def getAllRepoIssues(repoObject):
	issues = repoObject.get_issues()
	#issue_counter = 1
	for issue in issues:
		printIssue(issue)

def getCurrentIssue():
	return getIssue(int(helper.getStatus(configfilename,'current_issue')))

def getIssue(IssueID):
	repo = getCurrentRepo()
	try:
		issue = repo.get_issue(IssueID)
	except UnknownObjectException:
		print 'Issue with ID: ' + str(IssueID) + ' not found ... exiting'
		exit(2)
	return issue 

def printIssue(issueObject):
	comments = issueObject.get_comments()
	d = issueObject.created_at
	assignee = None
	if issueObject.assignee is None:
		assignee = 'Nobody'
	else:
		assignee = issueObject.assignee.name
	
	print '-------------------------------------------------------------------------------------------------'
	print 'ID:\t\t' + str(issueObject.number)
	print 'State:\t\t' + issueObject.state
	print 'Created:\t%02d' % d.year + '/' + '%02d' % d.month + '/' + '%02d' % d.day
	print 'Title:\t\t' + issueObject.title
	print 'Assignee:\t' + assignee 
	print 'Description:\t' + str(issueObject.body)
	for comment in comments:
		print '\n'
		print '\tComment by:\t' + comment.user.name
		print '\tComment:\t' + comment.body
		print '\turl: ' + comment.html_url 

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
			#helper.setStatus(configfilename,'current_issue',str(issue.number))
			#print 'TO BE IMPLEMENTED: Created branch #' + str(issue.number) + ' in ' + helper.getStatus(configfilename,'current_repo')
			openIssue(issue.number)
			print 'Happy coding!'
	else:
		issue = repo.create_issue(issue_title,issue_description)
		print 'Issue created'
	
def takeIssue(issueID):
	assignee = gh.get_user(cred['github_username'])
	repo = getCurrentRepo()
	issue = getIssue(issueID)
	issue.edit(assignee=assignee)

def openIssue(issueID):
	#repo = getCurrentRepo()
	helper.setStatus(configfilename,'current_issue',issueID)
	createBranch('#'+str(issueID))
	#print str(issueID)


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

def setComment(commentText):
	repo = getCurrentRepo()
	issueID = helper.getStatus(configfilename,'current_issue')
	issue = getIssue(int(issueID))
	issue.create_comment(commentText)

def closeIssue(issueID):
	repo = getCurrentRepo()
	issue = getIssue(issueID)
	issue.edit(state='closed')


def commit(message):
	git = sh.git.bake(_cwd=helper.getStatus(configfilename,'repo_local_location'))
	git.add('*.*')
	git.commit('-a',m=message)
	try:
		git.push()
	except:
		print 'WARNING: Unable to push latest commit to github'

def test():
	git = sh.git.bake(_cwd=helper.getStatus(configfilename,'repo_local_location'))
	git_meta = sh.git.bake(_cwd=helper.getStatus(configfilename,'repo_meta_local_location'))
	branchName = '#' + helper.getStatus(configfilename,'current_issue')
	try:
		git_meta.checkout('master')
	except:
		print 'ERROR: Unable to checkout to master branch of meta repository'
		exit(2)
	try:
		git_meta.pull()
	except:
		print 'ERROR: Unable to pull latest changes of the meta repository from Github'
		exit(2)

	try:
		git_meta.checkout(branchName)
	except:
		git_meta.checkout('-b',branchName)
	
	git.checkout(branchName)

	git_meta.add(helper.getStatus(configfilename,'repo_local_location'))

	git_meta.commit('-a',m='Changed reference of module ' + helper.getStatus(configfilename,'current_repo') + 'to HEAD of ' + branchName)

	try:
		git_meta.push('origin',branchName)
	except:
		print 'WARNING: Unable to push ' + branchName + ' to Github'


	if int(git_meta.version().split(' ')[2].split('.')[1]) < 8:
		try:
			git_meta.branch('--set-upstream','origin',branchName)
		except:
			print 'WARNING: Unable to set upstream'
	else:
		try:
			git_meta.branch('-u','origin/'+branchName)
		except:
			print 'WARNING: Unable to set upstream'

	print 'Testing branch created. Jenkins will automaticly test it. A manual functionality test might still by handy at the moment '










	










		

