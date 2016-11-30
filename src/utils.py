#coding:utf-8

import jieba,os,math
import cPickle
import conf.config as cf
import numpy as np
def idf():
    vocab = {}
    Path = os.listdir(cf.DATA_ROOT)
    #print Path
    D = 0
    for ele in Path:
        tpaths = os.listdir(os.path.join(cf.DATA_ROOT,ele))
        #print tpaths
        for tpath in tpaths:
            filePaths = os.listdir(os.path.join(cf.DATA_ROOT,ele,tpath))
            #print filePaths
            for fpath in filePaths:
                f = file(os.path.join(cf.DATA_ROOT,ele,tpath,fpath),'r')
                content = f.read()
                f.close()
                D += 1
                words = jieba.cut(content)
                words = list(set([word.strip() for word in words]))
                for word in words:
                    try:
                        vocab[word] += 1
                    except:
                        vocab[word] = 1
    
    table_idf = [(item[0],math.log(1.*D/(1+item[1]),10)) for item in vocab.items()]
    table_idf.sort(key=lambda x:x[1],reverse=True)
    f = file('table_idf.pkl','w')
    cPickle.dump(table_idf,f)
    f.close()
    
def createDocVec(doc,table_idf):
    vec = np.zeros(len(table_idf))
    words = jieba.cut(doc)
    doc_vocab = {}
    for ele in words:
        try:
            doc_vocab[ele] += 1
        except:
            doc_vocab[ele] = 1
    for ind,ele in enumerate(table_idf):
        try:
            vec[ind] = ele[1]*doc_vocab[ele[0]]
        except:
            continue
    return vec

if __name__=='__main__':
    idf()