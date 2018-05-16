import string
import random
import sys

'''
this obfuscator will replace all variables with randomstringA.randomstringB.Arandomstring.randomstringB
each randomstringB will be unique for each variable
but randomstringA will NOT be unique, as to make things more confusing

so console=dicks.unique.butts.unIquE
also height=dicks.UnIqUe.butts.Individualism

'''



words={}
wordSlim={}
validChars=string.ascii_letters+string.digits+"_" #these are all the characters that could ever make up a varaible name in js
dotValid="."+validChars
Bstrings=[] #these are the random lines that will be repeated
reserved=["break","default","function","return","var","case","delete","if","switch","void","catch","do","in","this","while","const","else","instanceof","throw","with","continue","finally","let","try","debugger","for","new","typeof"]


def isNotReserved(word): #makes sure this word is not a reserved javascript keyword
	for r in reserved:
		if r ==word:
			return(False)
	return(True)

def createBstrings(): #makes a bunch of Bstrings
	for x in range(0, random.randint(10,15)):
		Bstrings.append(randomString())

def randomString():
	out="_" #it has to start with a _ or else it is problematic when it starts with a number
	for x in range(0,random.randint(3,6)):
		r=random.randint(0,len(validChars)-1)
		out+=validChars[r:r+1]
	for w in words: #we make sure that this random string has not already been used
		if w == out:
			return(randomString()) #if it matches, then we have to try again
		for n in words[w]:
			if n == out:
				return(randomString()) #if it matches, then we have to try again
			for b in Bstrings:
				if b==out:
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
			while dotValid.find(text[x:x+1])!=-1 and x<len(text):
				word+=text[x:x+1]
				x=x+1
			try:
				words[word]
			except Exception, e: #if word does not have a dictionary entry
				if isNotReserved(word) == True:
					words[word]=[]
		else:
			x=x+1

def fillWords():
	#assuming the Words dictionary has been filled, we fill each key with a 
	#list of sublist. each sublist is of a random length between 2 and 5
	#each subllist is all the variable names that will make up the new obfuscatred name
	#words["console"] --> [["dicks","unique","butts","unIque"],["butts","boobz"]
	for w in words:
		#print("anus")
		subs=random.randint(2,5) #how many sublists this guy has
		bigList=[]
		for s in range(0,subs):
			subLen=random.randint(2,5) #this is the length of the sublist
			subList=[]
			realOne=random.randint(0,subLen-1) #we will have at most ONE unique string for each alias this will be the index of it
			for n in range(0,subLen): 
				if n==realOne or random.randint(0,1)==0: #theres a 50% chance of getting a 1 or 0
					subList.append(randomString()) #we add a unique random string at least ONCE but we might add a unique random one sometimes
				else:
					subList.append(Bstrings[random.randint(0,len(Bstrings)-1)])  #it will be a random string from Bstrings
			bigList.append(subList)
		words[w]=bigList

def editText(text):
	#text is the document that we're now parsing and fixing
	linesToAdd=[] #these will be the lines that define the new variables
	#linesToAdd.append("//obfusc8ed")
	text=text.replace("\n","")
	for w in words:
		#print(w)
		#usedNames=[]
		for name in words[w]: #name is a list of random words
			#print(name)
			lastThing=random.randint(0,len(linesToAdd)) #this is the index in linesToAdd of the last place where we defined a variable
			print(lastThing)
			'''
				like if sub=["dicks", "butts"],["bees","knees"]
				then maybe we put "var dicks;" at line 3
				then lastThing=3
			'''
			first="var "+name[0]+""
			randomWord="" #we want to find a random word in words dict to set this equal to 
			randomInt=random.randint(0,len(words)-1)
			count=0
			for wub in words:
				if count==randomInt:
					randomWord=wub		
				else:
					count=count+1
			first+="=(typeof "+randomWord+"!==\'undefined\' ? "+randomWord+" : null);"
			linesToAdd.insert(lastThing,first) #define the first element in the list
			#print("now we insert "+"var "+name[0]+";"+" at index "+str(lastThing))
			for q in range(1,len(name)): #we start at index 1 b/c we already added the first element
				add="var "+name[0] #this is the base
				for k in range(1,q+1):
					add+=""+name[k]
				if q== len(name)-1:
					add+="=(typeof "+w+"!==\'undefined\' ? "+w+" : null)" #if its the last thing in the list we need to set it equal to whatever variable name were disguising
				else:
					randomWord="" #we want to find a random word in words dict to set this equal to 
					randomInt=random.randint(0,len(words)-1)
					count=0
					for wub in words:
						if count==randomInt:
							randomWord=wub
						else:
							count=count+1
					add+="=(typeof "+randomWord+"!==\'undefined\' ? "+randomWord+" : null)"
				add+=";" #finish it off with a semicolon ofc
				lastThing=random.randint(lastThing+1,len(linesToAdd)) #the new thing we're writing will be randomly after the OG lastThing
				#print("now we insert "+add+" at index "+str(lastThing))
				linesToAdd.insert(lastThing,add)
	#return(linesToAdd)
	x=0 #now we parse the thing and find any words
	while x<len(text):
		if validChars.find(text[x:x+1])!=-1:
			start=x #the beginnign of the word
			word=""
			while dotValid.find(text[x:x+1])!=-1 and x<len(text):
				word+=text[x:x+1]
				x=x+1 #at the end, x will be the first character that isnt part of word
			try:
				#print(word)
				words[word]
			except Exception, e: #if word does not have a dictionary entry
				pass
			else:
				#word DOES have a dictionary entry
				alias=words[word][random.randint(0,len(words[word])-1)] #we randomly choose one of the lists that are attached to this word in the dictionary
				newStr=""+alias[0] 
				for b in range(1,len(alias)):
					newStr+=""+alias[b]
				text=text[0:start]+newStr+text[x:]
				x=start+len(newStr)
		else:
			x=x+1
	lines=""
	for line in range(0,len(linesToAdd)):
		lines+=linesToAdd[line]
	text=lines+text
	return(text)

def obfus(text): #takes some nice clean text and encrypts it
	getVars(text)
	createBstrings()
	fillWords()
	return(editText(text))

def main(file):
	text=open(file,"r+").read()
	open(file,"w+").close() #empties the contents of the old file
	open(file,"w+").write(obfus(text))

if __name__ == '__main__':
	if len(sys.argv)>1:
		main(sys.argv[1]) #presumably the file that we want to obfuscate is passed as a command line argument