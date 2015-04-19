import nltk, random
from indices import parse, aveSenLen, senLenVar, aveWordLen, getPosDist, getAveTTR, getUniPerp, getUniCounts, gettextGT, bagofwords, wordlengthSD
from ngramprobs import ngrams, ngramcounts, GTprobs
from sys import getsizeof

# BL: This function creates list of features from string
def features(s, numResults, uniGT, biGT, triGT, quadGT):
    
##    bag=(bagofwords(s, numResults))
##    #print bag
##    bagout=""
##    for n in range(numResults):
##        bagout+=",'freqword"+str(n)+"':bag["+str(n)+"]"
##    print bagout
    #[u, b, t, q]=gettextGT([s], uniGT, biGT, triGT, quadGT)
    out="{'avg sent len': aveSenLen(s),'avg sent sd':senLenVar(s)"
    #out+=",'avg word len':aveWordLen(s),'avg word sd':wordlengthSD(s)"
    out+=",'type-token ratio':getAveTTR(s, 100)"
    #out+=",'unigram log-probs':u,'bigram log-probs':b,'quadgram log-probs':q"
    #out+=",'trigram log-probs':t"
##    out+=","
##    out+=bagout[1:]
    out+="}"
    try:
        features=eval(out)
        print features
    except(IndexError):
        print bag
        print s[:100]
        return 999
    #print "Features are: avg sent len, avg sent sd, avg word len, avg word sd, most frequent words (n), n-gram log-probs, type-token ratio, PERPLEXITY?"
    return features

def makeFeatureList(filelist, training_set, test_set):
    #From texts from author only, calculate n-gram probs
    #Will be input to feature extractor
    [u,b,t,q]=ngrams(filelist)
    [u2,b2,t2,q2]=ngramcounts(u,b,t,q)
    [uniGT, biGT, triGT, quadGT]=GTprobs(u2,b2,t2,q2)
    
    #create feature set for training data
    training_feature_set = [(features(text, 5, uniGT, biGT, triGT, quadGT), author) for (text, author) in training_set]
    test_feature_set = [features(text, 5, uniGT, biGT, triGT, quadGT) for (text) in test_set]
    #print 'triGT size: ' + str(getsizeof(training_feature_sets))
    print 'training_set:'
    print training_feature_set
    print 'test_set:'
    print test_feature_set
    return training_feature_set, test_feature_set

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


#randomly pick sme number of books from other authors for training set and test set
otherlist=[]
num=0
sizeIdx=0
setlength=4

randNums=range(len(data))
random.shuffle(randNums)
pickedAuthor=author[randNums[0]] #classify this author
Author_train=booksDict[pickedAuthor]

non_author_test=[]
#non-author test and train sets
while sizeIdx<(setlength):
    if randNums[num] not in Author_train:
        if sizeIdx>=setlength/2:
            #add num to test set
            non_author_test.append(randNums[num])
            sizeIdx+=1
        else:
            #add num to training set
            otherlist.append(randNums[num])
            sizeIdx+=1
    num+=1 # iterate to next num in randNums

#author train set, test set
Author_test=[]
for j in range(setlength/2):
    Author_test.append(Author_train.pop())
Author_train=Author_train[:(setlength/2)]

#compile list of test authors
test_set=Author_test+non_author_test
random.shuffle(test_set)


### DEBUG ### Shortens runtime so that n-grams are calculated based on 1 text only
Author_train=[Author_train[0]]

#compile text training set
labelled_books_author = ([(text[i], pickedAuthor) for i in Author_train])
labelled_books_other = ([(text[o], 'Other') for o in otherlist])
training_set=labelled_books_author + labelled_books_other
random.shuffle(training_set)
print 'Finished training set'
#compile text test set
test_set = ([(text[i]) for i in test_set])


## Calculate GTprob for current author' texts (needed to calculate GTProbs of individual texts)
filelist=[]
for idx in Author_train:
    filelist.extend(text[idx])
print 'finished making filelist.  Ready to make Feature List'
print len(test_set)
[train, test] =makeFeatureList(filelist, training_set, test_set)

##train classifier
print 'training classifiers'
classifier = nltk.NaiveBayesClassifier.train(train)

#print most informative features
print 'Most informative Features'
print classifier.most_informative_features(5)

##test classifier
classifier.classify(test[0])





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
