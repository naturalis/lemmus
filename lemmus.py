

# Lemmus defines 4 groups
#
# Init
# Init module intializes the lemmus user.
# - registers github username password
# - gets te relevant dir's and repo's for developing
# - potentionally saves userdata locally (~/.lemmus) to ensure continuation after disaster
#
# Issue
# Issue module manages software issues and provides a workflow for fixing, testing etc by using github issue tracking
# - list current issues with creator and assignee and comments (or link to comments)
# - add an issue
# - close an issues
# - test a fix
# - delete an issue
#
# Review
# Review class provides tools for reviewing written code
# - does stuff
#
# ArgumentParse
# ArgumentPare class provides a parser for lemmus arguments and switches. Also provides the help
# - does stuff

import sys
from lemmus import *
#issue.getGithub()


if len(sys.argv) == 1:
	print 'no arugments given. Run lemmus help for help'
	exit(1)
argument = ''
for i in range(1,len(sys.argv)):
	argument += sys.argv[i] + ' '

if argument == 'help ':
	print 'this is a help message \n containing very \n very\nvery\nmuch\nlinies\n.\n.\n.'
elif argument == 'issue current ':
	issue.printIssue(issue.getCurrentIssue())
elif argument == 'issue repo ':
	print issue.getCurrentRepo().name
else:
	print 'Invalid arugment. Run lemmus help for help '

#ssue.getCurrentUserIssues()

#init.initSubmodule('/home/atze/git/naturalis/puppet/modules/base/')

#repo = 
#issue.getAllRepoIssues(issue.getCurrentRepo())
#issue.getIssue(7)
#issue.openCurrentIssue()
#a = issue.getCurrentRepo()
#print a.name
#init.initSubmodule()
