#system includes
import os

import lib
from lib import warn
from lib import abort
from lib import print_console
from lib import stream_exec
from lib import simple_exec

def gitCommitAll(msg="Incremental Comitt"):
	cmd="git add "+getGitRoot()+" && git commit -a -m \""+msg+"\""
	stream_exec(cmd)

def gitCommitOneFile(fileToAdd,msg="Single file commit"):
	gitStashPush()
	cmd="git checkout stash@{0} -- "+fileToAdd	
	stream_exec(cmd)
	if(not os.path.lexists(fileToAdd)):
		abort("Cannot add file \""+fileToAdd+"\" does not exist")
	gitAdd(fileToAdd)
	cmd="git commit -m '"+msg+"'"
	print_console(stream_exec(cmd))
	gitStashPop()

def destroy(path):
	cmd= "git filter-branch --tree-filter 'rm -rf "+path+"' HEAD"
	stream_exec(cmd)

def gitPush(brname,remote):
	cmd="git push "+remote+" "+brname
	stream_exec(cmd)

def pullRebase(brname,remote):
	cmd="git pull --rebase "+remote+" "+brname
	stream_exec(cmd)

def gitStashPush():
	cmd="git stash"
	stream_exec(cmd)

def gitStashPop():
	cmd="git stash apply"
	stream_exec(cmd)

def addRemote(remote=list()):
	cmd="git remote add "+remote[0]+" "+remote[1]
	stream_exec(cmd)

def gitRemove(filePath):
	if(not os.path.lexists(filePath)):
		abort("Cannot remove file \""+filePath+"\" does not exist")

	cmd="git rm -rf "+filePath
	stream_exec(cmd)

def readRemotes():
	output=simple_exec("git remote -v")
	print_console(output)
	remotes=list()
	for line in output:
		tokens=line.split("\t")
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
	output=	stream_exec("git branch -v")
	for line in output:
		if (line.find(brname)>=0):
			print_console ("Local branch "+brname+" exists")
			return True
		else:
			warn("Branch "+brname+" is not a local branch")
			return False
			
	

def gitAdd(path):
	if(os.path.lexists):
		cmd= "git add "+path
	else:
		warn("Warning: the a file that you wanted me to add is not at a valid path")
	stream_exec(cmd)


def createRepo():
	
	print_console("Creating a new git repository in "+workdir)
	cmd="git init "
	stream_exec(cmd)	

	if(len(contents)!=0 ):
		log_flush()
		gitAdd(lib.LOG)

	gitCommitAll('initialized git repository. Congratulations!')
	stream_exec(cmd)

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
		stream_exec(cmd)
		delete=prompt_user("Would you like to delete all of these files?\n"+str(matches))
		
	else:
		delete=False

	if(delete):
		for each in matches:
			gitRemove(each)				
		gitCommitAll("Removed the files globbed by previous commit's .gitignore")


