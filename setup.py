from lib import prompt_user
from lib import print_console 

from lib import guessUsername

from workflow import writeConfig



"""
Obviously you will need git, I will leave it you to you to install that for the time being.

"""

#setup tracking branches by default!!!
def setup_gitconfig():
	print_console("Setting up git configuration")
	
	guessedRight=prompt_user("Is your (full) name \""+guessUsername()+"\"?")
	if(not guessedRight):
		username=prompt_user("Please enter your name",False)
	else:
		username=guessUsername()
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


def setup(opts=list()):

	if (len(opts)>=0):
		for each in opts:
			#do opt
			pass
	
	setup_gitconfig()
	

#(called by main core)
#purpose is to collect user info, set config files (can be called at any time, reads info from config file by default

if __name__=="__main__":
	setup()
	
