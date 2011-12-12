# __init__.py
# Copyright (C) 2008, 2009 Michael Trier (mtrier@gmail.com) and contributors
#
# This module is part of GitPyPython and is released under
# the BSD License: http://www.opensource.org/licenses/bsd-license.php

import os
import sys
import inspect

__version__ = 'git'


#{ Initialization
def _init_externals():
	"""Initialize external projects by putting them into the path"""
	#sys.path.append(os.path.join(os.path.dirname(__file__), 'ext', 'gitdb'))
	import gitdb
	#END verify import
	
#} END initialization

#################
_init_externals()
#################

#{ Imports

from pygit.config import GitPyConfigParser
from pygit.objects import *
from pygit.refs import *
from pygit.diff import *
from pygit.exc import *
from pygit.db import *
from pygit.cmd import GitPy
from pygit.repo import Repo
from pygit.remote import *
from pygit.index import *
from pygit.util import (
						LockFile, 
						BlockingLockFile, 
						Stats,
						Actor
						)

#} END imports

__all__ = [ name for name, obj in locals().items()
			if not (name.startswith('_') or inspect.ismodule(obj)) ]
			
