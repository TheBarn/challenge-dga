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
    for filename in fnmatch.filter(filenames, 'validation.txt'):
        files.append(os.path.join(root, filename))

contractions = re.compile(r"'|-|\"")
# all non alphanumeric
symbols = re.compile(r'(\W+)', re.U)
# single character removal
singles = re.compile(r'(\s\S\s)', re.I|re.U)
# separators (any whitespace)
seps = re.compile(r'\s+')

# cleaner (order matters)
def clean(text):
    text = text.lower()
    text = contractions.sub('', text)
    text = symbols.sub(r' \1 ', text)
    text = singles.sub(' ', text)
    text = seps.sub(' ', text)
    return text

raw_corpus = []
for e in files:
    with open(e) as f:
        str = ""
        for line in f:
            str += clean(line)
        raw_corpus.append(str)
        print(e)

stoplist = set(stopwords.words('english')).union(set(stopwords.words('french')))
texts = [[word for word in document.split() if word not in stoplist]
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
dictionary.save('tmp/simul.dict')
print(dictionnary)

corpus = [dictionary.doc2bow(text) for text in texts]
corpora.Mmcorpus.serialize('/tmp/simul.mm', corpus)

from gensim import models
tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]
lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=)
corpus_lsi = lsi[corpus_tfidf]
lsi.save('/tmp/model.lsi')
