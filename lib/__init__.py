"""
Lib acts as the main bootstrap code for a python lib
Important: call init with main as a function pointer argument for bootstrapping to occur
"""



import sys
import os
import traceback
import time

global BASEDIR

EXCLUDES=(".git","github/tests")



#wrapper to easily exclude anything in excludes	
#returns: shoud exclude?(bool)
def exclude(path):
	exclude=False

	for each in EXCLUDES:
		if (path.find(each)>=0):
			return True

	return exclude

#recursively crawl a directory,appending all dirs rooted at BASEDIR to system path
def append_all(dir=None):

	def appendPath(path):
		path = os.path.abspath(path)

		if(sys.platform == "win32" ):
			path = path.lower()
		sys.path.insert(0,path)
#		print "Appending "+path


	
	if (dir==None):
		global BASEDIR
		dir=os.path.join(BASEDIR,"lib")

	appendPath(dir)
		
	for each in os.listdir(dir):
		path = os.path.join(dir,each)

		if (os.path.isdir(path) and not exclude(path)):
			append_all(path)


#Parse argdict is not yet finished. It does pre-processing on sys.argv, so that it passes an easier to use object to main
def parse_argdict():

	args=sys.argv
	#(split sys.argv to git arguments, map keys (switches) to values)
	request=list()
	#name=inspect.getfile( inspect.currentframe() )
	#name=sys.argv[0]
	if (len(args)<=1):
		request=args
	else:
		request=args[1:]

	return request
"""
this method handles all runtime scaffolding, to keep the project's main method cleaner.
It handles logging, debugging, and performance metrics (raw runtime)	
This basically establishes the runtime environment for the project, and is intended to be
useable with any project, handling common custodial tasks.

Accepts a function pointer, main, as an argument.
"""

def init(main):
	import debug
	rc=1
	try:
	       start = time.time()
	       
	       request=parse_argdict()			
	       main(request)

	       end = time.time()
	       elapsed= end - start
	       min = elapsed/60
	       debug.log("GK command took "+str(min)+" minutes.") 
	       #from bugmail import send_bug
	       #send_bug()
	except:
		rc=0
		err=traceback.format_exc()
		if (err!="None\n"):
			debug.log(err)
	finally:

		debug.shutdown(rc)
	
def boot_strap(main):
	global BASEDIR
	sys.argv[0]             

	pathname = os.path.dirname(sys.argv[0])        
	append_all(pathname)

	print ('full path ='+pathname) 

	BASEDIR=pathname

	init(main)

		
