import string
import random
import sys
words={}
wordSlim={}
validChars=string.ascii_letters+string.digits+"_"
dotValid="."+validChars
Bstrings=[]
reserved=["break","default","function","return","var","case","delete","if","switch","void","catch","do","in","this","while","const","else","instanceof","throw","with","continue","finally","let","try","debugger","for","new","typeof"]

def isNotReserved(word): 
	for r in reserved:
		if r ==word:
			return(False)
	return(True)

def createBstrings(): 
	for x in range(0, random.randint(10,15)):
		Bstrings.append(randomString())

def randomString():
	out="_" 
	for x in range(0,random.randint(3,6)):
		r=random.randint(0,len(validChars)-1)
		out+=validChars[r:r+1]
	for w in words: 
		if w == out:
			return(randomString()) 
	for b in Bstrings:
		if b==out:
			return(randomString())
	return(out)

def getVars(text):
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
			elif text[x:x+1]==" ":
				text=text[0:x]+text[x+1:]
		if validChars.find(text[x:x+1])!=-1:
			word=""
			while dotValid.find(text[x:x+1])!=-1 and x<len(text):
				word+=text[x:x+1]
				x=x+1
			try:
				words[word]
			except Exception, e: 
				if isNotReserved(word) == True:
					words[word]=[]
		else:
			x=x+1

def fillWordsTwo():
	for w in words:
		words[w]=randomString()+randomString()

def fillWords():
	for w in words:
		subs=random.randint(2,5) 
		bigList=[]
		for s in range(0,subs):
			subLen=random.randint(2,5) 
			subList=[]
			realOne=random.randint(0,subLen-1) 
			for n in range(0,subLen): 
				if n==realOne or random.randint(0,1)==0: 
					subList.append(randomString()) 
				else:
					subList.append(Bstrings[random.randint(0,len(Bstrings)-1)])  
			bigList.append(subList)
		words[w]=bigList

def removeComments(text):
	singleLine=False
	multiLine=False
	x=0
	while x<len(text):
		if text[x:x+1]=="/":
			if x+1>=len(text):
				continue
			elif text[x+1:x+2]=="/":
				singleLine=True
			elif text[x+1:x+2]=="*":
				multiLine==True
		elif text[x:x+1]=="\n" and singleLine is True:
			text=text[0:x]+text[x+1:]
			singleLine=False
			continue
		elif text[x:x+1]=="*" and multiLine is True and x+1<len(text) and text[x+1:x+2] =="/":
			text=text[0:x]+text[x+1:]
			singleLine=False
			continue
		if multiLine is True or singleLine is True:
			text=text[0:x]+text[x+1:]

def editText(text):
	linesToAdd=[] 
	text=text.replace("\n","")
	for w in words:
		for name in words[w]:
			lastThing=random.randint(0,len(linesToAdd)) 
			print(lastThing)
			first="var "+name[0]+""
			randomWord="" 
			randomInt=random.randint(0,len(words)-1)
			count=0
			for wub in words:
				if count==randomInt:
					randomWord=wub		
				else:
					count=count+1
			first+="=(typeof "+randomWord+"!==\'undefined\' ? "+randomWord+" : null);"
			linesToAdd.insert(lastThing,first) 
			for q in range(1,len(name)): 
				add=name[0] 
				for k in range(1,q+1):
					add+=""+name[k]
				if q== len(name)-1:
					while text.find(w)!=-1:
						text=text.replace(w,add)
					add+="=(typeof "+w+"!==\'undefined\' ? "+w+" : null)" 
				else:
					randomWord="" 
					randomInt=random.randint(0,len(words)-1)
					count=0
					for wub in words:
						if count==randomInt:
							randomWord=wub
						else:
							count=count+1
					add+="=(typeof "+randomWord+"!==\'undefined\' ? "+randomWord+" : null)"
				add+=";" 
				lastThing=random.randint(lastThing+1,len(linesToAdd)) 
				linesToAdd.insert(lastThing,"var "+add)
	x=0 
	'''while x<len(text):
		if validChars.find(text[x:x+1])!=-1:
			start=x 
			word=""
			while dotValid.find(text[x:x+1])!=-1 and x<len(text):
				word+=text[x:x+1]
				x=x+1 
			try:
				words[word]
			except Exception, e: 
				pass
			else:
				alias=words[word][random.randint(0,len(words[word])-1)] 
				newStr=""+alias[0] 
				for b in range(1,len(alias)):
					newStr+=""+alias[b]
				text=text[0:start]+newStr+text[x:]
				x=start+len(newStr)
		else:
			x=x+1'''
	lines=""
	for line in range(0,len(linesToAdd)):
		lines+=linesToAdd[line]
	text=lines+text
	return(text)

def obfus(text): 
	getVars(text)
	createBstrings()
	fillWords()
	return(editText(text))

def main(file):
	text=open(file,"r+").read()
	open(file,"w+").close() 
	open(file,"w+").write(obfus(text))

if __name__ == '__main__':
	#removeComments("aa//a")
	if len(sys.argv)>1:
		main(sys.argv[1])