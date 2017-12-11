#authors pdespres, fbabin

import re
from os import listdir
from os.path import isfile, join, isdir
from nltk.corpus import stopwords

def get_files_from_dir(path_to_dir, files):
    if not isdir(path_to_dir):
        return
    for output in listdir(path_to_dir):
        path_to_output = join(path_to_dir, output)
        if isdir(path_to_output):
            get_files_from_dir(path_to_output, files)
        elif isfile(path_to_output):
            files.append(path_to_output)
    return(files)

def get_corpus(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='surrogateescape') as f:
        corpus = f.read()
        corpus = re.sub(' +', ' ', corpus)
        corpus = corpus.replace("(", "")
        corpus = corpus.replace(")", "")
    return corpus

def get_words_set(dir_path):
    files = []
    files = get_files_from_dir(dir_path, files)
    stoplist = set(stopwords.words('english')).union(set(stopwords.words('french')))
    words_set = []
    for f_path in files:
        corpus = get_corpus(f_path)
        words_set += [word for word in corpus.lower().split() if word not in stoplist]
    return words_set

def get_frequency(words_set):
    frequency = {}
    for word in words_set:
        if word not in frequency:
            frequency[word] = 1
        else:
            frequency[word] += 1
    return frequency

def main():
    words_set = get_words_set('/Users/thebarn/challenge-dga/formated_data')
    frequency = get_frequency(words_set)
    processed_corpus = [token for token in words_set if frequency[token] > 1]
    return processed_corpus

if __name__ == "__main__":
    processed_corpus = main()
    print(processed_corpus)
