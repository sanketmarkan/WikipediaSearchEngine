from mapperReducer import *


def loop(data, fileC, catIn):
	global tdlist, stemmer, count, fileNo, proc
	for item in data:
		if item not in stop_words:
			item = stemmer.stemWord(item)
			no = (ord(item[0])-ord('a'))/5
			no = min(no, 4)
			if catIn!=1:
				no = 0
			tdlist[catIn][no].append([item, fileC])
			count[catIn] += 1
			if count[catIn] > 10**6:
				mapp.append(Process(target=mapper,args=(tdlist[catIn], fileNo[catIn], catIn)))
				mapp[-1].start()
				for i in range(nop[catIn]):
					tdlist[catIn][i] = [];
				count[catIn] = 0
				fileNo[catIn] += 1
	

def process(data, fileC):

	# if(fileC>1000):
	# 	return
	categories = re.findall(r"\[\[category:\w.*\]\]", data)
	categories = [x.strip('[').strip(']').split(':')[1] for x in categories]
	
	for category in categories:
		data2 = re.findall(r"[a-zA-Z0-9]+", category)
		loop(data2, fileC, 2)
	
	data2 = re.findall(r"\{\{infobox[^\}]*\}\}", a)[0].strip("{").strip("}").split()[1:]
	loop(data2, fileC, 3)

	data = re.sub("\{\{[^\}]*\}\}|\[\[file:[^\]]*\]\]|\[\[category:[^\]]*\]\]", " ", data)
	data = re.findall(r"[a-zA-Z]+", data)
	loop(data, fileC, 1)

if __name__ == "__main__":

	global count, proc, tdlist, fileNo, stop_words, stemmer, lis, mapp
	stop_words = set(stopwords.words('english'))
	stemmer = Stemmer.Stemmer('english')
	proc = 0
	count = [0]*nof
	mapp = []

	tdlist = [0]*nof
	for i in range(nof):
		tdlist[i] = [0]*nop[i]
		for j in range(nop[i]):
			tdlist[i][j] = []
	fileNo = [1]*nof
	lis = []

	tree = et.parse(sys.argv[1])
	root = tree.getroot()
	fileC = 1
	print "parsed"
	os.system("rm -rf data; mkdir data")
	os.system("rm -rf listFiles; mkdir listFiles")
	os.system("rm -rf Index; mkdir Index")

	for child in root:
		if(child.tag.endswith('page')):
			for t in child:
				fileName = "data/"+ str(fileC) + '.txt'
				with open(fileName,"w+") as f:
					if(t.tag.endswith('title')):
						if (t.text):
							f.write(t.text)
							f.write("\n")
							data = re.findall(r"[a-zA-Z]+", t.text.lower())
							loop(data, fileC, 0)
					if(t.tag.endswith('revision')):
						for c in t:
							if c.tag.endswith('text'):
								if (c.text):
									f.write(c.text)
									process(c.text.lower(), fileC)
								
			fileC += 1

	for i in range(nof):
		if count[i] > 0:
			mapp.append(Process(target=mapper,args=(tdlist[i], fileNo[i], i)))
			mapp[-1].start()
			fileNo[i] += 1

	for proc in mapp:
		proc.join()

	for j in range(nof):
		for i in range(nop[j]):
			lis.append(Process(target=reducer, args=(i, fileNo[j], j)))
			lis[-1].start()
	for proc in lis:
		proc.join()
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