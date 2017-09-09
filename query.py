from importFile import *
import operator
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
			print word
			bin[no].append(word)

	for i in range(5):
		if len(bin[i]) > 0:
			fileName = "listFiles/dict"+str(i)+".txt"
			with open(fileName, "r") as f:
				dic[i] = pickle.load(f)
			fileName = "listFiles/champ"+str(i)+".txt"
			with open(fileName, "r") as f:
				champ = json.load(f)

			for word in bin[i]:
				if word in dic[i]:
					ind = dic[i][word]
					for doc in champ[ind][1]:
						se.add(doc)
						score[doc] = 0

	for i in range(5):
		if len(bin[i]) > 0:
			fileName = "listFiles/final"+str(i)+".txt"
			with open(fileName, "r") as f:
				index = json.load(f)
			for word in bin[i]:
				if word in dic[i]:
					ind = dic[i][word]
					for freq, doc in index[ind][2]:
						if doc in se:
							score[doc] += freq

	result = sorted(score.items(), key=operator.itemgetter(1), reverse=True)[:10]
	print result