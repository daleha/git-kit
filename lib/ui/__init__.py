

"""
Prompts the user. Assumes yes/no, if not, then select from options, fallback to string input
"""
def prompt_user(message,isbool=True,opts=list(),default=None):

	def isvalid(answer):
		if (isbool):
			#answer = answer.strip().replace(" ","")
			valid= (answer == "y" or answer == "n"  or len(answer)==0)
			return valid
		else:
			if (len(opts)==0):
				return answer!=""	
			else:
				if (answer.isdigit() and int(answer) < len(opts)):
					return True
				try:
					valid= opts.index(answer)>=0	
				except:	
					valid=False
				finally:
					return valid

	def getInput(message,opts):
		if (isbool):
			y = "y"
			n = "n"
			
			if (default =="Y"):
				y="Y"
			else:
				n = "N"
				
			optlist=" ("+y+"/"+n+"): "
		elif(len(opts)>0):
			count = 0
			optlist=""

			for opt in opts:
				optlist=optlist+" "+str(opt)+"("+str(count)+")\n"
				count = count+1
			optlist=optlist+"?:"
		else:
			optlist=" (Please enter a value): "

		answer = raw_input(message+optlist)
		return answer

	answer=getInput(message,opts)
	while(not isvalid(answer)):
		answer=getInput(message,opts)
	if (answer.isdigit()):
		return opts[int(answer)]
	if(isbool):
		if (answer == "y"):
			return True
		elif (answer == ""):
			if(default == "Y"):
				return True
			else:
				return False
	else:
		return answer
		

