#coding:utf-8
from sklearn.externals import joblib
from utils import createDocVec
import cPickle

f = file('table_idf.pkl','r')
table_idf = cPickle.load(f)
f.close()
topic = {0:'finance',1:'not finance'}
def detect(doc):
    vec = createDocVec(doc, table_idf)
    clf = joblib.load('../model/gbdt_v1.m')
    y = clf.predict(vec)
    #print y
    #p = clf.predict_prob(vec)
    return [topic[ele] for ele in y]
#a test
if __name__=='__main__':
    f = file('../data/test/not_finance/new_10.txt')
    doc = f.read()
    f.close()
    print detect(doc)
    