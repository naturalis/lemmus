#!/usr/bin/python

from github import *
import helper,os,sh

configfilename = os.path.expanduser('~') + '/.lemmus'

cred = helper.getUserNamePassword(configfilename)
gh = Github(cred['github_username'],cred['github_password'])



def initSubmodule(repodir='.'):

	if repodir == '.':
		repodir = os.getcwd()

	repodir =  os.path.normpath(repodir)

	if not os.path.isfile(os.path.join(repodir,'.git')):
		print 'ERROR: ' + repodir + ' is not a Git submodle ... exiting'
		exit(2)

	print 'Current puppet module dir: ' + repodir

	#go down two directory's for meta repo 
	meta_repodir = os.path.dirname(repodir)
	meta_repodir = os.path.dirname(meta_repodir)
	
	if not os.path.isdir(os.path.join(meta_repodir,'.git')):
   		print meta_repodir + ' seems not to be a good puppet meta directory. Reclone you git repo ... exiting'
   		exit(2)
	print 'puppet meta dir: ' + meta_repodir
	helper.setStatus(configfilename,'repo_local_location',repodir)
	helper.setStatus(configfilename,'repo_meta_local_location',meta_repodir)

	git = sh.git.bake(_cwd=repodir)
	remote_origin = git.remote('show','origin')
	current_git_repo = remote_origin.splitlines()[1].split('/')[-1]
	print 'Current repository you want to work in: [' + current_git_repo + ']'
	org_repos = gh.get_organization('naturalis').get_repos()
	repo = None
	for r in org_repos:
		if str(r.name).strip() == str(current_git_repo).strip():
			repo = r
			print 'Found repository [' + r.name + '] found on Github'
			break
	helper.setStatus(configfilename,'current_repo',repo.name)

def showStatus():
	un = helper.getUserNamePassword(configfilename)
	print 'Current status'
	print 'Github username:\t\t' + un['github_username']
	print 'Github password:\t\tl3mmu$_is_cool_and'
	print 'Repository:\t\t\t' + helper.getStatus(configfilename,'current_repo')
	print 'Issue:\t\t\t\t' + helper.getStatus(configfilename,'current_issue')
	print 'Repository directory: \t\t' + helper.getStatus(configfilename,'repo_local_location')
	print 'Meta repository directory:\t' + helper.getStatus(configfilename,'repo_meta_local_location')

def resetStatus():
	helper.setStatus(configfilename,'current_repo','None')
	helper.setStatus(configfilename,'current_issue','None')
	helper.setStatus(configfilename,'repo_local_location','None')
	helper.setStatus(configfilename,'repo_meta_local_location','None')
	helper.setStatus(configfilename,'project_type','puppet_submodule')
	print 'All repository information set to None'

def initRepository(obj):
	
	print 'initializing ' + obj + ' as git directory '
	
