from lib import print_console
from lib import stream_exec

"""
->checkout branch at stable tag
->actions:

->action ->synonyms
->create -> add, +, 
	-> branches, commits, tags
->destroy-> del, [-f, -rf] (revwalk, prune, garbage collect)
	-> branches, commits, tags
->archive-> rm, arch
	->wrapper for rebase

->synchronize [all]
	->synchs all submodules with all repos (create reposynch action)
	
->add -> track, watch, 


"""



#
#def createBranch(branchname):
#def switchbranch(branchname,create=True):
#def createCommit(message):
#
#def clearCache(): 
#
#def updateAll():
#
#def synchAll():
#
def destroy(path):
	cmd= "git filter-branch --tree-filter 'rm -rf "+path+"' HEAD"
#	
#
def writeConfig(key,value,isglobal=True):
	if(isglobal):
		globalflag=" --global "
	else:
		globalflag=" "
	command=key+" "+value
	command="git config "+command+globalflag
	stream_exec(command,verbose=True)
#
#def run(command,args):
#	commands=command(*args)
#	for commands in commands:
#		
