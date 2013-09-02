

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
# ArgumentParse class provides a parser for lemmus arguments and switches. Also provides the help
# - does stuff

import argparse
from lemmus import *
#issue.getGithub()

def issue_parser(arg):
	if not arg.list is None:
		if arg.list == 'all': 
			issue.printIssue(issue.getCurrentIssue())
		else:
			issue.getAllRepoIssues(issue.getGithubRepo(arg.list))
	elif not arg.comment is None:
		issue.setComment(arg.comment)
	elif not arg.add is None:
		issue.createIssue()
	elif not arg.close is None:
		print arg.close
	elif not arg.take is None:
		print arg.take
	elif not arg.commit is None:
		print arg.commit
	elif not arg.test is None:
		print arg.test
	else:
		print 'going for nothing'

		
def init_parser(arg):
	if not arg.repo is None:
		if arg.repo == 'current':
			init.initSubmodule()
		else:
			init.initSubmodule(arg.repo)
	else:
		print 'going for nothing'

def status_parser(arg):
	if not arg.show is None:
		init.showStatus()
	else:
		print 'going for noting'



parser = argparse.ArgumentParser(description='Helps the workflow puppet module www.github.com/naturalis/lemmus  ')

subparsers = parser.add_subparsers(title='subcommands')

parser_issue = subparsers.add_parser('issue', help='arguments for issue\'s ')
parser_issue.set_defaults(func=issue_parser)
parser_issue.add_argument('-list',
							help='list current issues on a naturalis repository. by default lists current issue',
							const='all',
							nargs='?',
							metavar='repository')
parser_issue.add_argument('-comment',
							help='update issue with a comment',
							metavar='"comment"')
parser_issue.add_argument('-add',
							const='do_it',
							nargs='?',
							metavar='',
							help='create a new issue. will run wizzard')
parser_issue.add_argument('-open',
							metavar='id (int)',
							type=int,
							help='open an issue to work on now ')
parser_issue.add_argument('-take',
							metavar='id (int)',
							type=int,
							help='assign an issue to your name. does not open a issue')
parser_issue.add_argument('-close',
							help='closes current issue',
							const='current',
							metavar='',
							nargs='?')
parser_issue.add_argument('-commit',
							help='commits current code and pushes it to Github',
							metavar='"message"')
parser_issue.add_argument('-test',
							help='creates branches needed for testing by jenkins',
							metavar='',
							const='test',
							nargs='?')

parser_init = subparsers.add_parser('init', help='arguments for initialization')
parser_init.set_defaults(func=init_parser)
parser_init.add_argument('-repo',
							help='initialize directory as current working directory',
							nargs='?',
							const='current',
							metavar='puppet submodule directory')


parser_status = subparsers.add_parser('status', help='arguments for initialization')
parser_status.set_defaults(func=status_parser)
parser_status.add_argument('-show',
							help='show current status',
							nargs='?',
							const='current',
							metavar='')
parser_status.add_argument('-reset',
							help='reset current status',
							nargs='?',
							const='current',
							metavar='')

args = parser.parse_args()
args.func(args)
#args.func(args)


#ssue.getCurrentUserIssues()

#init.initSubmodule('/home/atze/git/naturalis/puppet/modules/base/')

#repo = 
#issue.getAllRepoIssues(issue.getCurrentRepo())
#issue.getIssue(7)
#issue.openCurrentIssue()
#a = issue.getCurrentRepo()
#print a.name
#init.initSubmodule()
