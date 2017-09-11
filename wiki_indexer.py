from mapperReducer import *
import xml.sax.handler

class MyHandler(xml.sax.handler.ContentHandler):
	def __init__(self):
		self.name = ""
		self.title_data = ""
		self.text_data = ""
		self.fileC = 1
	def startElement(self,name,attrs):
		self.name = name
		if(name=='title'):
			self.title_data = ""
		elif(name=='text'):
			self.text_data = ""
	def characters(self,data):
		if(self.name =='title'):
			self.title_data += data
		elif(self.name == 'text'):
			self.text_data += data
	def endElement(self,name):
		if(self.name=='title'):
			fileName = "title/"+ str(self.fileC) + '.txt'
			with open(fileName,"w+") as f:
				data = re.findall(r"[a-zA-Z]+", self.title_data.lower())        	
				loop(data, self.fileC, 1)
				f.write(self.title_data)
		elif(self.name=='text'):
			fileName = "data/"+ str(self.fileC) + '.txt'
			with open(fileName,"w+") as f:
				process(self.text_data.lower(), self.fileC)
				self.fileC += 1
				f.write(self.text_data)

def loop(data, fileC, catIn):
	global tdlist, stemmer, count, fileNo, proc
	for item in data:
		if item not in stop_words:
			item = stemmer.stemWord(item)
			no = getBin(item[0], catIn)
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
	
	data2 = re.findall(r"\{\{infobox[^\}]*\}\}", data)
	if len(data2):
		data2 = re.findall(r"[a-zA-Z0-9]+", data2[0])[1:]
		loop(data2, fileC, 3)

	data = re.sub("\{\{[^\}]*\}\}|\[\[file:[^\]]*\]\]|\[\[category:[^\]]*\]\]", " ", data)
	data = re.findall(r"[a-zA-Z]+", data)
	loop(data, fileC, 0)

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

	# tree = et.parse(sys.argv[1])
	# root = tree.getroot()
	fileC = 1
	os.system("rm -rf data; mkdir data")
	os.system("rm -rf listFiles; mkdir listFiles")
	os.system("rm -rf Index; mkdir Index")
	os.system("rm -rf title; mkdir title")
	parser = xml.sax.make_parser()
	handler = MyHandler()
	parser.setContentHandler(handler)
	parser.parse(open(sys.argv[1]))
	print "parsed"
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