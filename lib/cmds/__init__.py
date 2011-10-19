import debug

def gitConfigSetup(repo):
	from setup import setup_gitconfig

	setup_gitconfig(repo)


def syncBranch(repo,**kwargs):
	branch=kwargs["branch"]
	debug.log("Syncing branch "+branch)
	message=kwargs["message"]

	if(message!=""):
		repo.syncBranch(branch,message)
	else:
		debug.log("Using message "+message)
		repo.syncBranch(branch)



