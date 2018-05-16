import string
import random
import sys

reserved=["break","default","function","return","var","case","delete","if","switch","void","catch","do","in","this","while","const","else","instanceof","throw","with","continue","finally","let","try","debugger","for","new","typeof"]
validChars=string.ascii_letters+string.digits+"_" #these are all the characters that could ever make up a varaible name in js
dotValid="."+validChars
words={}

def isNotReserved(word): #makes sure this word is not a reserved javascript keyword
	for r in reserved:
		if r ==word:
			return(False)
	return(True)

class variable():
	def __init__(self, realname,codename,number=False):
		self.realname=realname
		self.codename=codename
		self.number=number
		self.properties=[]

def cleanFile(file):
	reader=open(file,"r+")
	out=""
	for line in reader:
		if line.find("//")!=-1:
			out+=line[0:line.find("//")]
		else:
			out+=line
	out=out.replace("\n","")
	return(out)

def DFSvars(variable,realname,level=0):
	p=""
	for c in range(0,level):
		p+="\t"
	print(p+variable.realname+" = "+variable.codename)
	if variable.realname==realname:
		return variable
	else:
		for p in variable.properties:
			maybe=DFSvars(p,realname,level+1)
			if maybe !=None:
				return maybe
	return(None)

allTheLists=[]#list of lists

def getDeepLists(variable,reallist=[],fakelist=[]): #creates a list that represents a real variable and one that represents the code name
	#[console,log], [dicks,butts]
	return(None)


def randomString(min=5,max=8):
	out="_" #it has to start with a _ or else it is problematic when it starts with a number
	for x in range(0,random.randint(5,8)):
		r=random.randint(0,len(validChars)-1)
		out+=validChars[r:r+1]
	for w in words: #we make sure that this random string has not already been used
		if w == out or words[w].codename==out or words[w].realname==out:
			return(randomString()) #if it matches, then we have to try again
	for r in reserved:
		if r==out:
			return(randomString())
	return(out)

def getVars(text):
	#gets variable names
	x=0
	openBrackets=False
	openQuotes=False
	openDoubleQuotes=False
	while x<len(text):
		if text[x:x+1]=="[":
			openBrackets=True
		else:
			if text[x:x+1]=="]":
				openBrackets=False
			elif text[x:x+1]=="\"" and openDoubleQuotes is False:
				openDoubleQuotes=True
			elif text[x:x+1]=="\"" and openDoubleQuotes is True:
				openDoubleQuotes=False
			elif text[x:x+1]=="\'" and openQuotes is False:
				openQuotes=True
			elif text[x:x+1]=="\'" and openQuotes is True:
				openQuotes=False
		if openBrackets is False:
			if openQuotes is True or openDoubleQuotes is True:
				x=x+1
				continue
		if validChars.find(text[x:x+1])!=-1:
			word=""
			while validChars.find(text[x:x+1])!=-1 and x<len(text):
				word+=text[x:x+1]
				x=x+1
			try:
				words[word]
			except Exception, e: #if word does not have a dictionary entry
				if isNotReserved(word) == True:
					words[word]=variable(word,randomString())
		else:
			x=x+1

def getProps(text):
	#gets properties names
	x=0
	openBrackets=False
	openQuotes=False
	openDoubleQuotes=False
	while x<len(text):
		if text[x:x+1]=="[":
			openBrackets=True
		else:
			if text[x:x+1]=="]":
				openBrackets=False
			elif text[x:x+1]=="\"" and openDoubleQuotes is False:
				openDoubleQuotes=True
			elif text[x:x+1]=="\"" and openDoubleQuotes is True:
				openDoubleQuotes=False
			elif text[x:x+1]=="\'" and openQuotes is False:
				openQuotes=True
			elif text[x:x+1]=="\'" and openQuotes is True:
				openQuotes=False
		if openBrackets is False:
			if openQuotes is True or openDoubleQuotes is True:
				x=x+1
				continue
		if validChars.find(text[x:x+1])!=-1:
			word=""
			while validChars.find(text[x:x+1])!=-1 and x<len(text):
				word+=text[x:x+1]
				x=x+1
			try:
				words[word]
			except Exception, e: #if word does not have a dictionary entry
				if isNotReserved(word) == True:
					words[word]=variable(word,randomString())
			else:
				currentVar=words[word]
				#now we need to descend down the object hierarchy
				while x<len(text) and dotValid.find(text[x:x+1])!=-1:
					if text[x:x+1]==".": #yay we found a cool new property i.e. console.log
						x=x+1
						subword=""
						while validChars.find(text[x:x+1])!=-1 and x<len(text):
							subword+=text[x:x+1]
							x=x+1
						maybe=DFSvars(currentVar,subword)
						if maybe!=None:
							currentVar=maybe
						else:
							newVar=variable(subword,randomString())
							print("real name is "+newVar.realname)
							currentVar.properties.append(newVar) #this here is the smokin gun
							currentVar=newVar

		else:
			x=x+1

def numberStuff(text):
	x=0
	out=""
	validBois=string.digits+"."
	openBrackets=False
	openQuotes=False
	openDoubleQuotes=False
	while x<len(text):
		if text[x:x+1]=="[":
			openBrackets=True
		else:
			if text[x:x+1]=="]":
				openBrackets=False
			elif text[x:x+1]=="\"" and openDoubleQuotes is False:
				openDoubleQuotes=True
			elif text[x:x+1]=="\"" and openDoubleQuotes is True:
				openDoubleQuotes=False
			elif text[x:x+1]=="\'" and openQuotes is False:
				openQuotes=True
			elif text[x:x+1]=="\'" and openQuotes is True:
				openQuotes=False
		if openBrackets is False:
			if openQuotes is True or openDoubleQuotes is True:
				x=x+1
				continue
		if validBois.find(text[x:x+1])!=-1:
			num=""
			if x-1<0 or validBois.find(text[x-1:x])==-1: #beginning of a number
				while validBois.find(text[x:x+1])!=-1 and x<len(text):
					num+=text[x:x+1]
					x=x+1
				alias=randomString(2,4)
				justDots=True
				for z in range(0,len(num)): #gotta make sure that it ain't just a string of dots thats wack
					if num[z:z+1] !=".":
						justDots=False
						break
				if justDots is False:
					out+="var "+alias+" = "+num+";\n"
					words[str(num)]=variable(str(num),alias,True)
		else:
			x=x+1
	return(out)

def beginningStuff():
	#this is all the code that goes at the beginning of the shrunken file
	add=""
	for w in words:
		if words[w].number is False:
			add+=words[w].codename+"=(typeof "+w+"!==\'undefined\' ? "+w+" : null);\n" 
	return(add)

def parseAndReplace(text):
	text=" "+text
	x=0
	openBrackets=False
	openQuotes=False
	openDoubleQuotes=False
	while x<len(text):
		if text[x:x+1]=="[":
			openBrackets=True
		else:
			if text[x:x+1]=="]":
				openBrackets=False
			elif text[x:x+1]=="\"" and openDoubleQuotes is False:
				openDoubleQuotes=True
			elif text[x:x+1]=="\"" and openDoubleQuotes is True:
				openDoubleQuotes=False
			elif text[x:x+1]=="\'" and openQuotes is False:
				openQuotes=True
			elif text[x:x+1]=="\'" and openQuotes is True:
				openQuotes=False
		if openQuotes is True or openDoubleQuotes is True or openBrackets is True:
			x=x+1
			continue
		if validChars.find(text[x:x+1])!=-1:
			word=""
			start=x
			while validChars.find(text[x:x+1])!=-1 and x<len(text):
				word+=text[x:x+1]
				x=x+1
			try:
				words[word]
			except Exception, e: #if word does not have a dictionary entry, this should NOT happsn
				if isNotReserved(word) == True:
					words[word]=variable(word,randomString())
			else:
				currentVar=words[word]
				rep=words[word].codename #what we replace all this shit with
				#now we need to descend down the object hierarchy
				totalWord=word
				while x<len(text) and dotValid.find(text[x:x+1])!=-1:
					totalWord+=text[x:x+1]
					x=x+1
				beeps=totalWord.split(".")
				for b in range(1,len(beeps)): #the first thing is the name of the OG word so we aint do nohing
					query=beeps[b]
					for p in currentVar.properties:
						if p.realname==query:
							rep+="."+p.codename
							currentVar=p
							break
				z=0
				openBracketsZ=False
				openQuotesZ=False
				openDoubleQuotesZ=False
				while z<len(text):
					if text[z:z+1]=='[':
						openBracketsZ=True
					else:
						if text[z:z+1]==']':
							openBracketsZ=False
						elif text[z:z+1] =='\"' and openDoubleQuotesZ is False:
							openDoubleQuotesZ=True
						elif text[z:z+1] =='\"' and openDoubleQuotesZ is True:
							openDoubleQuotesZ=False
						elif text[z:z+1] =="\'" and openQuotesZ is False:
							openQuotesZ=True
						elif text[z:z+1] =="\'" and openQuotesZ is True:
							openQuotesZ=False
					if openQuotesZ is True or openDoubleQuotesZ is True or openBracketsZ is True:
						z=z+1
						continue
					if validChars.find(text[z:z+1])!=-1:
						begin=z
						bitch=""
						while dotValid.find(text[z:z+1])!=-1:
							bitch+=text[z:z+1]
							z=z+1
						if bitch==totalWord:
							text=text[0:begin]+rep+text[begin+len(totalWord):]
					else:
						z=z+1
				x=start+len(rep)


		else:
			x=x+1
	return(text)

def obfus(text):
	#numbers
	pre=numberStuff(text)
	getVars(text)
	getProps(text)
	text=parseAndReplace(text)
	return(pre+beginningStuff()+text)


def main(file):
	text=cleanFile(file)
	open(file,"w+").close() 
	open(file,"w+").write(obfus(text))

if __name__ == '__main__':
	#removeComments("aa//a")
	if len(sys.argv)>1:
		main(sys.argv[1])