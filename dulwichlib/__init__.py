from lib import *

from dulwich.objects import *

from dulwich.repo import Repo


class GKRepo(Repo):
	def __init__(self,path):
		super(GKRepo,self).__init__()
		self.exclude_patterns = list()

		self.remotes_keys = list()
		self.remotes_dict = dict()

		self.branches_names = list()
		self.branches_keys = list()
		self.branches_dict = dict()

		self.heads_keys = list()
		self.heads_dict = dict()

		self.tags_keys = list()
		self.tags_dict  = dict()

		self.config_dict = dict()
	
"""
Stages a file in index
(glob blob wrapper)
"""	
	def gkStage(path=str()):
		if(os.path.lexists(path)):
			if (os.path.isdir(path)):
				contents=os.listdir(path)
				for each in contents:
					gkStage(os.path.join(path,each))
			elif(os.path.isfile(path)):
				if(not _isIgnored(repo,path)):
					files=list()
					files.append(path)
					super(GKRepo,self).stage(files)


	def addBranch(branch):
		self.branches_names.append(branch.name)
		self.branches_keys.append(branch.id)
		self.branches_dict[id]=branch
	
	def 	
				

	def _isIgnored(repo,path=str()):
"""
	ignorepath=os.path.join(repo.path,".gitignore") //should get blob from commit using get_object(r.head()).tree
	if(os.path.lexists(ignorepath)):
		ignore=open(ignorepath)
		for line in ignore:
			line=line.trim()
			if len(line)>0 and line[0]!="#":
				#need to add negate and dir support as per .gitignore spec
				if(fnmatch.fnmatch(filename, expression)):
					return True
"""#not ready yet...
				
		
		return False


	
	
class Branch:
	
	def __init__(self,name,headref,parent=None):
		self.name=name
		self.headref=headref
		self.reflog = list()
		
		if (parent!=None):
			warn("No parent to inherit from, this branch \""+branch+"\"has no reflog")
			self.reflog=parent.reflog

		
	def addCommit(commit):
		self.reflog.insert(0,commit)

	
