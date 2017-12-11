# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 15:04:39 2017
@author: Ambroise Prevel
"""

from os import listdir
from os.path import join, isdir, isfile
from whoosh.fields import Schema, TEXT, ID
from whoosh.analysis import StandardAnalyzer
from nltk.corpus import stopwords
import os.path
from whoosh.index import create_in
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser, FuzzyTermPlugin
import nltk

def get_files_from_dir(path_to_dir, r):
    """
    recursive function to retrieve the paths of the files
    """
    
    if not isdir(path_to_dir):
        return
    for output in listdir(path_to_dir):
        path_to_output = join(path_to_dir, output)
        if isdir(path_to_output):
            get_files_from_dir(path_to_output, r=r)
        elif isfile(path_to_output):
            r.append(path_to_output)
    return(r)

def create_index():
    """
    Create a whoosh index for all files
    """
    nltk.download('stopwords')
    # Création du schéma de l'index
    set_of_stopwords = set(stopwords.words('english')).union(set(stopwords.words('french')))
    schema = Schema(path=ID(stored=True), title=TEXT(stored=True), content=TEXT(analyzer=StandardAnalyzer(stoplist=set_of_stopwords)))
    # Création de l'index
    if not os.path.exists("index"):
        os.mkdir("index")
        ix = create_in("index", schema)
    ix = open_dir("index")
    writer = ix.writer()
    result = []
    files_to_import = get_files_from_dir("/Users/thebarn/challenge-dga/formated_data", r = result)
    for f in files_to_import:
    #on ferme le seacher
        with open(f, 'r', encoding='utf-8', errors='surrogateescape') as handle:
            cont = handle.read()
        titl = f.split('\\')[-1]
        writer.add_document(title=titl, content=cont, path=f)
        print(titl)    
    print('COMMITING')
    writer.commit()

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
    #on utilise un MultifieldParser pour rechercher à la fois dans le titre et dans le contenu
    parser = MultifieldParser(["content", "title"], index.schema)
    #on rajoute un plugin de FuzzyMatching pour pouvoir chercher au delà des mots exacts
    parser.add_plugin(FuzzyTermPlugin()) 
    searcher = index.searcher()
    #on transforme la requête utilisateur pour la mettre en format compréhensible par le plugin de FuzzyMatching
    to_parse = ' '.join([i+'~1' for i in search_kw.split(' ')]) 
    myquery = parser.parse(to_parse)
    #on récupère les résultats pour pouvoir fermer le searcher  par la suite   
    r = searcher.search(myquery)
    results = []
    for res in r:
        results.append({'title': res['title'], 'path': res['path']})
    #on set-up le correcteur et on stock ce qu'il propose pour chaque mot tapé
    corrector = searcher.corrector("content")
    suggestions = {}    
    for kw in search_kw.split(' '):
        suggestions[kw] = corrector.suggest(kw)
    #on ferme le seacher
    searcher.close() 
    return {'results': results, 'suggestions': suggestions}    


def test_search_function():
    ix = open_dir("index")
    #démo de cette fonction:
    r = search_in_index('pomitical tentions', ix)
    print(r)
    resultats = r['results']
    print("MEILLEUR RESULTAT:")
    print(resultats[0])
    print("\nSUGGESTIONS DE MOTS CLEFS")
    suggestions = r['suggestions']
    print(suggestions)

if __name__ == "__main__":
    #create_index()
    test_search_function()
