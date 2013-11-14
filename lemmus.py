#!/usr/bin/python


from lemmus import helper as h
from lemmus import Parser as parser
def kees():
	print 'hiep hiep'
p = parser.Parser()
p.add('piet',help='piet help')
p.add('karel',help='karel help')
p.add_sub('piet','bla',help='bla help')
p.add_sub('piet','kees',help='kees help')
print p.parse()
#argparse = h.importLib('argparse')

#p = argparse.ArgumentParser(description='test')
#p.add_argument('piet',
#				help='piet',
#				nargs=1)
#args = p.parse_args()
#print args