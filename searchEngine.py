import string
import nltk
# nltk.download('stopwords')
import re
import copy
import json
from collections import defaultdict
import scipy
import numpy as np
import time
from save_load import *

#https://github.com/tomekzaw/agh_sem4_mownit2/blob/master/lab6/Laboratorium_6_Tomasz_Zawadzki.pdf

stopWords = copy.deepcopy(nltk.corpus.stopwords.words('english'))
stemmer = nltk.stem.PorterStemmer()
corpusPath = "new-corpus.txt"

def getContent():
    documents = []
    with open(corpusPath, 'r', encoding='utf-8') as f:
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
            if len(token) <= 3:
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
        if i % 100 == 0:
            print(f'Word i-th: {i}')
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
    vec = scipy.sparse.lil_matrix((1, n))

    query = query.lower()
    query = re.sub('[^a-zA-Z_ 0-9]+', '', query)
    queryWords = query.split()
    tokens = []

    for i in range(len(queryWords)):
        tokens.append(stemmer.stem(queryWords[i]))

    for i in range(n):
        word = terms[str(i)]
        if word in tokens:
            vec[0,i] = 1
        else:
            vec[0,i] = 0
    return vec

def get_col(A, j, n):
    col = scipy.sparse.lil_matrix((n, 1))
    for i in range(n):
        col[i, 0] = A[i, j]
    return col

def prob(q, tfIdf, j, n, norms):
    # print("STARTING PROB")
    t1 = time.time()
    Aj = tfIdf[:, j]
    # Aj = get_col(tfIdf, j, n)
    t2 = time.time()
    # print(f"getting col took {t2-t1}s")
    # print("Calcing numerator")
    t1 = time.time()
    numerator = q*Aj
    t2 = time.time()
    # print(f"Calcing numerator took {t2-t1}s")
    # print("Calcing norms")
    t1 = time.time()
    # te normy na upartego da sie jeszcze skrócić, powinno pomóc o tak sekunde albo więcej
    denumerator = scipy.sparse.linalg.norm(q)
    # denumerator *= scipy.sparse.linalg.norm(Aj)
    denumerator *= norms[j]
    t2 = time.time()
    # print(f"Calcing norms took {t2-t1}s")
    # print("DIVISION")
    t1 = time.time()
    res = numerator/denumerator
    t2 = time.time()
    # print(f"Division took {t2-t1}s")
    # print(res)
    return res

def calcSVD(A, k):
    u, s, v = scipy.sparse.linalg.svds(A, k)
    Ar = u @ np.diag(s) @ v
    Ar = scipy.sparse.csc_matrix(Ar)
    print(f"Ar type: {type(Ar)}")
    return Ar

def search(documents, terms, query, tfIdf, norms):
    n = len(terms.values())
    m = len(documents.values())

    q = parseQuery(query, terms)

    cos = scipy.sparse.lil_matrix((1,n))
    for j in range(m):
        # print(f"calc prob for {j} document")
        cos[0,j] = prob(q, tfIdf, j, n, norms)[0, 0]
    resArr = [(cos[0,j], j) for j in range(m)]
    resArr = sorted(resArr, key=lambda tup: tup[0], reverse=True)
    res = []
    for i in range(10):
        article = documents[str(resArr[i][1])]
        website = {}
        website['title'] = article["name"]
        website['url'] = article['url']
        res.append(website)
        # res.append(f"Title: {article['name']}, URL: {article['url']}")
    print(res)
    return res

def getNorms(A):
    norms = []
    for i in range(A.shape[1]):
        col = A[:, i]
        norm = scipy.sparse.linalg.norm(col)
        norms.append(norm)
    norms = np.array(norms)
    return norms 

def doIndexing(svd_k):
    timeStart = time.time()

    documents = getContent()
    terms = parseContent(documents)
    tfIdf = createTfIdf(documents, terms)
    tfIdfNorms = getNorms(tfIdf)
    print("Started to save files")
    saveTfIdf(tfIdf)
    saveTfIdfNorms(tfIdfNorms)
    if svd_k > 0:
        print("Started to calculating SVD")
        tfIdf = calcSVD(tfIdf, svd_k)
        svdNorms = getNorms(tfIdf)
        saveSVDNorms(svdNorms)
        saveSVD(tfIdf)
        print("Ended SVD")
    saveDocuments(documents)
    saveTerms(terms)

    timeEnd = time.time()
    print(f"Saving took: {timeEnd-timeStart}s")

def searchQuery(query, svd_k):
    timeStart = time.time()
    print(f"Starting loading matrices")
    svd_k = int(svd_k)
    terms = loadTerms()
    tfIdf = loadTfIdf()
    norms = loadTfIdfNorms()
    if svd_k > 0:
        tfIdf = loadSVD()
        norms = loadSVDNorms()
    documents = loadDocuments()
    timeEnd = time.time()
    print(f"Ending loading matrices, time: {timeEnd-timeStart} s")
    timeStart = time.time()
    print(f"Starting searching")
    res = search(documents, terms, query, tfIdf, norms)
    timeEnd = time.time()
    print(f"Ended searching, time: {timeEnd-timeStart} s")
    print(tfIdf[25,25])
    return res

#k = 25
# doIndexing(25)
searchQuery("First computer", 10)