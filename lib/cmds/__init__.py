import debug

def gitConfigSetup(repo):
	from setup import setup_gitconfig

	setup_gitconfig(repo)


def syncBranch(repo,**kwargs):
	branch=kwargs["branch"]
	debug.log("Syncing branch "+branch)
	repo.syncBranch(branch)



