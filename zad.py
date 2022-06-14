import string
import nltk
import re
import copy
import json
from collections import defaultdict
import scipy
import numpy as np
import time

#https://github.com/tomekzaw/agh_sem4_mownit2/blob/master/lab6/Laboratorium_6_Tomasz_Zawadzki.pdf

stopWords = copy.deepcopy(nltk.corpus.stopwords.words('english'))
stemmer = nltk.stem.PorterStemmer()
path = './'
# terms = defaultdict(lambda: 0)

# byc moze bedzie trzeba dodac stuczny dict!!!!!!

def saveDocuments(documents):
    filePath = path + '/documents.json'
    jsonObj = json.dumps(documents, indent=4)
    out = open(filePath, encoding='utf-8', mode='w')
    out.write(jsonObj)
    out.close()

def saveTerms(terms):
    filePath = path + '/terms.json'
    jsonObj = json.dumps(terms, indent=4)
    out = open(filePath, encoding='utf-8', mode='w')
    out.write(jsonObj)
    out.close()

def loadDocuments():
    filePath = path + '/documents.json'
    f = open(filePath, encoding='utf-8', mode='r')
    jsonObj = json.load(f)
    f.close()
    return jsonObj

def loadTerms():
    filePath = path + '/terms.json'
    f = open(filePath, encoding='utf-8', mode='r')
    jsonObj = json.load(f)
    f.close()
    return jsonObj

def saveTfIdf(TfIdf):
    filePath = path + '/tf-idf'
    scipy.sparse.save_npz(filePath, TfIdf)

def loadTfIdf():
    filePath = path + '/tf-idf'
    return scipy.sparse.load_npz(filePath)

def getContent():
    documents = []
    with open('corpus.txt', 'r', encoding='utf-8') as f:
        corpus = f.read()
        for article in corpus.split('\n\n'):
            name, content = article.split('\n', 1)
            name = name.replace(' ', '_')
            url = f'https://simple.wikipedia.org/wiki/{name}'
            document = {}
            document['name'] = name
            document['content'] = content
            document['url'] = url
            documents.append(document)
    documents = dict(enumerate(documents))
    return documents

def parseContent(documents):
    terms = defaultdict(lambda: 0)
    for document in documents.values():
        content = document['content']
        content.lower()
        content = re.sub('[^a-zA-Z_ 0-9]+', '', content)
        vec = defaultdict(lambda: 0)

        tokens = content.split()
        # for token in nltk.word_tokenize(content):
        for token in tokens:
            if len(token) <= 2:
                continue
            if token in stopWords:
                continue
            stemmedWord = stemmer.stem(token)
            vec[stemmedWord] += 1
            terms[stemmedWord] += 1
        document['vec'] = vec
    terms = dict(enumerate(terms))
    return terms

def createTfIdf(documents, terms):
    n = len(terms.values())
    m = len(documents.values())
    tfIdf = scipy.sparse.lil_matrix((n, m))
    wordVec = defaultdict(lambda: 0)
    for i in range(n):
        for j in range(m):
            term = terms[i]
            vec = documents[j]['vec']
            if term in vec:
                val = vec[term]
                wordVec[i] += 1
            else:
                val = 0
            tfIdf[i, j] = val
    
    idf = []
    for i in range(n):
        if wordVec[i] != 0:
            idf.append(np.log(m/wordVec[i]))
        else:
            print("TO NIE POWINNO SIE ZDARZYC")
            idf.append(0)
    
    for i in range(n):
        for j in range(m):
            tfIdf[i, j] = tfIdf[i, j] * idf[i]
    
    # inaczej nie chce mi zapisać do .npz
    tfIdf = scipy.sparse.csc_matrix(tfIdf)
    
    return tfIdf

# mnozenie macierzy - wierszowa*kolumnowa to jedna wartość
def parseQuery(query, terms):
    n = len(terms.values())
    vec = defaultdict(lambda: 0)

    query.lower()
    query = re.sub('[^a-zA-Z_ 0-9]+', '', query)
    tokens = query.split()
    for i in range(n):
        word = terms[i]
        if word in tokens:
            vec[i] = 1
        else:
            vec[i] = 0
    vec = dict(enumerate(vec))
            


def search(documents, terms, query):
    n = len(terms.values())
    m = len(terms.values())
    q = scipy.sparse.lil_matrix((n, 1))

def main(type):
    if type == 'save':
        timeStart = time.time()

        documents = getContent()
        terms = parseContent(documents)
        tfIdf = createTfIdf(documents, terms)
        saveDocuments(documents)
        saveTerms(terms)
        saveTfIdf(tfIdf)

        timeEnd = time.time()
        print(f"TU PATRZ JAREK\n Time={timeEnd-timeStart} \nPATRZ WYZEJ JAREK")

    else:
        print('dupa')

main('save')