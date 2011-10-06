import lib
from lib import warn
from lib import abort
from lib import print_console
from lib import stream_exec
from lib import simple_exec

def gitCommitAll(msg="Incremental Comitt"):
	cmd="git add . && git commit -a -m '"+msg+"'"
	simple_exec(cmd)
	

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

def readRemotes():
	output=simple_exec("git remote -v")
	print(output)
	remotes=list()
	for line in output:
		tokens=line.split("\t")
		remotes.append((tokens[0],tokens[1].split(" ")[0]))
	print (remotes)
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
	cmd="git init && git add ."
	stream_exec(cmd)	

	if(len(contents)!=0 ):
		log_flush()
		gitAdd(lib.LOG)

	cmd="git commit -a -m 'initialized git repository. Congratulations!'"
	stream_exec(cmd)


