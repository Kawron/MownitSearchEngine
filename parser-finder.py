import nltk
import re
import json
import numpy as np
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from collections import defaultdict
import copy
import os
import wikipedia
import random

dictionary = defaultdict(lambda: 0)
dictionaryArr = []
articleWords = []
ps = PorterStemmer()
stopWords = copy.deepcopy(stopwords.words('english'))

def get_col(A, j):
    n = len(dictionaryArr)
    m = len(articleWords)
    col = np.zeros((n,1))

    for i in range(n):
        col[i] = A[i][j]
    return col

def read_indexes():
    files = os.listdir("./index_res")
    
    cnt = 0
    for file_name in files:
        file = open("./index_res/"+file_name, encoding="utf-8", mode='r')
        cnt += 1
        try:
            json_object = json.load(file)
            title = json_object['title']
            vector = json_object['val']
            articleWords.append((title,vector))
        except Exception as e:
            print(f"Error in: {file_name}, \n{e}")
        finally:
            file.close()
    
    file = open("./dictionary.json", encoding="utf-8", mode='r')
    json_object = json.load(file)
    dictionaryFromFile = json_object['dict']
    for key in dictionaryFromFile.keys():
        dictionaryArr.append(key)


def save_indexes():
    dictionaryArt = {}
    for art in articleWords:
        dictionaryArt['title'] = art[0]
        dictionaryArt['val'] = art[1]
        jsonObject = json.dumps(dictionaryArt, indent = 4)
        out = open(f"./index_res/{art[0]}.json", encoding='utf-8', mode='w')
        out.write(jsonObject)
        out.close()
    out = open(f"./dictionary.json",encoding='utf-8', mode='w')
    d = {}
    d['dict'] = dictionary
    jsonObject = json.dumps(d, indent = 4)
    out.write(jsonObject)
    out.close()

        
def create_article_vector(article_path):
    file = open(article_path, encoding="utf-8", mode='r')
    words = defaultdict(lambda:0)
    title = None
    try:
        json_object = json.load(file)
        title = json_object["title"]
        content = json_object["content"]
        content = content.lower()
        content = re.sub('[^a-zA-Z_ ]+', '', content)
        content = content.split()
        for word in content:
            if word in stopWords:
                continue
            if len(word) <= 1:
                continue
            stemmedWord = ps.stem(word)
            words[stemmedWord] += 1
            dictionary[stemmedWord] += 1
    except Exception as e:
        print(f"Error in: {article_path}, \n{e}")
    finally:
        file.close()
    return title,words

def simplify_dict():
    keys = [key for key in dictionary.keys()]
    for key in keys:
        if dictionary[key] <= 5:
            dictionary.pop(key, None)

def fill_matrix(A):
    n = len(dictionaryArr)
    m = len(articleWords)
    for i in range(n):
        for j in range(m):
            if articleWords[j][1].get(dictionaryArr[i]) != None:
                A[i][j] = articleWords[j][1][dictionaryArr[i]]
            else:
                A[i][j] = 0
    return A

def IDF(A):
    n = len(dictionaryArr)
    m = len(articleWords)
    for i in range(n):
        for j in range(m):
            if articleWords[j][1].get(dictionaryArr[i]) != None:
                A[i][j] = len(articleWords)/articleWords[j][1][dictionaryArr[i]]
            else:
                A[i][j] = 0
            pass
    return A

def find(words, A, printN):
    n = len(dictionaryArr)
    m = len(articleWords)

    res = []

    Q = np.zeros((n,1))
    for word in words:
        # get index of array in elem
        # word = ps.stem(word)
        Q[dictionaryArr.index(word)][0] = 1

    for j in range(m):
        prob = probability_func(Q, A, j)
        res.append([(prob, articleWords[j][0])])
    res.sort(key=lambda x: x[0], reverse=True)
    for i in range(printN):
        print(wikipedia.page(res[i][0]).url)

def probability_func(Q, A, j):
    Aj = get_col(A,j)
    numerator = np.transpose(Q) @ Aj
    denumerator = np.linalg.norm(A)*np.linalg.norm(Aj)
    return numerator[0][0]/denumerator

def main(numOfArticles, printN, words, readIndex):
    if readIndex == True:
        read_indexes()
        n = len(dictionaryArr)
        m = len(articleWords)
        A = np.zeros((n, m))
        print(n,m)
        A = fill_matrix(A)
        find(words, A, printN)
    else:
        files = os.listdir("./resv2")
        random.shuffle(files)
        cnt = 0
        for file in files:
            cnt += 1
            res = create_article_vector("./resv2/"+file)
            if res[0] != None:
                articleWords.append(create_article_vector("./resv2/"+file))
            if cnt > numOfArticles:
                break
        save_indexes()
        simplify_dict()

        print(dictionary.keys())

main(1000, 10, ['computer'], True)