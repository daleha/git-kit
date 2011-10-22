#system includes
import os

import debug

#3rd party includes
from git import Git
from git import Repo
from git import Repo

class GKRepo(Repo):


	def __init__(self,path,name="gitkit_repo"):
		super(GKRepo,self).__init__(path)
		self.root=path
		self.cmdrunner=self.git
		self.name=name

	
	def _native_exec(self,cmd):	
		rawcomlist=cmd.split(" ")	
		comlist=list()
		for each in rawcomlist:
			comlist.append(each.replace("&S"," "))
			
		debug.log(self.cmdrunner.execute(comlist))
		
	def _gitStashPush(execfunc):
		cmd="git stash"
		self._native_exec(cmd)

	def _gitStashPop(execfunc):
		cmd="git stash apply"
		self._native_exec(cmd)

		
	def _commitAll(repo,msg="Incremental commit"):
		message=message.replace(" ","&S")


	
	def getConfig(self):	
		from git import GitConfigParser
		debug.log(self.configpath)
		return GitConfigParser(self.configpath)._sections

	def writeConfig(self,key,value,isglobal=True):
		pass

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
		return True

	def syncBranch(self,**kwargs):
		


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
		self.remotes=remotes
		self.cache_meta=cachemeta
		
	
		
	def safeSyncBranch(self,repo): #use kwargs
		self.name=kwargs["branch"]
	
		if(not repo.isClean()):
			if(self.cache_meta):
				debug.log("Metadata storage not yet implemented")
				#import metastore
				#metastore.store_metadata()	
			if(kwargs.has_key("cmsg")):
				cmsg=kwargs["cmsg"]
			else:
				cmsg="Incremental Commit"

			repo.gitCommitAll(cmsg)
	
		debug.log("""
			You want me to sync "+brname+", but you migh have given me an 
			unclean working tree ( hopefully you didn't).
			Stashing your tree state.""")
		repo.gitStashPush()

		debug.log("""
			Working tree clean. Local stack may have been pushed""")
		
#		debug.log("""Alright, checking if we need to switch head refs...

#			debug.log("""Switching head refs""")
#			
	
		for remote in remotes:	
			repo.pullRebase(self.name,remote)
#			
			if(remote.isWriteable()):
				_push(self.name,remote)

#		debug.log("""Alright, checking if we need to switch head refs...

#			debug.log("""Switching head refs""")
#		
		debug.log("""
			Alright, you've synch with the specified remotes. Now I'll restore your working tree""")	
		repo.gitStashPop()



	


class Remote:
	def __init__(self,upstream_name,upstream_branch,writable=False,**kwargs):
		self.upstream_name=upstream_name
		self.upstream_branch=upstream_branch
		self.writeable=False
		
		if(kwargs.has_key("url")):
			self.url=kwargs["url"]

	def isWriteable():
		return self.writable

	def pullRebase(self):
			
		self._native_exec("git pull --rebase "+self.upstream_name+" "+self.upstream_branch )
	


	def push(self):
		self._native_exec("git push "+self.upstream_name+" "+self.upstream_branch)
#
		
	

"""
			if(not check):
				print_console("Synching with new remote")
				addRemote(remote)
"""

	
			
			
		

"""

		if(isglobal):
			globalflag=" --global "
		else:
			globalflag=" "
		command=key+" "+value
		command="git config "+globalflag+command
		simple_exec(command,verbose=True)


def gitCommitOneFile(fileToAdd,msg="Single file commit"):
	gitStashPush()
	cmd="git checkout stash@{0} -- "+fileToAdd	
	simple_exec(cmd)
	if(not os.path.lexists(fileToAdd)):
		abort("Cannot add file \""+fileToAdd+"\" does not exist")
	gitAdd(fileToAdd)
	cmd="git commit -m \""+msg+"\""
	print_console(simple_exec(cmd))
	gitStashPop()

def destroy(path):
	cmd= "git filter-branch --tree-filter 'rm -rf "+path+"' HEAD"
	simple_exec(cmd)

def gitPush(brname,remote):
	cmd="git push "+remote+" "+brname
	simple_exec(cmd)
def addRemote(remote=list()):
	cmd="git remote add "+remote[0]+" "+remote[1]
	simple_exec(cmd)

def gitRemove(filePath):
	if(not os.path.lexists(filePath)):
		abort("Cannot remove file \""+filePath+"\" does not exist")

	cmd="git rm -rf "+filePath
	simple_exec(cmd)

def readRemotes():
	output=simple_exec("git remote -v")
	print_console(output)
	remotes=list()
	for line in output:
		tokens=line.split("\t")
		print_console(tokens)
		if(len(tokens)>1 and tokens[1].find(" ")>=0):
			remotes.append((tokens[0],tokens[1].split(" ")[0]))
	print_console(remotes)
	return remotes
		
		
	

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
			warn("Branch "+brname+" is not a local branch")
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

def getGitRoot():
	cmd="git config --get alias.root"
	output =os.popen(cmd).read().strip()
	print_console("Read git root as "+output)

	if(not(os.path.lexists(output))):
		abort("Getting git root failed")

	return output

def writeGitIgnore(line):
	ignorepath=getGitRoot()+"/.gitignore"
	gitignore=open(ignorepath,"a")
	gitignore.write(line+"\n")
	gitignore.flush()
	gitignore.close()
	gitCommitOneFile(ignorepath)

def ignoreExpression(expression):
	
	from lib import prompt_user
	import fnmatch
	matches=list()

 
	rootPath = getGitRoot()
	if(not os.path.isfile(expression)): 
		for root, dirs, files in os.walk(rootPath):
			for filename in files:
				#print filename
				if(fnmatch.fnmatch(filename, expression)):
				#	print ('match'+filename)
					matches.append(os.path.join(root, filename))
	else:
		matches.append(expression)#probably need to doctor the syntax here
	
	print_console("The following files match the expression:")	

	print_console(matches)	
	ignore=prompt_user("Would you like to ignore all of these files?")
	
	if(ignore):
		writeGitIgnore(expression)		
		cmd="git update-index --assume-unchanged"
		simple_exec(cmd)
		delete=prompt_user("Would you like to delete all of these files?\n"+str(matches))
		
	else:
		delete=False

	if(delete):
		for each in matches:
			gitRemove(each)				
		gitCommitAll("Removed the files globbed by previous commit's .gitignore")
"""
