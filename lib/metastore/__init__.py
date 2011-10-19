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
		print "path "+fullpath+" does not exist"
	


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
		print "file "+file+" does not exist"
	
	return time

def backupMetaData(path,timeCachePath=".git_cache_time",permCachePath=".git_cache_meta"):
	
	os.chdir(path)
	try:
		pipe = Popen("git ls-files", shell=True,  stdout=PIPE).stdout
	except:
		pipe = popen("git ls-files").read().split("\n")
	timecache=open(timeCachePath,"w")
	permcache=open(permCachePath,"w")
	
	for file in pipe:
		file=file.strip()
		path=os.getcwd()+"/"+file

		if os.path.exists(path):
			times=backupTime(path)
			mode = os.stat(path)[ST_MODE]
			timestamp=(file+","+times[0]+","+times[1]+"\n")
			permstamp=backupPerms(file,mode)
			timecache.write(timestamp)
			permcache.write(permstamp)
	
			
	permcache.flush()
	permcache.close()
	timecache.flush()
	timecache.close()
	
def restoreMetaData(path,timeCachePath=".git_cache_time",permCachePath=".git_cache_meta"):
	os.chdir(path)

	timecache=open(path+"/"+timeCachePath,"r")
	permcache=open(path+"/"+permCachePath,"r")

	print "restoring perms"
	for line in permcache:
		restorePerms(line,basepath=path)


	print "restoring times"
	for line in timecache:
		line=line.strip()
		tokens=line.split(",")
		fname=tokens[0]
		atime=int(tokens[1].split(".")[0])
		mtime=int(tokens[2].split(".")[0])
		restoreTime(path+"/"+fname,atime,mtime)


if __name__ == '__main__':
	print "Usage: python metastore GIT_REPO_ROOT [r]\n\tAdd optional r param to restore, else backup"
	try:
		sys.argv.index("r")
		print "restoring metadata"
		restoreMetaData(sys.argv[1])
	except ValueError:
		print "backing up metadata"
		backupMetaData(sys.argv[1])
	except:
		err=traceback.format_exc()
		print err


		
