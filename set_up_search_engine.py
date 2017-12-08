# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 15:04:39 2017

@author: Ambroise Prevel
"""


from os import listdir
from os.path import join, isdir, isfile

def get_files_from_dir(path_to_dir, r):
    
    if not isdir(path_to_dir):
        return
    for output in listdir(path_to_dir):
        path_to_output = join(path_to_dir, output)
        if isdir(path_to_output):
            get_files_from_dir(path_to_output, r=r)
        elif isfile(path_to_output):
            r.append(path_to_output)
    return(r)
    

from whoosh.fields import Schema, TEXT, ID
from whoosh.analysis import StandardAnalyzer
from nltk.corpus import stopwords


# Création du schéma de l'index
set_of_stopwords = set(stopwords.words('english')).union(set(stopwords.words('french')))
schema = Schema(path=ID(stored=True), 
                title=TEXT(stored=True), 
                content=TEXT(analyzer=StandardAnalyzer(stoplist=set_of_stopwords)))


# Création de l'index

import os.path
from whoosh.index import create_in
from whoosh.index import open_dir
from whoosh.qparser import QueryParser

if not os.path.exists("index"):
    os.mkdir("index")
    ix = create_in("index", schema)

ix = open_dir("index")

# Si pas encore fait, ajout des docs dans l'index

if ix.doc_count() != 3376:
    writer = ix.writer()
    
    result = []
    files_to_import = get_files_from_dir("C:\\Users\\Ambroise Prevel\\Dropbox\\HEC\\Cours\\Digital\\DGA\\formated_data",
                                         r = result)
    for f in files_to_import:
        with open(f, 'r', encoding='utf-8', errors='surrogateescape') as handle:
            cont = handle.read()
        titl = f.split('\\')[-1]
        writer.add_document(title=titl, content=cont, path=f)
        print(titl)    
    print('COMMITING')
    writer.commit()


from whoosh.qparser import MultifieldParser, FuzzyTermPlugin


def search_in_index(search_kw, index):
    '''
    search_kw: ce que rentre l'utilisateur dans la barre de recherche
    index: l'index ouvert (objet ix dans le code qui précède)
    
    La fonction renvoie un dictionnaire avec pour clefs:
        - results: une liste contenant des dictionnaires. Chaque dictionnaire 
        correspond à un résultat de recherche. Le premier élément de la liste 
        est le meilleur résultat. Les dictionnaires on deux clefs: 'title' avec 
        le titre du doc, et 'path' avec le chemin (vers le doc texte, pour le moment)
        - suggestions: dictionnaire de suggestion qui propose une éventuelle 
        correction pour chaque mot entré par l'utilisateur. A voir comment on 
        mélange les suggestions des différents mots pour fournir des suggestions 
        complètes

    '''
    parser = MultifieldParser(["content", "title"], index.schema) #on utilise un MultifieldParser pour rechercher à la fois dans le titre et dans le contenu
    parser.add_plugin(FuzzyTermPlugin()) #on rajoute un plugin de FuzzyMatching pour pouvoir chercher au delà des mots exacts
    searcher = index.searcher()
    to_parse = ' '.join([i+'~1' for i in search_kw.split(' ')]) #on transforme la requête utilisateur pour la mettre en format compréhensible par le plugin de FuzzyMatching
    myquery = parser.parse(to_parse)
    r = searcher.search(myquery)
    #on récupère les résultats pour pouvoir fermer le searcher  par la suite   
    results = []
    for res in r:
        results.append({'title': res['title'], 'path': res['path']})
    #on set-up le correcteur et on stock ce qu'il propose pour chaque mot tapé
    corrector = searcher.corrector("content")
    suggestions = {}    
    for kw in search_kw.split(' '):
        suggestions[kw] = corrector.suggest(kw)
    
    searcher.close() #on ferme le seacher
    
    return {'results': results, 'suggestions': suggestions}    

#démo de cette fonction:
r = search_in_index('pomitical tentions', ix)
resultats = r['results']
print("MEILLEUR RESULTAT:")
print(resultats[0])
print("\nSUGGESTIONS DE MOTS CLEFS")
suggestions = r['suggestions']
print(suggestions)



    

    
    

