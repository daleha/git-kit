
def gitConfigSetup(repo):
	from setup import setup_gitconfig

	setup_gitconfig(repo)

#used to sync a single branch

def safeSyncBranch(repo,args):


	if(len(args)>0):
		branch=args[0]	
	else:
		branch="master"

	if(len(args)>1):
		cmsg=args[1]	
	else:
		cmsg="Incremental commit"

	
	debug.log("Syncing branch "+branch)

	repo.syncBranch(cmsg=cmsg,branch=branch)


	
def _handHold(repo,**kwargs):
	global METHODS
	handhold=prompt_user("No arguments eh? Want some help?")
	debug.log("Choose from one of: ")
	debug.log(METHODS)
#actuall add handhold stuff
	

global METHODS
METHODS	=dir()[6:]

import debug

from ui import prompt_user

#To Do: finish repo object so it can be easily serializable.
#Add repo management params+wizard (using talk lib)


