import nltk, random
from indices import parse, aveSenLen, senLenVar, aveWordLen, getPosDist, getAveTTR, getUniPerp, getUniCounts, getngramprobs, bagofwords, wordlengthSD
from ngramprobs import ngrams, ngramcounts, GTprobs

# BL: This function creates list of features from string
def features(s, numResults, uniGT, biGT, triGT, quadGT):
    feature_array=[]
    feature_array.extend([aveSenLen(s)])
    feature_array.extend([senLenVar(s)])
    feature_array.extend([aveWordLen(s)])
    feature_array.extend([wordlengthSD(s)])
    
    feature_array.extend(bagofwords(s, numResults))
    feature_array.extend([getngramprobs(s, uniGT, biGT, triGT, quadGT)])

    #getPosDist(input) #requires numpy
    feature_array.extend([getAveTTR(s, 100)]) #arbitrary n
    feature_array.extend([getUniPerp(s, getUniCounts(s))])

    print "Features are: avg sent length, avg sent sd, avg word len, avg word sd, most frequent words (n), n-gram log-probs, type-token ratio, PERPLEXITY?"
    return feature_array

##### Metrics #####
def accuracy():
    return 1
def perplexity():
    return 1
def precision():
    return 1
def recall():
    return 1


##### Main #####

# cd to dir, load all texts
f=open('database.txt')
data=eval(f.read())

#split data into author and text
booksDict={} #create lookup table for books, by author
author=[]
text=[]
title=[]
for i in range(len(data)):
    #format: 'title', 'author', 'gutenberg#', '', 'text'
    #title.append(data[i][0]) #not neccessary
    currauthor=data[i][1]
    author.append(currauthor)
    if currauthor in booksDict.keys():
        booksDict[currauthor].append(i)
    else:
        booksDict[currauthor]=[i]
    text.append(data[i][4]) #next step is to strip table of contents and 'End of the Project Gutenberg EBook of '... from the end


#random shuffle to pick author for training set
randNums=range(len(data))
random.shuffle(randNums)
randAuthor=author[randNums[0]] #classify this author
AuthorBookList=booksDict[randAuthor]
########randomly remove one for testing purposes
random.shuffle(AuthorBookList)
author_test=AuthorBookList.pop()

#randomly pick sme number of books from other authors for training set
otherlist=[]
i=1
while len(otherlist)<len(AuthorBookList):
    if randNums[i] not in AuthorBookList:
        otherlist.append(randNums[i])
    i+=1

#compile training set
labelled_books_author = ([(text[i], randAuthor) for i in AuthorBookList])
labelled_books_other = ([(text[o], author[o]) for o in otherlist])
training_set=labelled_books_author + labelled_books_other
random.shuffle(training_set)

## Calculate GTprob for current author' texts (needed to calculate GTProbs of individual texts)
filelist=[]
for idx in AuthorBookList:
    filelist.extend(text[idx])
[u,b,t,q]=ngrams(filelist)
[u2,b2,t2,q2]=ngramcounts(u,b,t,q)
[uniGT, biGT, triGT, quadGT]=GTprobs(u2,b2,t2,q2)

#create feature set for training data
training_feature_sets = [(features(text, 5, uniGT, biGT, triGT, quadGT), author) for (text, author) in training_set]

#train classifier
classifier = nltk.NaiveBayesClassifier.train(training_feature_sets)

#print most informative features
classifier.show_most_informative_features(5)

#test classifier
classifier.classify(features(text[author_test])) #author
classifier.classify(features(text[i])) #non-author





######Example Classifier#######
##from nltk.corpus import names #make corpus
##labeled_names = ([(name, 'male') for name in names.words('male.txt')] +
##... [(name, 'female') for name in names.words('female.txt')]) #label
##
### create training/test groups
##random.shuffle(labeled_names)
##featuresets = [(gender_features(n), gender) for (n, gender) in labeled_names]
##train_set, test_set = featuresets[500:], featuresets[:500]
##
### train classifier
##classifier = nltk.NaiveBayesClassifier.train(train_set)
##
### test classifier
##classifier.classify(gender_features('Neo'))
##
### find informative features
##classifier.show_most_informative_features(5)
