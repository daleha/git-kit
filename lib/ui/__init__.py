

"""
Prompts the user. Assumes yes/no, if not, then select from options, fallback to string input
"""
def prompt_user(message,isbool=True,opts=list()):

	def isvalid(answer):
		if (isbool):
			return answer=="y" or answer == "n"
		else:
			if (len(opts)==0):
				return answer!=""	
			else:
				try:
					valid= opts.index(answer)>=0	
				except:	
					valid=False
				finally:
					return valid
	if (isbool):
		optlist=" (y/n): "
	elif(len(opts)>0):
		optlist=" "+str(opts)+": "
	else:
		optlist=" (Please enter a value): "
	answer=""

	while(not isvalid(answer)):
		answer=raw_input(message+optlist)
	if(isbool):
		return answer=="y"
	else:
		return answer
		

