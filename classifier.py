import nltk, random, re
from indices import parse, aveSenLen, senLenVar, aveWordLen, getPosDist, getAveTTR, getUniPerp, getUniCounts, gettextGT, bagofwords, wordlengthSD
from ngramprobs import ngrams, ngramcounts, GTprobs
from sys import *

### INPUT:
###  - raw - raw txt file of a gutenberg book
###  - c - comment (e.g., 'P' for play)
### OUTPUT: that txt file with header and footer removed
def clean(raw, c):
	i = 0
	asts = []
	while i < len(raw)-2:
		if raw[i] == raw[i+1] == raw[i+2] == '*':
			asts.append(i)
		i += 1
	diffs = dict() ### returns distance to next * cluster
	for i, index in enumerate(asts):
		if i != len(asts)-1:
			diffs[index] = asts[i+1]-asts[i]
	top = 0
	topI = 0
	for index in diffs:
		if diffs[index] > top:
			top = diffs[index]
			topI = index
	if top > 10000:
		trimmed = raw[topI:topI+top]
	else:
		trimmed = raw[asts[len(asts)-1]:]
	### if play replaces uppercase things of 4+ char w/ __nAME__:
	if c == 'P':
		trimmed = re.sub(r'[A-Z]{3}[A-Z]+', '__nAME__', trimmed)
	trimmed = re.sub(r'<<[^)]*>>','',trimmed)
	return trimmed

# BL: This function creates list of features from string
def features(s, numResults, uniGT, biGT, triGT, quadGT):
    
    bag=(bagofwords(s, numResults))
    #print bag
    bagout=""
    for n in range(numResults):
        bagout+=",'freqword"+str(n)+"':bag["+str(n)+"]"
    print bagout
    [u, b, t, q]=gettextGT([s], uniGT, biGT, triGT, quadGT)
    out="{'avg sent len': aveSenLen(s),'avg sent sd':senLenVar(s)"
    out+=",'avg word len':aveWordLen(s),'avg word sd':wordlengthSD(s)"
    out+=",'type-token ratio':getAveTTR(s, 100)"
    out+=",'unigram log-probs':u,'bigram log-probs':b,'quadgram log-probs':q"
    out+=",'trigram log-probs':t"
    out+=","
    out+=bagout[1:]
    out+="}"
    try:
        features=eval(out)
        print features
    except(IndexError):
        print 'Bag of Words Error'
        print len(s)
        print s
        features=[999]
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
##    print 'training_set:'
##    print training_feature_set
##    print 'test_set:'
##    print test_feature_set
    return training_feature_set, test_feature_set

##### Metrics #####
##Input: test set, author-idx vector, test-set-idx, author that is being identified,
##Output: Accuracy, precision, recall
def test_metrics(test, author, test_set_idx, pickedAuthor):
    classifier_output=[]
    actual_answer=[]
    for t in range(len(test)): #make sure size of test isn't 1
        classifier_output.append(classifier.classify(test[t]))
        actual_answer.append(author[test_set_idx[t]])

    #In lsit f actual authors, replace non-Author with 'Other'
    for a in range(len(actual_answer)):
        if actual_answer[a]!=pickedAuthor:
            actual_answer[a]='Other'
    print actual_answer
    print classifier_output

    #initialize T/F-pos/negative values
    correct=0
    T_pos=0
    T_neg=0
    F_pos=0
    F_neg=0
    #count  T/F-pos/negative values
    for a in range(len(actual_answer)):
        if actual_answer[a]==classifier_output[a]:
            correct+=1
        if actual_answer[a]==pickedAuthor:
            if classifier_output[a]==pickedAuthor:
                T_pos+=1
            elif classifier_output[a]=='Other':
                F_neg+=1
        elif actual_answer[a]=='Other':
            if classifier_output[a]==pickedAuthor:
                F_pos+=1
            elif classifier_output[a]=='Other':
                T_neg+=1

    #calculate precision, accuracy, recall
    accuracy=float(correct)/len(actual_answer)   
    #precision
    #relevant records retrieved/number of relevant and irrelevant records retrieved
    #Of the clssifier outputs that are labelled Author X, how many are actually Author X?
    precision=float(T_pos)/(T_pos+F_pos)
    #recall
    #relevnt records retrieved/relevant records retrieved or not retrieved
    recall=float(T_pos)/(T_pos+F_neg)

    #print warnings
    if F_pos==0:
        print 'Warning: No false positives'
    if T_pos==0:
        print 'Warning: No true positives'
    if F_neg==0:
        print 'Warning: No false negatives'
    if T_neg==0:
        print 'Warning: No true negatives'
    return accuracy, precision, recall


##### Main #####
def main(pickedAuthor,setlength):
        print 'main'
        # cd to dir, load all texts
        f=open('db.txt')
        data=eval(f.read())

        #split data into author and text
        print 'read data'
        booksDict={} #create lookup table for books, by author
        author=[]
        text=[]
        title=[]
        for i in range(len(data)):
            #format: 'title', 'author', 'gutenberg#', '', 'text'
            currauthor=data[i][1]
            title.append(data[i][0])
            author.append(currauthor)
            if currauthor in booksDict.keys():
                booksDict[currauthor].append(i)
            else:
                booksDict[currauthor]=[i]
            cleaned = clean(data[i][4],data[i][3])
            text.append(cleaned)
        print 'finished reading corpus'
        print 'titles'
        print title
        print'authors'
        print author

        #randomly pick n number of books from other authors for training set and test set
        otherlist=[]
        num=0
        sizeIdx=0
        #setlength=8 #Was constant, now is an input

        randNums=range(len(data))
        random.shuffle(randNums)
        pickedAuthor='Shakespeare, William' #argv[1] #classify this author
        Author_train=booksDict[pickedAuthor]
        random.shuffle(Author_train)

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
        test_set_idx=Author_test+non_author_test
        random.shuffle(test_set_idx)
        print Author_train
        print otherlist
        print test_set_idx
        ### DEBUG ### Shortens runtime so that n-grams are calculated based on 1 text only
        Author_train=[range(24)]

        #compile text training set
        labelled_books_author = ([(text[i], pickedAuthor) for i in Author_train])
        labelled_books_other = ([(text[o], 'Other') for o in otherlist])
        training_set=labelled_books_author + labelled_books_other
        random.shuffle(training_set)
        print 'Finished training set'
        #compile text test set
        test_set = ([(text[i]) for i in test_set_idx])


        ## Calculate GTprob for current author' texts (needed to calculate GTProbs of individual texts)
        filelist=[]
        for idx in Author_train:
            filelist.extend(text[idx])
        print 'finished making filelist.  Ready to make Feature List'
        [train, test] =makeFeatureList(filelist, training_set, test_set)

        ##train classifier
        print 'training classifiers'
        classifier = nltk.NaiveBayesClassifier.train(train)

        #print most informative features
        print 'Most informative Features'
        print classifier.most_informative_features(5)
        #Evaluation
        [accuracy, precision, recall]=test_metrics(test, author, test_set_idx, pickedAuthor)
        return accuracy, precision, recall

### SHELL ####
iterations=2 #test
setlength=2 #Total 8 in the corpus
authors=['Shakespeare, William','Twain, Mark', 'Dickens, Charles']
evalDict={}
for a in authors:
        total_acc=0
        total_precision=0
        total_recall=0
        for i in range(iterations):
                [accuracy, precision, recall]=main(a,setlength)
                total_acc+=accuracy
                total_precision+=precision
                total_recall+=recall
        avg_acc=float(total_acc)/iterations
        avg_precision=float(total_precision)/iterations
        avg_recall=float(total_recall)/iterations
        evalDict[a]=[avg_acc, avg_precision, avg_recall]

print 'Evaluation:'
print 'Dict contents are average accuracy, precision, and recall'
print evalDict
