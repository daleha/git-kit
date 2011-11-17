#system includes
import os

import debug

#3rd party includes
from git import Git
from git import Repo
from git import Remote
from git.exc import GitCommandError


from gkconfig import *

def getRepos():
	repos=list()
	for repocfg in getRepoConfigs():
		repos.append(GKRepo(repocfg))

#	repoconf=GKRepoConfig()
#	repos.append(GKRepo(repoconf))

	return repos

class GKRepo(Repo):


	def __init__(self,repoconfig=None,submodule=None):
		
		if(not submodule):
			path=repoconfig.repopath
			super(GKRepo,self).__init__(path)
			self.root=path
			self.cmdrunner=self.git
			self.name=repoconfig.reponame
		else:
			path=submodule.config_reader().get_value('path')
			super(GKRepo,self).__init__(path)
			self.root=path
			self.cmdrunner=submodule.module().git
			self.name=submodule.name

		self.gkbranches=dict()
		self.gkremotes=dict()

		self._loadConfig(repoconfig)

			
	def _loadConfig(self,repoconfig):
		#load data for new remotes, assuming default values	
		for remote in self.remotes:
			default=GKRemoteConfig()
			default.readConfigFromRemote(remote)
			self.gkremotes[remote.name]=GKRemote(self,default)
	
		#load data for new branches, assuming default values	
		for branch in self.branches:
			default=GKBranchConfig()
			default.readConfigFromBranch(branch)
			self.gkbranches[branch.name]=GKBranch(self,default)


		if(repoconfig!=None):#override default values here
			remoteCfgs=repoconfig.getRemoteConfigs()
			
			#load stored remotes
			for remote in remoteCfgs:
				conf=GKRemoteConfig()
				conf.readConfigFromJson(remote,remoteCfgs[remote])
				self.gkremotes[remote]=GKRemote(self,conf)
	
			branchCfgs=repoconfig.getBranchConfigs()

			#load stored branches
			for branch in branchCfgs:
				conf=GKBranchConfig()
				conf.readConfigFromJson(branch,branchCfgs[branch])
				self.gkbranches[branch]=GKBranch(self,conf)
		


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
		
	def backupMetadata(self):
		import metastore
		metastore.backupMetaData(self)
	
	def restoreMetadata(self):
		import metastore
		
		metastore.restoreMetaData(self)

			


	def gitStashPush(self):
		cmd="git stash"
		self._native_exec(cmd)

	def gitStashPop(self):
		cmd="git stash apply"
		self._native_exec(cmd)

		
	def gitCommitAll(self,cmsg):
		cmd=["git", "commit", "-a", "-m", cmsg]

		try:
			self._native_exec(cmd)
		except GitCommandError:
			debug.warn("There was nothing to do")


	def addWorkingTree(self):
		cwd=os.getcwd()
		os.chdir(cwd)
		
		for each in os.path.listdir(self.root):
			self._addFile(each)

		os.chdir(cwd)


	
	#is working tree clean?
	def isClean(self):
		return not self.is_dirty()

	"""
	Used to provide a means of synching a single branch in the repo
	"""
	def syncAll(self,**kwargs):
		debug.log("Updating submodules")
		self.submodule_update()
		for each in self.submodules:
			subrepo=GKRepo(submodule=each)
			debug.log("Syncing submodule "+subrepo.name)
			subrepo.syncAll(cmsg=kwargs["cmsg"])
			

		for branch in self.gkbranches:
			toSync=self.gkbranches[branch]
			toSync.safeSyncBranch(cmsg=kwargs["cmsg"])

	def safeUpdate():
		cmsg="Performed gitkit safe update"
		debug.log("Performing update on repo "+self.name)

	

		self.gitCommitAll()

		for each in self.submodules:#recurse down into all *tracked* submodules	
			debug.log("Updating submodule "+subrepo.name)
			subrepo.syncAll(cmsg)
			

		for branch in self.branches:
			toSync=Branch(self,branchcfg)
			toSync.safeUpdateBranch(cmsg)


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
			


class GKBranch:

	def __init__(self,repo,branchcfg):
		self.repo=repo
		self.name=branchcfg.name
		self.cachemeta=branchcfg.cachemeta
		

	#accepts cmsg, and branch name		
	def safeSyncBranch(self,**kwargs): #use kwargs
	
#		debug.log("""Alright, checking if we need to switch head refs...

#			debug.log("""Switching head refs""")
#			

#if we do need to switch, we will first back up the current state of the current branch.
		if(kwargs.has_key("cmsg")):
			cmsg=kwargs["cmsg"]
		else:
			cmsg="Incremental Commit"

		if(self.cachemeta):
			debug.log("Caching metadata")
			self.repo.backupMetaData()
		
		self.repo.gitCommitAll(cmsg)

	
		for remote in self.repo.gkremotes:	
			toSync=self.repo.gkremotes[remote]
			toSync.pullRebase(self)
			if(toSync.isWriteable()):
				toSync.push(self)
			else:
				debug.warn("Remote :"+toSync.name+" is not writeable - cannot sync!")
			

#		debug.log("""Alright, checking if we need to switch head refs...

#			debug.log("""Switching head refs""")
#		


	def getFiles(self):
		return self.git.ls_files().split("\n")

	def safeUpdateBranch(self,cmsg):	

		if(not self.repo.isClean()):
			warn("Staging area not clean: you will lose all pending changes to tracked content.")



		if(self.cache_meta):
			repo.backupMetaData()
			
		self.repo.gitCommitAll(cmsg)
	#switch to each	

	
		for remote in self.repo.gkremotes:	
			toUpdate=self.repo.gkrepotes[remote]
			toUpdate.pullRebase(self)
		
	def safeCheckout(self):	
		self.repo.gitAddAll()
		self.repo.gitCommitAll()	


	def _checkout(self):
		self.repo.git.checkout(self.name)		

"""
Fixme: this should extend the git python Remote object, so that it can use those apis instead of re-implementing them

"""
class GKRemote:
	def __init__(self,repo,remoteconfig):
	#read config	
		self.name=remoteconfig.name
		self.writeable=remoteconfig.writeable
		self.repo=repo
		self._exec=repo.getExecFunc()
		

	def isWriteable(self):
		return self.writeable

	def pullRebase(self,branch):
			debug.log("Rebasing changes from remote "+self.name+" onto "+branch.name)
			self._exec("git pull --rebase "+self.name+" "+branch.name )
	


	def push(self,branch):
		if(self.writeable):
			debug.log("writing to remote "+self.name+" "+branch.name)
			self._exec("git push "+self.name+" "+branch.name)
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
