#system includes
import os

import debug

#3rd party includes
from git import Git
from git import Repo
from git import Repo
from git.exc import GitCommandError

class GKRepo(Repo):


	def __init__(self,path,name="gitkit_repo"):
		super(GKRepo,self).__init__(path)
		self.root=path
		self.cmdrunner=self.git
		self.name=name

	def _readRemotes(self):
		for each in self.remotes:
			newRemote = RemoteUpstreamBranch(_exec=self._native_exec,upstream_name="origin",upstream_branch=kwargs["branch"],writeable=True)#hack
			self.gkremotes.add(newRemote) #should make this a hashtable?

		remotes=list()#hack	
		remotes.append(origin)#hack


	def _native_exec(self,cmd):	
		if (not type(cmd)==list):
			rawcomlist=cmd.split(" ")	
			cmd=list()
			for each in rawcomlist:
				cmd.append(each)
			
		debug.log(self.cmdrunner.execute(cmd))
			
	def _writeGitIgnore(self,line):
		ignorepath=os.path.join(self.root,".gitignore")
		gitignore=open(ignorepath,"a")
		gitignore.write(line+"\n")
		gitignore.flush()
		gitignore.close()
		self._gitCommitOneFile(ignorepath,msg="Wrote to gitignore")

	def _gitCommitOneFile(self,fileToAdd,msg="Single file commit"):

		wasClean=True

		if(not os.path.lexists(fileToAdd)):
			abort("Cannot add file \""+fileToAdd+"\" does not exist")

		if(not self.isClean()):
			self.gitStashPush()
			wasClean=False

			cmd="git checkout stash@{0} -- "+fileToAdd	

			self._native_exec(cmd)
	
		self._addFile(fileToAdd)
		cmd=["git", "commit", "-m", msg]
		debug.log(self._native_exec(cmd))
		if(not wasClean):
			self.gitStashPop()

	def _removeFiles(self,filePaths):
		wasClean=True

		if(not self.isClean()):
			self.gitStashPush()
			wasClean=False

		for each in filePaths:
			cmd="git checkout stash@{0} -- "+each
			self._removeFile(each)				

		self.gitCommitAll(cmsg="Removed the files requested")

		
		if(not wasClean):
			self.gitStashPop()



	def _removeFile(self,filePath):
		if(not os.path.lexists(filePath)):
			abort("Cannot remove file \""+filePath+"\" does not exist")

		cmd="git rm -rf "+filePath
		try:

			self._native_exec(cmd)
		except GitCommandError:
#			debug.warn("filePath could not be removed - this means it is either ignored, or untracked by git")
			self._native_exec("rm -rf "+filePath)
	
	def _addFile(self,filePath):
		if(not os.path.lexists(filePath)):
			abort("Cannot add file \""+filePath+"\" does not exist")
		cmd="git add "+filePath
		self._native_exec(cmd)


	def _destroyFile(self,path):
		cmd= "git filter-branch --tree-filter 'rm -rf "+path+"' HEAD"
		self._native_exec(cmd)
	
	def _destroyOnAllRemotes(self,filesPaths=list()):
		for file in filePaths:	
			_destroyFile(file)
		
		for remote in self.remotes:
			#ripple this change to all remotes
			pass
		



	def gitStashPush(self):
		cmd="git stash"
		self._native_exec(cmd)

	def gitStashPop(self):
		cmd="git stash apply"
		self._native_exec(cmd)

		
	def gitCommitAll(self,cmsg):
		cmd=["git", "commit", "-a", "-m", "\""+cmsg+"\""]

		try:
			self._native_exec(cmd)
		except GitCommandError:
			debug.warn("There was nothing to do")




	
	def getConfig(self):	
		from git import GitConfigParser
		debug.log(self.configpath)
		return GitConfigParser(self.configpath)._sections


	"""
	Will be used to call the repo object serializer, and update the repo by key in config file using config calls to json
	"""
	def writeConfig():
		pass

	"""
	Will be used to call add config params to repo config
	"""
	def writeToConfig(self,key,value,isglobal=True):
		pass

	"""

	List available branches in the repo as branch objects
	"""
	def listBranches(self):
		branches = list()

		for each in self.branches:
			branches.append(each)
	
		debug.log("got branches:",branches=branches)
		return branches
		
	
	def listRemotes(self):
		remotes = list()

		for each in self.remotes:
			remotes.append(each)
	
		debug.log("got remotes:",remotes=remotes)
		print(type(remote))
		return remotes

	#is working tree clean?
	def isClean(self):
		return not self.is_dirty()

	"""
	Used to provide a means of synching a single branch in the repo
	"""
	def syncBranch(self,**kwargs):


		toSync=Branch(self,kwargs["branch"],self.remotes)

		toSync.safeSyncBranch(cmsg=kwargs["cmsg"])

	"""
	Accessor to exec function, for native calls on this repo
	"""
	def getExecFunc(self):
		return self._native_exec

	"""
	Add an expression to the .gitignore, and prompt for deletion
	"""
	def ignoreExpression(self,expression):
		
		from ui import prompt_user
		import fnmatch
		matches=list()

	 
		if(not os.path.isfile(expression)): 
			for root, dirs, files in os.walk(self.root):
				for filename in files:
					#print filename
					if(fnmatch.fnmatch(filename, expression)):
					#	print ('match'+filename)
						matches.append(os.path.join(root, filename))
		else:
			matches.append(expression)#probably need to doctor the syntax here
		
		debug.log("The following files match the expression:")	

		debug.log(matches)	
		ignore=prompt_user("Would you like to ignore all of these files?")
		
		if(ignore):
			self._writeGitIgnore(expression)		
			cmd="git update-index --assume-unchanged"
			self._native_exec(cmd)
			delete=prompt_user("Would you like to delete all of these files?\n"+str(matches))
			
		else:
			delete=False

		if(delete):
			self._removeFiles(matches)
			



#	Fix me: each object should have a getCfgString (make an abstract class for this eventually)	
#	def generateRepoConfJson(self):
#		debug.log("Generating config for repository "+self.name)
#
#		localbranches=self.listBranches()
#		remotes = self.listRemotes()
#		self.remoteRefs= list()
#
#		
#		for remote in remotes:
#			remote.fetch()
#			debug.log("Remote: "+remote.url)
#			for ref in remote.refs:
#				self.remoteRefs.append(ref)
#				debug.log("\t"+ref.remote_name+":"+ref.remote_head)


class Branch:

	def __init__(self,repo,name,remotes=list(),cachemeta=False):
		self.repo=repo
		self.name=name
		self.remotes=remotes#remotes to sync with
		self.cache_meta=cachemeta
		
	
	def getRepoExec(self):
		return self.repo.getExecFunc()
			
	#accepts cmsg, and branch name		
	def safeSyncBranch(self,**kwargs): #use kwargs
	
#		debug.log("""Alright, checking if we need to switch head refs...

#			debug.log("""Switching head refs""")
#			

#if we do need to switch, we will first back up the current state of the current branch.
		if(not self.repo.isClean()):
			if(self.cache_meta):
				debug.log("Metadata storage not yet implemented")
				#import metastore
				#metastore.store_metadata()	
			if(kwargs.has_key("cmsg")):
				cmsg=kwargs["cmsg"]
			else:
				cmsg="Incremental Commit"

			self.repo.gitCommitAll(cmsg)
	
		debug.log("""
			You want me to sync "+brname+", but you migh have given me an 
			unclean working tree ( hopefully you didn't).
			Stashing your tree state.""")

		debug.log("""
			Working tree clean. Local stack may have been pushed""")
	
		for remote in self.remotes:	
			remote.pullRebase()
#			
			if(remote.isWriteable()):
				remote.push()
			

#		debug.log("""Alright, checking if we need to switch head refs...

#			debug.log("""Switching head refs""")
#		
		debug.log("""
			Alright, you've synch with the specified remotes. Now I'll restore your working tree""")	



	

"""
Fixme: this should extend the git python Remote object, so that it can use those apis instead of re-implementing them

"""
class RemoteUpstreamBranch:
	def __init__(self,_exec,upstream_name,upstream_branch,writeable=False,**kwargs):
		self.upstream_name=upstream_name
		self.upstream_branch=upstream_branch
		self.writeable=writeable
		self._exec=_exec
		
		if(kwargs.has_key("url")):
			self.url=kwargs["url"]

	def isWriteable(self):
		return self.writeable

	def pullRebase(self):
			
		self._exec("git pull --rebase "+self.upstream_name+" "+self.upstream_branch )
	


	def push(self):
		debug.log("writing to remote "+self.upstream_name+" "+self.upstream_branch)
		self._exec("git push "+self.upstream_name+" "+self.upstream_branch)
#
		
	

"""
			if(not check):
				print_console("Synching with new remote")
				addRemote(remote)
"""

	
			
			
		

"""

#Storage of old code that needs re-integration (garbage pile, some treassures in here though)


def addRemote(remote=list()):
	cmd="git remote add "+remote[0]+" "+remote[1]
	simple_exec(cmd)
	
		

##NOT DONE FIX ME
def checkRemote(newRemote=list()):
	currRemotes=readRemotes()
	rc=False
	for each in currRemotes:
		if (each[0]==newRemote[0] and each[1]==newRemote[1]):
			rc=True
	#rc=false means remote did not match
	return rc
			

	

def branchExists(brname):
	output=	simple_exec("git branch -v")
	for line in output:
		if (line.find(brname)>=0):
			print_console ("Local branch "+brname+" exists")
			return True
		else:
			self.warn("Branch "+brname+" is not a local branch")
			return False
			
	

	


def createRepo():
	
	print_console("Creating a new git repository in "+workdir)
	cmd="git init "
	simple_exec(cmd)	

	if(len(contents)!=0 ):
		log_flush()
		gitAdd(lib.LOG)

	gitCommitAll('initialized git repository. Congratulations!')
	simple_exec(cmd)
"""
