import math, nltk, numpy, random

### Input: a string
### Output: the same string, but tokenized into a list using the
###  word_tokenize() function from nltk
### Comments:
###  -Gets input ready for nltk functions
###  -Also used to clean data when punctuation is irrelevant
def tokenize(s):
	s = list(s)
	for i, c in enumerate(s):
		val = (not c.isalnum() and not c.isspace()) or c == '\n'
		if val:
			s[i] = ' '
	s = ''.join(s)
	output = nltk.word_tokenize(s)
	return output

### Input: a string
### Output: a list of the sentence lengths in that string
### Comments:
###  -Should contractions be one or two words? Here, they're two
###  -Also, numerals are currently basically treated as punctuation
###  -Can't handle characters like accents--might be a problem if we
###   want to do foreign languages. Could easily be coded in though.
###  -Weird problem w/ Huck Finn
def getSenLens(input):
	senLens = []
	counter = 0
	for i, c in enumerate(input):
		if not type(c) is str:
			return senLens
		if not c.isalpha() or i+1 == len(input):
			if input[i-1].isalpha():
				counter += 1
		if c in ['!','.','?'] or i+1 == len(input):
			senLens.append(counter)
			counter = 0
	return senLens

### Input: a string
### Output: a list of word lengths in that string
###
def getWordLens(input):
	wordLens = []
	words = tokenize(input)
	for w in words:
		wordLens.append(len(w))
	return wordLens

### Input: a string
### Output: A dictionary of unigram counts over that string
### Comments:
###  -Does this deal with capitalization correctly?
def getUniCounts(input):
	words = tokenize(input)
	counts = dict()
	for w in words:
		if w not in counts:
			counts[w] = 1
		else:
			counts[w] += 1
	return counts


### END OF HELPER FUNCTIONS


### Input: a string
### Output: average sentence length over that string
### Comments:
###  -See getSenLens()
def aveSenLen(input):
	if len(input) == 0:
		return 0
	senLens = getSenLens(input)
	return numpy.mean(senLens)

### Input: a string
### Output: standard deviation of sentence length over that string
### Comments:
###  -See getSenLens()
def senLenVar(input):
	if len(input) == 0:
		return 0
	senLens = getSenLens(input)
	std = numpy.std(senLens)
	return std

### Input: a string
### Output: average word length over that string
### Comments:
###  -Basically the same as for getSenLens()
def aveWordLen(input):
	wordLens = getWordLens(input)
	ave = numpy.mean(wordLens)
	return ave

### Input: a string
### Output: a dictionary with proportions of each POS in the input
### Comments:
###  -Careful, very slow
###  -There is no entry in the dictionary for POS's unattested in
###    the input
def getPosDist(input):
	words = tokenize(input)
	output = dict()
	pos = nltk.pos_tag(words)
	for pair in pos:
		for t in ['CC','CD','DT','EX','FW','IN','JJ','JJR','JJS','LS','MD','NN','NNS','NNP','NNPS','PDT','POS','PRP','PRP$','RB','RBR','RBS','RP','SYM','TO','UH','VB','VBD','VBG','VBN','VBP','VBZ','WDT','WP','WP$','WRB']:
			output[t] = 0
		if pair[1] not in output:
			output[pair[1]] = 1
		else:
			output[pair[1]] += 1
	total = numpy.sum(output.values())
	for t in output:
		output[t] /= total
	return output

### Input: a string, a sample size
### Output: Average type-to-token ratio over a sample size of n
###  tokens in the input string
### Comments:
###  -It's sensitive to n so that the output is more relevant to the
###    specific length of the input
def getAveTTR(input, n):
	text = tokenize(input)
	random.shuffle(text)
	if n > len(text):
		print 'ERROR: n TOO LARGE'
		return -1
	ttrs = []
	for x in range(len(text)):
		if x+n < len(text):
			temp = text[x:x+n]
		else:
			temp = text[x:] + text[:n-(len(text)-x)]
		counts = dict()
		for w in temp:
			if w in counts:
				counts[w] += 1
			else:
				counts[w] = 1
		counts = counts.values()
		tokenCount = numpy.sum(counts)
		typeCount = len(counts)
		ttr = float(typeCount)/float(tokenCount)
		ttrs.append(ttr)
	ave = numpy.mean(ttrs)
	return ave

### Input: a string, and a dictionary of unigram counts
### Output: perplexity of the string under the language model
###  defined by using the smoothing method from midterm of the counts
###  in the input dictionary
### Comments:
###  -Can take dictionary input from getUniCounts()
###  -Maybe prep stuff (e.g., missing mass calculation, generation of
###    probability dictionary, etc.) can be combined w/ getUniCounts()?
def getUniPerp(s, counts):
	### Calculates 'missing mass' probability
	n = 0
	for x in counts.values():
		n += x
	n1 = 0
	for w in counts:
		if counts[w] == 1:
			n1 += 1
	mProb = float(n1)/float(n)
	### Generates probability dictionary using no. of incidences
	###  as keys (e.g., if counts['foo'] = 5, probs[5] represents
	###  smoothed unigram probability of 'foo')
	nCounts = dict()
	highest = 0
	for w in counts:
		if counts[w] in nCounts:
			nCounts[counts[w]] += 1
		else:
			nCounts[counts[w]] = 1
		if counts[w] > highest:
			highest = counts[w]
	for i in range(highest+1):
		if 1<i<6:
			if not i+1 in nCounts:
				nCounts[i+1] = 0
			nCounts[i] = float(nCounts[i+1])/float(nCounts[i])
			nCounts[i] *= nCounts[i+1]
	probs = dict()
	for x in nCounts:
		probs[x] = nCounts[i]/n
	### Actually calculates perplexity
	pp = float(0)
	text = tokenize(s)
	for w in text:
		if w in nCounts:
			pp *= math.log10(probs[nCounts[w]])
		else:
			pp += math.log10(mProb)
	pp *= (-1/float(n))
	pp = math.pow(10, pp)
	return pp


