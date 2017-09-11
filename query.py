from importFile import *
import operator, subprocess
from ast import literal_eval

if __name__ == "__main__":

	query = raw_input("Enter Your Query: ")
	# query = "love go"
	# import wikipedia
	# print wikipedia.search(query)
	# query = ""

	stop_words = set(stopwords.words('english'))
	stemmer = Stemmer.Stemmer('english')
	se = set()
	score = {}
	idf = {}
	
	fq = 0
	if query.find(":") != -1:
		fq = 1
		re.sub(":", " ", query)
	query = re.findall(r"[a-zA-Z]+", query.lower())
	# query = query.split()

	dic = [0]*nof
	bin = [0]*nof
	for i in range(nof):
		bin[i] = [0]*nop[i]
		dic[i] = [0]*nop[i]
		for j in range(nop[i]):
			bin[i][j] = []
			dic[i][j] = []


	if fq ==0:
		for word in query:
			if word not in stop_words:
				word = stemmer.stemWord(word)
				for i in range(nof):
					no = getBin(word[0], i)
					bin[i][no].append(word)
	else:
		i = 0
		while i < len(query):
			cat = field[query[i]]
			word = query[i+1]
			if word not in stop_words:
				word = stemmer.stemWord(word)
				no = getBin(word[0], cat)		
				bin[cat][no].append(word)
			i += 2
	
	cmd = 'ls data | wc -w'
	N = int(literal_eval(subprocess.check_output(cmd, shell=True)[:-1]))
	for i in range(nof):
		for j in range(nop[i]):
			# if len(bin[i][j]) > 0:
				fileName = "Index/dict"+str(j)+"-"+str(i)+".txt"
				with open(fileName, "r") as f:
					dic[i][j] = json.load(f)
				fileName = "Index/champ"+str(j)+"-"+str(i)+".txt"
				for word in bin[i][j]:
					if word in dic[i][j]:
						ind, occ = dic[i][j][word]
						cmd = 'sed "'+ str(ind) +'q;d" '+ str(fileName)
						output = literal_eval(subprocess.check_output(cmd, shell=True)[:-1])
						for doc in output:
							se.add(doc)
							score[doc] = 0
						try:
							idf[word] += occ
						except:
							idf[word] = occ

	for key, val in idf.iteritems():
		val = math.log(float(N)/float(val))
		idf[key] = val
	
	for i in range(nof):
		for j in range(nop[i]):
			fileName = "Index/final"+str(j)+"-"+str(i)+".txt"
			for word in bin[i][j]:
				if word in dic[i][j]:
					ind = dic[i][j][word][0]
					cmd = 'sed "'+ str(ind) +'q;d" '+ str(fileName)
					output = literal_eval(subprocess.check_output(cmd, shell=True)[:-1])
					iddf = idf[word]
					print word, iddf
					for freq, doc in output:
						if doc in se:
							freq = 1 + math.log(freq)
							score[doc] += freq*iddf

	print "\n\n"
	results = sorted(score.items(), key=operator.itemgetter(1), reverse=True)[:10]
	results = [int(x[0]) for x in results]
	for result in results:
		fileName = "title/"+ str(result) + ".txt"
		with open(fileName, "r") as f:
			print f.read(), result
