#system imports
import os
import getpass



import debug
from ui import prompt_user

from gitlib import GKRepo
from gitlib import getRepos

from gkconfig import GKRepoConfig

#from workflow import writeConfig



"""
Obviously you will need git, I will leave it you to you to install that for the time being.

"""


def guessUsername():
	return getpass.getuser()

#setup tracking branches by default!!!
def setup_gitconfig(repo):
	debug.log("Setting up git configuration")

	guessedRight=prompt_user("Is your (full) name \""+guessUsername()+"\"?")
	if(not guessedRight):
		username=prompt_user("Please enter your name",False)
	else:
		username=guessUsername()
"""
	writeConfig("user.name",username) 
	writeConfig("user.email",prompt_user("What is your email?",isbool=False))
	writeConfig("branch.master.remote","origin")
	writeConfig("branch.master.merge","refs/heads/master")

	aliases=prompt_user("Would you like to use default aliases?")
	if(aliases==True):
		writeConfig("alias.st","status")
		writeConfig("alias.ci","commit")
		writeConfig("alias.co","checkout")
		writeConfig("alias.br","branch")
"""

def configure_repo(repo):
	debug.log("stub!")
	if(prompt_user("Do you want to change to root path?")):
		newpath= prompt_user("What should the root path be?",isbool=False)
		while (not os.path.exists(newpath)):
			newpath= prompt_user("Invalid path. What should the root path be?",isbool=False)
		repo.rootpath=newpath

	for remote in repo.remotes:
		writeable = prompt_user("Do you have write access to the remote \""+remote.name+"\" ("+remote.url+") for this repository?")
		repo.gkremotes[remote.name].setWriteable(writeable)
	repo.cachemeta = prompt_user("Do you want to track metadata (filesystem attributes like date modified, octal permiossions) for this repository?")

	import gkconfig
	gkconfig.writeRepoToJson(repo)	

def create_repo(rootPath):
	import gkconfig

	reponame=  prompt_user("What would you like to call this repo?",isbool=False)
	repo = GKRepo(GKRepoConfig(reponame,rootPath))
	gkconfig.writeRepoToJson(repo)	
	

def setup_repos(opts=list()):

	if (len(opts)>=0):
		for each in opts:
			#do opt
			pass

	createRepo = prompt_user("Would you like to configure a new repository? ")


	if (createRepo):
		rootPath = prompt_user ("Please enter the root path of the repository",isbool=False) 
		rootPath= os.path.abspath(rootPath)
		while (not os.path.exists (rootPath)):
			rootPath = prompt_user ("Please enter a valid path, "+rootPath+" does not exist, or contains envalid syntax.",isbool=False)
		
		create_repo( rootPath )
	
	repos = getRepos()
	selection = prompt_user("Which repo would you like to configure?",opts=repos,isbool=False)
	configure_repo(selection)

#(called by main core)
#purpose is to collect user info, set config files (can be called at any time, reads info from config file by default

if __name__=="__main__":
	setup()
	
