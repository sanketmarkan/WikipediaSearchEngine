import datrie, string
import re, codecs, os, time
from multiprocessing import Manager, Process
import xml.etree.ElementTree as et
from nltk.corpus import stopwords
import Stemmer
import json, math

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

field = {}
field2 = {}

field['b'] = 0
field['t'] = 1
field['c'] = 2
field['i'] = 3

field2[0] = 'b'
field2[1] = 't'
field2[2] = 'c'
field2[3] = 'i'
nof = 4

nop = [5,1,1,1]

def getBin(cha, catIn):
	no = (ord(cha)-ord('a'))/5
	no = min(no, 4)
	if no < 0:
		no = 4
	if catIn!=0:
		no = 0
	return no