from importFile import *
import operator, subprocess
from ast import literal_eval

if __name__ == "__main__":

	query = raw_input("Enter Your Query: ")
	# query = "love go"
	stop_words = set(stopwords.words('english'))
	stemmer = Stemmer.Stemmer('english')
	se = set()
	score = {}

	bin = [0]*5
	dic = [0]*5
	for i in range(5):
		bin[i] = []
	query = re.findall(r"[a-zA-Z]+", query.lower())

	for word in query:
		if word not in stop_words:
			word = stemmer.stemWord(word)
			no = (ord(word[0])-ord('a'))/5
			no = min(no, 4)
			bin[no].append(word)

	for i in range(5):
		if len(bin[i]) > 0:
			fileName = "listFiles/dict"+str(i)+".txt"
			with open(fileName, "r") as f:
				dic[i] = json.load(f)
			fileName = "listFiles/champ"+str(i)+".txt"
			# with open(fileName, "r") as f:
			# 	champ = json.load(f)

			for word in bin[i]:
				if word in dic[i]:
					ind = dic[i][word]
					cmd = 'sed "'+ str(ind) +'q;d" '+ str(fileName)
					output = literal_eval(subprocess.check_output(cmd, shell=True)[:-1])
					for doc in output:
						se.add(doc)
						score[doc] = 0

	for i in range(5):
		if len(bin[i]) > 0:
			fileName = "listFiles/final"+str(i)+".txt"
			# with open(fileName, "r") as f:
			# 	index = json.load(f)
			for word in bin[i]:
				if word in dic[i]:
					N = 72325
					ind = dic[i][word]
					cmd = 'sed "'+ str(ind) +'q;d" '+ str(fileName)
					output = literal_eval(subprocess.check_output(cmd, shell=True)[:-1])
					idf = math.log(float(N)/float(output[0]))
					print word, idf
					for freq, doc in output[1]:
						if doc in se:
							freq = 1 + math.log(freq)
							score[doc] += freq*idf

	result = sorted(score.items(), key=operator.itemgetter(1), reverse=True)[:10]
	result = [int(x[0]) for x in result]
	# for doc in result:
	# 	cmd = "cat data/" + str(doc) +".txt | grep -io jon  | wc -l"
	# 	a = subprocess.check_output(cmd, shell=True)[:-1]
		
	# 	cmd = "cat data/" + str(doc) +".txt | grep -io snow  | wc -l"
	# 	b = subprocess.check_output(cmd, shell=True)[:-1]
		
	# 	print doc, (a, b)
	
	print result