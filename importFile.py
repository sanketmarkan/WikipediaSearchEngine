import datrie, string, pickle
import re, codecs, os, time
from multiprocessing import Manager, Process
import xml.etree.ElementTree as et
from nltk.corpus import stopwords
import Stemmer
import json

import sys
reload(sys)
sys.setdefaultencoding('utf-8')