#authors pdespres, fbabin

import numpy
import os
import subprocess
import re
from os import listdir
from os.path import isfile, join
import fnmatch
from nltk.corpus import stopwords

files = []
for root, dirnames, filenames in os.walk('.'):
    for filename in fnmatch.filter(filenames, '*.txt'):
        files.append(os.path.join(root, filename))

raw_corpus = []
for e in files:
    with open(e) as f:
        str = ""
        for line in f:
            line = re.sub(' +', ' ', line)
            line = line.replace("(", "")
            line = line.replace(")", "")
            str += line
        raw_corpus.append(str)
        print(e)

stoplist = set(stopwords.words('english')).union(set(stopwords.words('french')))
#set('for a of the and to in le la mais ou donc or ni car + on in oui non'.split(' '))
#stoplist = set('for a of the and to in le la mais ou donc or ni car'.split(' '))
# Lowercase each document, split it by white space and filter out stopwords
texts = [[word for word in document.lower().split() if word not in stoplist]
    for document in raw_corpus]

# Count word frequencies
from collections import defaultdict
frequency = defaultdict(int)
for text in texts:
    for token in text:
        frequency[token] += 1

# Only keep words that appear more than once
processed_corpus = [[token for token in text if frequency[token] > 1] for text in texts]
from gensim import corpora

dictionnary = corpora.Dictionnary(processed_corpus)
print(dictionnary)
