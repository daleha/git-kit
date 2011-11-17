import os,sys

#get repo, (self), and perform  full working tree commit (to stash), then branch, update, and branch back and rebase
def updateGitkit():
	from gitlib import GKRepo

	pathname=os.path.dirname(sys.argv[0])
	abspath= os.path.abspath(pathname)

	repo=GKRepo(abspath)
	repo.safeUpdate()

	
