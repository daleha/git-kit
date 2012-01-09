"""
The cmds module contains the highest level APIs, mapping command line arguments to function calls directly
"""


"""
Please put all global namespace imports at the bottom of the file.
"""


"""
Run setup on a repository to start using it with gitkit, and configure various settings
"""
def gitConfigSetup(repos):
	from setup import setup_repos
	from setup import setup_workspaces

	setup_workspaces()
	setup_repos()


def safeUpdate(repos,args):#todo: use args to selectively update/sync
	for repo in repos:
		repo.safeUpdate()

"""
Safely sinc a single branch in a single repo
"""
def safeSyncAll(repos,args):
	for repo in repos:

		if(len(args)>0):
			cmsg=args[0]	
		else:
			cmsg="Incremental commit"

		repo.syncAll(cmsg=cmsg)

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
def _handHold(repos,**kwargs):
	print "Handholding"
	global METHODS
	handhold=prompt_user("No arguments eh? Want some help?",default="Y")

	if(not handhold):
		return
	choice=prompt_user("Enter choice from: ",isbool=False,opts=METHODS)
	
	choiceFunc= globals()[choice]
	if(prompt_user("Do you want to supply arguments to "+choice+"?")):
		args=prompt_user("Please provide arguments for "+choice,isbool=False)
	else:
		args=None
	if(args==None):
		choiceFunc(repos)
	else:
		choiceFunc(repos,args)
#actuall add more handhold,including arguments for each func
	

global METHODS
METHODS	=dir()[6:]

import debug

from ui import prompt_user

#To Do: finish repo object so it can be easily serializable.
#Add repo management params+wizard (using talk lib)


