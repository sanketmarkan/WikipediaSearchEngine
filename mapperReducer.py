from importFile import *

# trie = datrie.Trie(string.ascii_lowercase+string.digits+":")
def mapper(tdlist, fileNo):
	print fileNo
	for i in range(5):
		fileName = "listFiles/"+str(fileNo)+"-"+str(i)+".txt"
		with open(fileName, "w+") as f:
			json.dump(tdlist[i], f)


def reducer(bin, fileC):
	print str(bin)+"started"
	trie = datrie.Trie(string.ascii_lowercase)
	start = time.time()
	for i in range(1, fileC):
		fileName = "listFiles/"+str(i)+"-"+str(bin)+".txt"
		# while os.path.isfile(fileName) == False:
		# 	time.sleep(3)
		# try:
		with open(fileName, "rw+") as f:
			data = json.load(f)
		# print bin, i
		# except:
		# 	time.sleep(3)
		# 	with open(fileName, "rw+") as f:
		# 		data = json.load(f)
		for word, doc in data:
			word = word.decode("utf-8")
			doc = str(doc).decode("utf-8")
			# word += "::" + doc
			# 	trie[word] = 0
			if word not in trie:
				trie[word] = datrie.Trie(string.digits)
			if doc not in trie[word]:
				trie[word][doc] = 0
			trie[word][doc] += 1
			# trie[word] += 1

	# trie.save(fileName)
	# return


	lisoflis = []
	champ = []
	c = 1
	dic = {}
	fileName = "listFiles/final"+str(bin)+".txt"
	fileName2 = "listFiles/champ"+str(bin)+".txt"

	with open(fileName, "w+") as f:
		with open(fileName2, "w+") as f2:
			for key in trie.keys():
				tr = trie[key]
				lis = []
				for doc in tr.keys():
					lis.append([tr[doc], doc])
				# lisoflis.append([key, len(tr.keys()), lis])
				f.write(str([len(tr.keys()), lis])+'\n')
				lis.sort()
				lis.reverse()
				lis = [x[1] for x in lis[:1000]]
				lis.sort()
				# champ.append([key, lis])
				f2.write(str(lis)+'\n')
				dic[key] = c
				c += 1


		# json.dump(lisoflis, f)
	
		# json.dump(champ, f)

	fileName = "listFiles/dict"+str(bin)+".txt"
	with open(fileName, "w+") as f:
		pickle.dump(dic, f)
	
	end = time.time()
	print bin, end - start
	# 39.76939039228
	# 18.704721736902
