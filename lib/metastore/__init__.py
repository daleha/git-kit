
import debug


import os, sys
from stat import *
try:
	from subprocess import *
except:
	from os import popen
import traceback


def backupPerms(path,mode):
	perms="0"+str((S_IRWXU & mode)>>6)+str((S_IRWXG & mode)>>3)+str(S_IRWXO & mode)
	line="chmod %(perm)s \"%(path)s\"\n"%{"perm":perms,"path":path}
#	print line
	return line


def restorePerms(line,basepath=os.getcwd()):
	line=line.strip()
	space1=line.find(" ")
	space2=line.find(" ",space1,len(line))
	maskstr=line[space1+1:space1+space2]
	mask=(int(maskstr[1])<<6)|(int(maskstr[2])<<3)|(int(maskstr[3]))
	path=line[space1+space2+2:len(line)-1]
	fullpath=basepath+"/"+path
#	print "Restoring perms for file "+fullpath
	if (os.path.exists(fullpath)):
		os.chmod(fullpath,mask)
#		print "permissions restored"
	else:
		debug.warn ("path "+fullpath+" does not exist")
	


def restoreTime(file,atime,mtime):

	if (os.path.exists(file)):
#		print "restoring time for file "+file
		os.utime(file,(atime,mtime))

def backupTime(file):

	if (os.path.exists(file)):
		atime=str(os.stat(file).st_atime)
		mtime=str(os.stat(file).st_mtime)
		time=(atime,mtime)
	else:
		debug.warn ("file "+file+" does not exist")
	
	return time

def backupMetaData(repo,timeCachePath=".git_cache_time",permCachePath=".git_cache_meta"):
	import git	

	basepath=repo.root

	cwd=os.chdir(basepath)

	timecache=open(os.path.join(basepath,timeCachePath),"w")
	permcache=open(os.path.join(basepath,permCachePath),"w")

	debug.log("Backing up metadata for repo "+repo.name)	

	for line in repo.getFiles():
		filepath=os.path.join(basepath,line)

		if(os.path.exists(filepath)):

			times=backupTime(filepath)
			mode = os.stat(filepath)[ST_MODE]
			timestamp=(line+","+times[0]+","+times[1]+"\n")
			permstamp=backupPerms(line,mode)
			timecache.write(timestamp)
			permcache.write(permstamp)
	
			
	permcache.flush()
	permcache.close()

	timecache.flush()
	timecache.close()
	debug.log("Metadata backed up")

	os.chdir(cwd)
	
def restoreMetaData(repo,timeCachePath=".git_cache_time",permCachePath=".git_cache_meta"):
	cwd=os.getcwd()
	path=repo.root
	os.chdir(path)

	timecache=open(path+"/"+timeCachePath,"r")
	permcache=open(path+"/"+permCachePath,"r")

	debug.log ("restoring perms on repo "+repo.name)
	for line in permcache:
		restorePerms(line,basepath=path)


	debug.log ("restoring times on repo "+repo.name)

	for line in timecache:
		line=line.strip()
		tokens=line.split(",")
		fname=tokens[0]
		atime=int(tokens[1].split(".")[0])
		mtime=int(tokens[2].split(".")[0])
		restoreTime(path+"/"+fname,atime,mtime)

	debug.log("Metadata restored")
	os.chdir(cwd)

