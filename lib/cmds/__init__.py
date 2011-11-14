"""
The cmds module contains the highest level APIs, mapping command line arguments to function calls directly
"""


"""
Please put all global namespace imports at the bottom of the file.
"""


"""
Run setup on a repository to start using it with gitkit, and configure various settings
"""
def gitConfigSetup(repo):
	from setup import setup_gitconfig

	setup_gitconfig(repo)

"""
Safely sinc a single branch in a single repo
"""
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

"""
Ignore an expression given in a format suitable for fnmatch, or else a
filepath
"""
def ignoreExpression(repo,args):
	if (len(args)!=1):
		debug.abort("Ignore expression didn't get enough args")
	else:
		repo.ignoreExpression(args[0])
		


"""
Provide a list of high level opis to the user
"""	
def _handHold(repo,**kwargs):
	global METHODS
	handhold=prompt_user("No arguments eh? Want some help?")
	if(not handHold):
		return
	choice=prompt_user("Enter choice from: ",isbool=False,opts=METHODS)
	
	choiceFunc= globals()[choice]
	if(prompt_user("Do you want to supply arguments to "+choice+"?")):
		args=prompt_user("Please provide arguments for "+choice,isbool=False)
	else:
		args=None
	if(args==None):
		choiceFunc(repo)
	else:
		choiceFunc(repo,args)
#actuall add more handhold,including arguments for each func
	

global METHODS
METHODS	=dir()[6:]

import debug

from ui import prompt_user

#To Do: finish repo object so it can be easily serializable.
#Add repo management params+wizard (using talk lib)


