from mapperReducer import *

def process(data, fileC, catIn):
	global tdlist, stemmer
	data = re.findall(r"[a-zA-Z]+", data.lower())
	# if(fileC>1000):
	# 	return
	for item in data:
		if item not in stop_words:
			item = stemmer.stemWord(item)
			global count
			no = (ord(item[0])-ord('a'))/5
			no = min(no, 4)
			tdlist[catIn][no].append([item, fileC])
			count[catIn] += 1
			if count[catIn] > 10**6:
				global fileNo, proc
				mapp.append(Process(target=mapper,args=(tdlist[catIn], fileNo,)))
				mapp[-1].start()
				for i in range(5):
					tdlist[catIn][i] = [];
				count[catIn] = 0
				fileNo += 1

if __name__ == "__main__":

	global count, proc, tdlist, fileNo, stop_words, stemmer, lis, mapp
	stop_words = set(stopwords.words('english'))
	stemmer = Stemmer.Stemmer('english')
	proc = 0
	count = [0]*2
	mapp = []

	tdlist = [0]*2
	for i in range(2):
		tdlist[i] = [0]*5
		for j in range(5):
			tdlist[i][j] = []
	fileNo = 1
	lis = []

	tree = et.parse(sys.argv[1])
	root = tree.getroot()
	fileC = 1
	print "parsed"
	os.system("rm -rf data; mkdir data")
	os.system("rm -rf listFiles; mkdir listFiles")

	for child in root:
		if(child.tag.endswith('page')):
			for t in child:
				if(t.tag.endswith('title')):
					pass
					# print t.text
				if(t.tag.endswith('revision')):
					for c in t:
						if c.tag.endswith('text'):
							if (c.text):
								fileName = "data/"+ str(fileC) + '.txt'
								with codecs.open(fileName,"w+") as f:
									f.write(c.text)
								process(c.text, fileC, 1)
							
			fileC += 1
	if len(tdlist[1]) > 0:
		mapp.append(Process(target=mapper,args=(tdlist[1], fileNo)))
		mapp[-1].start()
		fileNo += 1

	print "join started"
	for proc in mapp:
		proc.join()
	print "joined"

	for i in range(5):
		lis.append(Process(target=reducer, args=(i, fileNo)))
		lis[i].start()
		# reducer(i, fileNo)

	for i in range(5):
		lis[i].join()
	print fileC
	# data = []
	# for i in range(5):
	# 	fileName = "listFiles/final"+str(i)+".txt"
	# 	with open(fileName, "r") as f:
	# 		data += json.load(f)

	# fileName = sys.argv[2]
	# with open(fileName, "w+") as f:
	# 	json.dump(data, f)


	# os.system("rm -rf data listFiles")