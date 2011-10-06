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

def parse_argdict():
	#(split sys.argv to git arguments, map keys (switches) to values)
	pass

def main():
	setup()

def init(argdict):
	verbose=False#read from dict

	try:
		if (verbose):
			start = time.time()

		main()
		
		if (verbose):

			end = time.time()
			elapsed= end - start
			min = elapsed/60
			print_console("git command took "+str(min)+" minutes.")

#		JOptionPane.showMessageDialog(None,"Please bookmark BIRCH custom documentation, which will appear in a web browser")
#		showCustomDoc()
#		JOptionPane.showMessageDialog(None,"Installation completed successfully.")

	except:
		
	#	print_console(err)
		err=traceback.format_exc()
		print_console(err)
		#ARGS.log_file.flush()
		#ARGS.log_file.close()
		#from bugmail import send_bug
		#send_bug()
	#	JOptionPane.showMessageDialog(None,"Installation failed, please try again and submit install log as a bug report.")

	finally:
		shutdown()



if __name__ == "__main__":
	sys.exit(init(parse_argdict()))
