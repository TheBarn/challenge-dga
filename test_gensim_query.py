from gensim import corpora, models, similarities
dictionary = corpora.Dictionary.load('/tmp/simul.dict')
corpus = corpora.MmCorpus('/tmp/simul.mm')
lsi = models.load('/tmp/model.lsi')

search = ? # saisie de recherche
vec_bow = dictionary.doc2bow(doc.lower().split())
vec_lsi = lsi[vec_bow]

index = similarities.MatrixSimilarity(lsi[corpus])
sims = index[vec_lsi]
sims = sorted(enumerate(sims), key=lambda item: -item[1])
print(sims)
