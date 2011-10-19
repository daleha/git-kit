import sys
import os
import traceback
import time

global BASEDIR

EXCLUDES=(".git","github/tests")
	
def exclude(path):
	exclude=False

	for each in EXCLUDES:
		if (path.find(each)>=0):
			return True

	return exclude

def append_all(dir=None):

	
	if (dir==None):
		global BASEDIR
		dir=os.path.join(BASEDIR,"lib")
		sys.path.append(dir)

	for each in os.listdir(dir):
		path=os.path.join(dir,each)
		if (os.path.isdir(path) and not exclude(path)):
			sys.path.insert(0,path)
			append_all(path)

def parse_argdict():

	args=sys.argv
	#(split sys.argv to git arguments, map keys (switches) to values)
	request=list()
	#name=inspect.getfile( inspect.currentframe() )
	name=sys.argv[0]
	if (len(args)<=1):
		debug.abort("Not enough arguments. No help yet, sorry")
	else:
		request=args[1:]

	return request
	
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

	finally:
		err=traceback.format_exc()
		if (err!="None\n"):
			debug.log(err)
		debug.shutdown(rc)
	
def boot_strap(main):
	global BASEDIR
	sys.argv[0]             

	pathname = os.path.dirname(sys.argv[0])        
	abspath= os.path.abspath(pathname)

	#print ('full path ='+ abspath)

	BASEDIR=abspath
	append_all()
	init(main)

		
