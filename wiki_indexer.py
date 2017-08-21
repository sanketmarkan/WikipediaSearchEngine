import re, codecs, os, time
from multiprocessing import Manager, Process
import datrie, string
import xml.etree.ElementTree as et
from nltk.corpus import stopwords
import Stemmer
import json

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

trie = datrie.Trie(string.ascii_lowercase)

def mapper(tdlist, fileNo):
	for word, doc in tdlist:
		word = word.decode("utf-8")
		if word not in trie:
			trie[word] = set()
		trie[word].add(doc)
	
	
	lisoflis = [0]*5
	for i in range(5):
		lisoflis[i] = []
	for key in trie.keys():
		l = list(trie[key])
		l.sort()
		no = (ord(key[0])-ord('a'))/5
		no = min(no, 4)
		lisoflis[no].append([key, l])	

	for i in range(5):
		fileName = "listFiles/"+str(fileNo)+"-"+str(i)+".txt"
		with open(fileName, "w+") as f:
			json.dump(lisoflis[i], f)
	

def reducer(bin):
	for i in range(1,12):
		fileName = "listFiles/"+str(i)+"-"+str(bin)+".txt"
		while os.path.isfile(fileName) == False:
			time.sleep(3)
		try:
			with open(fileName, "rw+") as f:
				data = json.load(f)
		except:
			time.sleep(3)
			with open(fileName, "rw+") as f:
				data = json.load(f)
		for word, docs in data:
			word = word.decode("utf-8")
			if word not in trie:
				trie[word] = []
			trie[word] += docs

	lisoflis = []
	for key in trie.keys():
		l = list(set(trie[key]))
		l.sort()
		lisoflis.append([key, l])

	fileName = "listFiles/final"+str(bin)+".txt"
	with open(fileName, "w+") as f:
		json.dump(lisoflis, f)


def process(data, fileC):
	global tdlist, stemmer
	data = re.findall(r"[a-zA-Z]+", data.lower())
	for item in data:
		if item not in stop_words:
			item = stemmer.stemWord(item)
			if len(item) > 2 and len(item)<10:
				tdlist.append([item, fileC])
			if len(tdlist) > 10**6:
				global fileNo
				Process(target=mapper,args=(tdlist, fileNo,)).start()
				# mapper(data)
				tdlist = []
				fileNo += 1
	

if __name__ == "__main__":

	global proc, tdlist, fileNo, stop_words, stemmer, lis
	stop_words = set(stopwords.words('english'))
	stemmer = Stemmer.Stemmer('english')
	proc = 0
	tdlist = []
	fileNo = 1
	lis = []

	tree = et.parse(sys.argv[1])
	root = tree.getroot()
	fileC = 1
	
	os.system("rm -rf data; mkdir data")
	os.system("rm -rf listFiles; mkdir listFiles")

	for i in range(5):
		lis.append(Process(target=reducer, args=(i,)))
		lis[i].start()

	for child in root:
		if(child.tag.endswith('page')):
			for t in child:
				if(t.tag.endswith('revision')):
					for c in t:
						if c.tag.endswith('text'):
							fileName = "data/"+ str(fileC) + '.txt'
							with codecs.open(fileName,"w+") as f:
								f.write(c.text)
							process(c.text, fileC)
							
			fileC += 1
	if len(tdlist) > 0:
		Process(target=mapper,args=(tdlist, fileNo,)).start()

	for i in range(5):
		lis[i].join()
	data = []
	for i in range(5):
		fileName = "listFiles/final"+str(i)+".txt"
		with open(fileName, "r") as f:
			data += json.load(f)

	fileName = sys.argv[2]
	with open(fileName, "w+") as f:
		json.dump(data, f)


	os.system("rm -rf data listFiles")