from gensim import corpora, models, similarities
import numpy

def search(search_kw):
    dictionary = corpora.Dictionary.load('simul.dict')
    corpus = corpora.MmCorpus('simul.mm')
    lsi = models.LsiModel.load('model.lsi')
    docNames = numpy.load('index_dict.npy').item()
 
    vec_bow = dictionary.doc2bow(search_kw.lower().split())
    vec_lsi = lsi[vec_bow]
    index = similarities.MatrixSimilarity(lsi[corpus])
    sims = index[vec_lsi]
    result = sorted(enumerate(sims), key=lambda item: -item[1])
    result_files = []
    for r in result:
        result_files.append(docNames[r[0]])
    return(result_files)
 #   return(result)

def main():
    return_lst = search('political military')
    return(return_lst)

if __name__ == "__main__":
    return_lst = main()
    print(return_lst)
