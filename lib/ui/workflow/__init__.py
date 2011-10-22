#sysincludes
import os
import inspect

#custincludes
import lib
from lib import warn
from lib import abort
from lib import log_flush
from lib import print_console
from lib import stream_exec
from lib import simple_exec

from gitlib import *

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


def gitBranchSync(brdict=dict()):
	for br in brdict:
		k=0
		v=1

		brname=brdict[k]
		remotelist=brdict[v]	

		print_console("Adding branch "+brname+", with the following remotes:")
		for remote in remotelist:
			print ("\tAdding remote "+remote)
	
		
def startBranch(brname,remoteMap=list()):
	
	exists=branchExists(brname)
	if(exists):
		abort("Ack! The branch you wanted to create already exists. Please either synch, or destroy it.")
	
	cmd="git checkout -b "+brname
	simple_exec(cmd)

	for remote in remotes:
		cmd="git remote add "+remote[0]+" "+remote[1]
		
	
def syncBranch(brname,commitmsg="Incremental Commit",remotes=list(),greedy=True):
	exists=branchExists(brname)
	
	if(exists):
		print_console("Branch "+brname+" exists synching with remotes")

		
	else:
		print_console("Branch "+brname+" does not exist, synching from remotes")

	if (len(remotes)==0):
		remotes=readRemotes()		

	for remote in remotes:

		check=checkRemote(remote)
		if(not check):
			print_console("Synching from with new remote")
			addRemote(remote)
		gitStashPush()
		pullRebase(brname,remote[1])
		gitStashPop()

		if(greedy==True):
			gitCommitAll(commitmsg)

		gitPush(brname,remote[0])	

	
			
			

		

		

"""
the braches dict accepts a string branch name, and the list of remotes to synch it to.(string to list map)
"""
def gitSync(wrkdir=os.getcwd(),branches=dict(),create=True,trackMaster=True,rebase=True,greedy=True):
	OLDPWD=os.getcwd()

	#dir sanity check
	if (os.path.lexists(wrkdir)):
		os.chdir(wrkdir)	
	else:
		warn("wrkdir param to gitSync not a valid directory: Falling back to cwd")
		wrkdir=os.getcwd()

	contents=os.listdir(wrkdir)

	if (len(contents)!=0 and not create):
		abort("You are trying to synch something that does not contain a git repo. Pass create flag to init")
	elif(create):
		createRepo()	
			

	brdict=branches.items()
	gitBranchSync(brdict)
	

	os.chdir(OLDPWD)
	
		

#def synchAll():
#
#	
#
#
#def run(command,args):
#	commands=command(*args)
#	for commands in commands:
#		
