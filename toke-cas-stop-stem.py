import sys, re, codecs, os, multiprocessing
import datrie, string
import xml.etree.ElementTree as et
from nltk.corpus import stopwords
# from nltk.stem.porter import PorterStemmer
# from thread import start_new_thread
# from stemming.porter2 import stem
import Stemmer
import json

reload(sys)
sys.setdefaultencoding("utf-8")



def is_ascii(s):
    return all(ord(c) < 128 for c in s)


def sortandmerge(tdlist):
	# if fileNo%100==0:
	# 	print str(fileNo)+" started"
	# fileName = "listFiles/" + str(fileNo) + ".txt"

	# tdlist.sort()
	# ptr = 0
	# index = []
	# index.append([tdlist[0][0], [tdlist[0][1], ]])
	# for i in range(1, len(tdlist)):
	# 	if tdlist[i-1][0] == tdlist[i][0]:
	# 		if tdlist[i-1][1] == tdlist[i][1]:
	# 			pass
	# 		else:
	# 			index[ptr][1].append(tdlist[i][1])
	# 	else:
	# 		ptr += 1
	# 		index.append([tdlist[i][0], [tdlist[i][1],]])




	# with open(fileName, "w+") as f:
	# 	json.dump(index, f)
	global trie
	for ele in tdlist:
		word = ele[0].decode("utf-8")
		if word not in trie:
			trie[word] = set()
		trie[word].add(ele[1])
		# print trie[word]
	print len(trie.keys())
	# print str(fileNo)+" completed"


def process(data, docId):
	if docId > 5:
		return
	global tdlist
	data = re.findall(r"[a-zA-Z]+", data.lower())
	data = [ [stemmer.stemWord(item), docId] for item in data if item not in stop_words]
	tdlist += data
	if len(tdlist) >= 10**6:
		global fileNo, proc
		if proc:
			proc.join()
		proc = multiprocessing.Process(target=sortandmerge, args=(tdlist, ))
		proc.start()
		# sortandmerge(data)
		fileNo += 1
		# if fileNo%100==0:
		print fileNo
		tdlist = []
	

def main():
	global stop_words, stemmer, tdlist, fileNo, trie, proc
	proc = None
	trie = datrie.Trie(string.ascii_lowercase)
	tdlist = []
	stop_words = stopwords.words('english')
	stemmer = Stemmer.Stemmer('english')
	fileNo = 1
	noThreads = 0

	tree = et.parse('./wiki-search-small.xml')
	root = tree.getroot()
	fileC = 1
	os.system("rm -rf data; mkdir data")
	os.system("rm -rf listFiles; mkdir listFiles")
	for child in root:
		if(child.tag.endswith('page')):
			for t in child:
				if(t.tag.endswith('revision')):
					for c in t:
						if c.tag.endswith('text'):
							fileName = "data/"+ str(fileC) + '.txt'
							with codecs.open(fileName,"w+") as f:
								f.write(c.text)
								process(c.text.lower(), fileC)
								# multiprocessing.Process(target=process, args=(c.text.lower(), )).start()
								fileC += 1
								# print fileC
	
	if len(tdlist) > 0:
		if proc:
			proc.join()
		multiprocessing.Process(target=sortandmerge, args=(tdlist, )).start()
	# sortandmerge(tdlist, fileNo)
	# tdlist = []
	if proc:
		proc.join()
	state = datrie.State(trie)
	# state.walk(u'')
	it = datrie.Iterator(state)
	print len(trie.keys())
	s = ""
	while it.next():
		print "hola"
		print it.key()
main()