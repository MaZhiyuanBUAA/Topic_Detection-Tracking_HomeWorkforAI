#coding:utf-8
import conf.config as cf
import os,cPickle,random
from utils import createDocVec
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.externals import joblib

def getTrainSet():
    f = file('table_idf.pkl','r')
    table_idf = cPickle.load(f)
    print len(table_idf)
    f.close()
    topic0 = ['finance']
    topic1 = ['entertainment','military','technology','world']
    topic0samples = []
    topic1samples = []
    for ele in topic0:
        tmp = os.listdir(os.path.join(cf.TRAIN_ROOT,ele))
        tmp = [os.path.join(cf.TRAIN_ROOT,ele,path) for path in tmp]
        topic0samples += tmp
    for ele in topic1:
        tmp = os.listdir(os.path.join(cf.TRAIN_ROOT,ele))
        tmp = [os.path.join(cf.TRAIN_ROOT,ele,path) for path in tmp]
        topic1samples += tmp
    
    T0 = []
    T1 = []
    for ele in topic0samples:
        f = file(ele,'r')
        doc = f.read()
        f.close()
        T0.append(createDocVec(doc, table_idf))
    for ele in topic1samples:
        f = file(ele,'r')
        doc = f.read()
        f.close()
        T1.append(createDocVec(doc, table_idf))
    T0 = [(ele,0) for ele in T0]
    T1 = [(ele,1) for ele in T1]
    tmp = T0 + T1
    random.shuffle(tmp)
    X,Y = [ele[0] for ele in tmp],[ele[1] for ele in tmp] 
    return X,Y

def getTestSet():
    f = file('table_idf.pkl','r')
    table_idf = cPickle.load(f)
    f.close()
    topic0 = ['finance']
    topic1 = ['not_finance']
    topic0samples = []
    topic1samples = []
    for ele in topic0:
        tmp = os.listdir(os.path.join(cf.TEST_ROOT,ele))
        tmp = [os.path.join(cf.TEST_ROOT,ele,path) for path in tmp]
        topic0samples += tmp
    for ele in topic1:
        tmp = os.listdir(os.path.join(cf.TEST_ROOT,ele))
        tmp = [os.path.join(cf.TEST_ROOT,ele,path) for path in tmp]
        topic1samples += tmp
    
    T0 = []
    T1 = []
    for ele in topic0samples:
        f = file(ele,'r')
        doc = f.read()
        f.close()
        T0.append(createDocVec(doc, table_idf))
    for ele in topic1samples:
        f = file(ele,'r')
        doc = f.read()
        f.close()
        T1.append(createDocVec(doc, table_idf))
    return T0+T1,len(T0)*[0]+len(T1)*[1]

def creatModel(n_estimators=100, learning_rate=1.0, max_depth=1, random_state=0):
    return GradientBoostingClassifier(n_estimators=n_estimators, learning_rate=learning_rate, max_depth=max_depth, random_state=random_state)

def train():
    model = creatModel()
    X,Y = getTrainSet()
    test_x,test_y = getTestSet()
    clf = model.fit(X,Y)
    joblib.dump(clf,'../model/gbdt_v1.m',compress=3)
    return clf.score(test_x,test_y)
    
    
if __name__=='__main__':
    print 'Accuracy:%f'%train()
    
