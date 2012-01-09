import os
import debug


global CONFIGPATH
CONFIGPATH="gitkit.cfg"


class GKWorkspaceConfig:

	def __init__(self):
		pass
		
	def readConfigFromJson(self,name,jsondata):
		import json

		self.name=name
		self.writeable=jsondata[name]["writeable"]




class GKRemoteConfig:
	def __init__(self):
		self.writeable=False

	def readConfigFromJson(self,name,jsondata):
		import json

		self.name=name
		self.writeable=jsondata[name]["writeable"]

	def readConfigFromRemote(self,remote):
		from gitlib import GKRemote
		self.name=remote.name
		if(isinstance (remote,GKRemote)):
			self.writeable=remote.writeable

	def setWriteable(self):
		self.writeable=True

	def serialize(self):
		self.serialized=dict(\
		{\
		"writeable":self.writeable\
		})
		return self.serialized
			
	

class GKBranchConfig:
	def __init__(self):
		self.cachemeta=False
	
	def readConfigFromJson(self,name,jsondata):
		self.name=name	
		self.cachemeta=jsondata[name]["cachemeta"]

	def readConfigFromBranch(self,branch):
		from gitlib import GKBranch
		self.name=branch.name
		if(isinstance( branch, GKBranch)):
			self.cachemeta=branch.cachemeta

	def setCacheMeta(self):
		self.cachemeta=True
	
	def serialize(self):
		self.serialized=dict(\
		{\
		"cachemeta":self.cachemeta\
		})
		return self.serialized
		

class GKRepoConfig:

	def _getSerializedBranchcfgs(self):
		serializedBranches=dict()

		for each in self.branchcfgs:
			serializedBranches[self.branchcfgs[each].name]=self.branchcfgs[each].serialize()
		return serializedBranches

	def _getSerializedRemotecfgs(self):
		serializedRemotes=dict()

		for each in self.remotecfgs:
			serializedRemotes[self.remotecfgs[each].name]=self.remotecfgs[each].serialize()
		return serializedRemotes

	def getBranchConfigs(self):
		return self.branchcfgs

	def getRemoteConfigs(self):
		return self.remotecfgs

	def __init__(self,reponame="genericrepo",repopath=os.getcwd(),cachemeta=True):#scaffolding
		import os
		self.reponame=reponame
		if(os.path.exists(repopath)):
			self.repopath=repopath
		else:
			debug.warn("The path specified "+repopath+ " does not exist")
			self.repopath=""
			
		self.cachemeta=cachemeta

		self.branchcfgs	=dict()	
		self.remotecfgs	=dict()	



	def readConfigFromJsondata(self,name,jsondata):
		self.reponame=name
		self.repopath=jsondata["rootpath"]
		self.cachemeta=jsondata["cachemeta"]

		
		for branchcfg in jsondata["gkbranchcfgs"]:
			self.branchcfgs[branchcfg]=jsondata["gkbranchcfgs"]

		for remotecfg in jsondata["gkremotecfgs"]:
			self.remotecfgs[remotecfg]=jsondata["gkremotecfgs"]
	

	def readConfigFromRepo(self,repo):
		self.reponame=repo.name
		self.repopath=repo.root

		for branch in repo.gkbranches:
			config=GKBranchConfig()
			config.readConfigFromBranch(repo.gkbranches[branch])
			self.branchcfgs[branch]=config
		for remote in repo.gkremotes:
			config=GKRemoteConfig()
			config.readConfigFromRemote(repo.gkremotes[remote])
			self.remotecfgs[remote]=config

		

	def serialize(self):
		self.serialized=dict(\
		{\
		"rootpath":self.repopath,\
		"cachemeta":self.cachemeta,\
		"gkbranchcfgs":self._getSerializedBranchcfgs(),\
		"gkremotecfgs":self._getSerializedRemotecfgs()\
		})
		return self.serialized
"""
Public APIS:
	
"""

def writeWorkspaceToRepo():
	pass

def getWorkspaceConfig():	
	jsondata=_parseConfigToDict()

	workspaceConfigs = list()	

	for each in jsondata["workspaces"]:
		workspaceConfigs.append(_getWorkspaceConfig(each,jsondata[each])


def writeRepoToJson(repo):
	repoconf=GKRepoConfig()
	repoconf.readConfigFromRepo(repo)
	data = repoconf.serialize()
	jsondata=_parseConfigToDict()

	jsondata["repos"][repo.name]=data
	_writeConfigToFile(jsondata)
		

def getRepoConfigs():
	repoconfigs=list()

	jsondata=_parseConfigToDict()
	
	for each in jsondata["repos"]:
		repoconfigs.append(_getRepoConfig(each,jsondata["repos"]))
	return repoconfigs

"""
Private APIS
"""
def _getRepoConfig(reponame,jsondata):
	repoconf=GKRepoConfig()
	repoconf.readConfigFromJsondata(reponame,jsondata[reponame])
	return repoconf



def _parseConfigToDict():
	import json
	rawdata=_readConfigFromFile()
	mappings=json.loads(rawdata)
	return dict(mappings)	

def _readConfigFromFile():
	jsondata=""
	if(os.path.exists(CONFIGPATH)):
		data=open(CONFIGPATH)
		jsondata= data.read()
	if(jsondata.strip()==""):
		import json
		jsondata=json.dumps({"repos":{}})
	#debug.log("jsondata:"+jsondata)

	return jsondata

def _writeConfigToFile(jsondata):
	import json
	datastr=json.dumps(jsondata,sort_keys=True, indent=4)
	#debug.log("Writing datastr"+datastr)
	
	configfile=open(CONFIGPATH,"w")
	configfile.write(datastr)
	configfile.flush()
	configfile.close()

