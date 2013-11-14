class Parser:
	sys = __import__('sys')
	def __init__(self,description='None given'):
		self.description=description
		self.args = dict()


	def add(self,arg,help=''):
		self.args.update({arg:{'help':help,'sub':{}}})

	def add_sub(self,arg,sub_arg,help=''):
		if not arg in self.args:
			print 'Argument %s not found'%(arg)
			exit(1)
		else:
			self.args[arg]['sub'].update({sub_arg:{'help':help}})

	def parse(self):
		
		if len(self.sys.argv) == 1:
			print 'No arguments given. Run %s help [argument] for detailed help'%(self.sys.argv[0])
			self.printHelp()

		if len(self.sys.argv) == 2:
			if not self.sys.argv[1] in self.args and self.sys.argv[1] != 'help': 
				print 'Argument %s not found'%(self.sys.argv[1])
				exit()
			if self.sys.argv[1] in self.args and self.args[self.sys.argv[1]]['sub'] != {}:
				print 'Argument %s requires sub arguments '%(self.sys.argv[1])
				self.printHelp(self.sys.argv[1])
				exit()
			if self.sys.argv[1] == 'help': 
				self.printHelp()
			else:
				return setattr(self,self.sys.argv[1],'') 
				#globals()[self.sys.argv[1]]()

		if len(self.sys.argv) > 2:
			if self.sys.argv[1] == 'help': 
				self.printHelp(self.sys.argv[2])
			else:
				return self.sys.argv[1:]

	def printHelp(self,arg=None):
		if not arg:
			print '\nDescription: %s\n\nArguments:\n'%(self.description)
			for a in self.args.keys():
				print '  %s \t\t %s'%(a,self.args[a]['help'])
		else:
			if arg in self.args:
				print '\nHelp for: %s\n'%(arg)
				for a in self.args[arg]['sub'].keys():
					print ' %s \t %s'%(a,self.args[arg]['sub'][a]['help'])
			else: print 'Argument %s not found'%(self.sys.argv[2])
		print '\n'

