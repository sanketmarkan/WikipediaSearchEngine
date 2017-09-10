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

field['t'] = 0
field['b'] = 1
field['c'] = 2
field['i'] = 3
nof = 4

nop = [1,5,1,1]