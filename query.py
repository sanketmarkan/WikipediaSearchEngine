from importFile import *
import operator, subprocess
from ast import literal_eval

if __name__ == "__main__":


	dic = [0]*nof
	for i in range(nof):
		dic[i] = [0]*nop[i]
		for j in range(nop[i]):
			dic[i][j] = []

	query = raw_input("Enter Your Query: ")
	while query != 'EOF':
		stop_words = set(stopwords.words('english'))
		stemmer = Stemmer.Stemmer('english')
		se = set()
		score = {}
		idf = {}
		notindoc = {}
		
		fq = 0
		if query.find(":") != -1:
			fq = 1

		bin = [0]*nof
		for i in range(nof):
			bin[i] = [0]*nop[i]
			for j in range(nop[i]):
				bin[i][j] = []

		if fq ==0:
			query = re.findall(r"[a-zA-Z0-9]+", query.lower())
			for word in query:
				if word not in stop_words:
					word = stemmer.stemWord(word)
					for i in range(1):
						no = getBin(word[0], i)
						bin[i][no].append(word)
		else:
			for i in range(nof):
				delim = field2[i]+":"
				tok = query.split(delim)
				if len(tok) > 1:
					tok = tok[1]
					print tok
					tok = re.sub("b:.*", " ", tok)
					tok = re.sub("i:.*", " ", tok)
					tok = re.sub("t:.*", " ", tok)
					tok = re.sub("c:.*", " ", tok)
					tok = re.findall(r"[a-zA-Z0-9]+", tok.lower())
					for word in tok:
						if word not in stop_words:
							word = stemmer.stemWord(word)
							no = getBin(word[0], i)		
							bin[i][no].append(word)
		print bin
		cmd = 'ls data | wc -w'
		N = int(literal_eval(subprocess.check_output(cmd, shell=True)[:-1]))
		for i in range(nof):
			for j in range(nop[i]):
				# if len(bin[i][j]) > 0:
					if dic[i][j] == []:
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
								notindoc[doc] = 0
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
								score[doc] += freq*iddf + 1.5

		print "\n\n"
		results = sorted(score.items(), key=operator.itemgetter(1), reverse=True)[:10]
		results = [int(x[0]) for x in results]
		for result in results:
			fileName = "title/"+ str(result) + ".txt"
			with open(fileName, "r") as f:
				print f.read(), result
		query = raw_input()
