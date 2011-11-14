
import sys
import traceback

global LOG

LOGPATH=".gitkit.log"
PROGRAM=sys.argv[0]

LOG=open(LOGPATH,"w")
LOG.close()

def warn(msg):
	log("Warning: "+msg)
def abort(msg):

	log("Aborting: "+msg)
	shutdown(1)
	
def bail(msg):
	log("Bailing out for safety. Please submit a log (default is .gitlog in cwd) to hameld@cc.umanitoba.ca")
	shutdown(0)

"""
A wrapper function to print a label for a log section.
"""
def label(label,rad=20):
	string=rad*"*"+label+":"+rad*"*"
	writelog(string)	
	

def writelog(obj):
	obj=str(obj)
	LOG = open(LOGPATH,"a")	
	if (obj!=""):
		LOG.write(obj+"\n")
		LOG.close()
		print(obj)


def log(line,**kwargs):
	if line==None:
		return

	line=">>"+str(line)
	writelog(line)	

	for arg in kwargs:
		writelog("Object key \n\t%s:\nhas value:\n\t%s" % (arg, kwargs[arg]))
		

def shutdown(rc):
	if(rc==1):
		log("Shut down normally")
	else:
		log("Exitting on error code "+str(rc))

	sys.exit(rc)
	#CONSOLE.shutdown()
		


