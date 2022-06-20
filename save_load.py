import json
import scipy
import numpy as np

path = './cache'

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
    filePath = path + '/tf-idf.npz'
    scipy.sparse.save_npz(filePath, TfIdf)

def loadTfIdf():
    filePath = path + '/tf-idf.npz'
    return scipy.sparse.load_npz(filePath)

def saveSVD(SVD):
    filePath = path + '/SVD.npz'
    scipy.sparse.save_npz(filePath, SVD)
    # f = open(filePath, mode='wb')
    # np.save(f, SVD)
    # f.close()

def loadSVD():
    filePath = path + '/SVD.npz'
    return scipy.sparse.load_npz(filePath)
    # f = open(filePath, mode='rb')
    # SVD = np.load(f)
    # f.close()
    # return SVD
    
def saveSVDNorms(norms):
    filePath = path + '/SVD_norms.csv'
    np.savetxt(filePath, norms, delimiter=',')


def saveTfIdfNorms(norms):
    filePath = path + '/TfIdf_norms.csv'
    np.savetxt(filePath, norms, delimiter=',')

def loadSVDNorms():
    filePath = path + '/SVD_norms.csv'
    norms = np.loadtxt(filePath, delimiter=',')
    return norms

def loadTfIdfNorms():
    filePath = path + '/TfIdf_norms.csv'
    norms = np.loadtxt(filePath, delimiter=',')
    return norms