# comp
Ling 550 computational linguistics

Corpus:
All the files that are called ####.txt
Each file contains in an array:
['title', 'author', gutenberg#', 'type of text', 'text of book']
These include 8 works each from Shakespeare, Dickens, and Twain.


How to run:

  classifier.py
  In the part of the script named shell (at the very bottom), you can specify
  the author that you want to train the model on (authors), 
  the number of texts to train the classifier on (setlength),
  and the number of repetitions you want to run the script per author (iterations).  
  The script will average precision, recall, and accuracy over repetitions.
  The 5 most informative features will be printed out as the script runs.
  The output of classifier.py is formatted as a dict:
  {[author]:[accuracy, precision, recall]}
  
example call from command prompt:
  python classifier.py

  
#####Details, Details ###############################################
Sub-functions:
indices.py - contains several sub-functions:
  -parse(file): takes a text file, strips punctuation (not implemented yet), and splits file into a list of words
  -ngramprobs(file): takes a list of words (output of parse), calculates the Simple Good-Turing probabilities of each n-gram
  -wordlengthSD(file): takes a list of words (output of parse), and calculate standard deviation of word lengths in the text
  -bagofwords(file, x): takes a list of words (output of parse) and returns x most frequent words and x most frequent POS tags
  -hifreqwords(file1, file2, x): ||TO COME|| takes 2 lists of words (the 1st to compare against the 2nd), and returns a list of x words whose frequencies are the most statistically different from the other word list
   
Details on each function:
  -parse(filename): takes in a text file, splits words by whitespace, outputs list of words in the file
  -ngramprobs(filename): from list of words, creates list of bi-, tri-, quadragrams. nltk simple good-turing function is applied to those 4 lists to get n-gram probabilities.  4 lists containing uni-, bi-, tri-, quadragram probabilities are returned.
  -wordlengthSD(filename): from a list of words, word length is counted for each word.  sd is calculated.
  -bagofwords(filename, numResults): from a list of words, get the POS tags for each, using nltk function pos_tags.  Count tokens and return top x results for both lists.
  -hifreqwords(file1, file2, x): frequency counts of each word list will be calculated for both lists, top x words in file1 with the maximum deviation from the same word in file 2 will be returned

