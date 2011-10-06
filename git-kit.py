#!/usr/bin/env python

#make a check for python verion
#need to cleanup threads, can't quick restart
'''
Created on Jun 14, 2010

@modified: Jun 14, 2010
@author: Dale Hamel
@contact: umhameld@cc.umanitoba.ca
'''
#python libs
import traceback
import os
import sys
import time

#move these imports
import shutil
import subprocess
import tarfile
from subprocess import *

#custom lib imports

from setup import setup

from lib import shutdown
from lib import print_console
from lib import warn
from lib import abort
from workflow import *
from gitlib import *

ACTIONS=("help","sync","userconf")

def printHelp():
	print(ACTIONS)

def parse_argdict():
	args=sys.argv
	#(split sys.argv to git arguments, map keys (switches) to values)
	request=list()
	name=inspect.getfile( inspect.currentframe() )
	base=args.index(name)
	if (len(args)<=base+1):
		abort("Not enough arguments. No help yet, sorry")
	else:
		action=args[base+1]
		request.append(action)

	return request
			
def main(request):
	
	#todo: add config check for default config options	
	if (len(request)!=0):
		action=request[0]
		if(action=="userconf"):
			setup()
		elif(action=="sync"):
			#synch should actually call gitSynch, testing for now
			syncBranch(brname="master")
		elif(action=="help"):
			printHelp()
			
	else:
		abort("Nothing to do")
	

def init(request):
	verbose=False#read from dict

	try:
		if (verbose):
			start = time.time()

		main(request)
		
		if (verbose):

			end = time.time()
			elapsed= end - start
			min = elapsed/60
			print_console("git command took "+str(min)+" minutes.")

#		showCustomDoc()

	except:
		
		err=traceback.format_exc()
		print_console(err)
		#from bugmail import send_bug
		#send_bug()

	finally:
		shutdown()



if __name__ == "__main__":
	init(parse_argdict())
