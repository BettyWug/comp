import urllib2, time, random

### INPUT: a csv of books to download, like textCSV
### OUTPUT: a list of lists (one per book) of metadata,
###  formatted as follows:
###	[0] :: title
###	[1] :: author
###	[2] :: call number for Gutenberg
###	[3] :: comments (e.g. 'Play')
def makeList(csv):
	li = csv.split('\n')
	output = []
	for entry in li:
		temp = entry.split(';')
		output.append(temp)
	return output

### INPUT: a Gutenberg call number
### OUTPUT: txt of book at that number
### Notes:
###  -still needs to be altered to catch alternate url formats
###  -add a part at the beginning that checks connection
def download(callNum):
	url = 'https://www.gutenberg.org/cache/epub/'
	url += str(callNum)
	url += '/pg'
	url += str(callNum)
	url += '.txt'
	try:
		text = urllib2.urlopen(url).read()
		print 'd/l success'
		return text
	except Exception:
		print 'ERROR:'
		print url+' doesn\'t exist'
		return -1

### INPUT: filepath to a csv of books, like books.csv
### OUTPUT: like makeList(), but with the txt file as entry [4]
###  of each sublist (finished database)
def makeDatabase(csvFilepath):
	print 'OPENING AND PROCESSING CSV FILE'
	csv = open(csvFilepath).read()
	print 'opened'
	db = makeList(csv)
	print 'done'
	i = 0
	print 'BEGINNING DOWNLOADS'
	while i < len(db):
		book = db[i]
		if len(book) < 4:
			db.remove(book)
		else:
			print 'NOW DOWNLOADING: '+str(book[0])
			text = download(book[2])
			book.append(text)
			print 'WAITING 5 SECONDS...'
			###time.sleep(1)
			print 'done'
			i += 1
	print 'DATABASE PREPARED'
	return db

db = makeDatabase('books.csv')
open('database.txt','w')
outfile = open('database.txt','r+')
print 'FILE WRITTEN. EXITING.'
outfile.write(str(db))
