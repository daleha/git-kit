
# The lib directory:

The lib module itself contains code used to bootstrap the rest of the modules, and establish the project namespace.
By default, all folders in the lib folder are added when lib's init module is called. This is the method that should be called by
the main thread, with the only argument being a pointer to the project's main method. This effectively allows it to bootstrap any program.

1. Write your lib, exposing any public APIS you want to call.
1. Put all libs in the lib folder, in their own directory (dirname=namespace). Name the script __init__.py. 
1. Put call your lib from your script by importing it

Example: `mkdir mylib && echo "mycode" > mylib/__init__.py && echo "import mylib \n mylib.mycoolfunction" > mymain.py && python mymain.py`

## Libs currently in use:

+ Cmds : This is the higest level API, mapping 1-to-1 function pointers with command line APIs
+ Config: This is the configuration class. It handles configuration logic. Currently, it does not have a permanent model layer,
though this is planned to be implemented in pretty json.
+ debug: This hosts the debug library, including logging methods. 
+ Git: The git python api
+ Gitlib: The gitkit porcelain, wrapping Git python and eventually dulwich.
+ metastore: implementation of metadata storage, to be used in git repo hooks
+ ui: The UI wrappers. Currently, the api uses only a CLI interface, but these public APIS should be portable to a Gui, such as tkinter or swing.


## Future use/heavy lifting API's:

The following libs are not currently used, but will
+ dulwich: This is the dulwich low-level git API, for pythonish implementations of low-level git porcelain, including primitives.
+ gkdulcom
