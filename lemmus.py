

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

from lemmus import *
print issue.bla
