import nltk as nltk
import pyodbc
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC, LinearSVC
#from sklearn import cross_validation
from sklearn.model_selection import KFold, cross_val_score
from sklearn.metrics import recall_score,precision_score,accuracy_score,f1_score


conn1 = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};'
                       'SERVER=94.73.150.3;'
                       'Trusted_Connection=no;'
                       'DATABASE=u7307120_zenep;'
                       'UID=u7307120_zenep;'
                       'PWD=EBkd63D2')
cursor = conn1.cursor()
cursor1 = conn1.cursor()

train = [
    #(dict(cc=1,loc=2,cm=1,om=1), 'notfeaturEnvy'), #Sallamasyon
    (dict(cc=2,loc=4,cm=2,om=1),  'featurEnvy'), #getPropertyArrykey
    (dict(cc=1,loc=13,cm=2,om=2), 'notfeaturEnvy'), #addDomain
    (dict(cc=2,loc=14,cm=3,om=0), 'featurEnvy'), #getversionresourceces
    (dict(cc=4,loc=72,cm=13,om=9), 'notfeaturEnvy'), #getDomain
    (dict(cc=6,loc=28,cm=2,om=0,), 'featurEnvy'), #updateotherprpproperties
    (dict(cc=11,loc=50,cm=5,om=5), 'notfeaturEnvy'), #getDomain
    (dict(cc=5,loc=24,cm=2,om=0), 'featurEnvy'), #getOtherprpproperties
    (dict(cc=7,loc=45,cm=5,om=0), 'notfeaturEnvy'), #getDomain
    (dict(cc=1,loc=13,cm=2,om=2), 'featurEnvy'), #adddomain
    (dict(cc=19,loc=122,cm=7,om=1), 'notfeaturEnvy'), #getDomain
    (dict(cc=7,loc=17,cm=5,om=2),  'featurEnvy'),
    (dict(cc=3,loc=6,cm=0,om=1), 'notfeaturEnvy'), #getDomain
    (dict(cc=1,loc=6,cm=3,om=0), 'featurEnvy'),
    (dict(cc=2, loc=28, cm=5, om=2), 'notfeaturEnvy'),  # getDomain
    (dict(cc=5,loc=10,cm=4,om=0), 'featurEnvy'),
    #(dict(cc=0,loc=0,cm=0,om=0), 'notfeaturEnvy'), #Sallamasyon
   ]

nSplit=5

k_fold = KFold(n_splits=nSplit,shuffle=True)
acrSVM=0
acrDEC=0
acrNAI=0
preSVM=0
recSVM=0
preNAI=0
recNAI=0
preDEC=0
recDEC=0

print("***********************************")
for train_indices, test_indices in k_fold.split(train):
    print('Train: %s | test: %s' % (train_indices, test_indices))

    subTest =[]
    subTrain=[]
    realValues=[]

    for train_index in train_indices:
        subTrain.append(train[train_index])
    for test_index in test_indices:
        subTest.append(train[test_index][0])
        realValues.append(train[test_index][1])
    classifierDecision = nltk.classify.DecisionTreeClassifier.train(subTrain)
    sorted(classifierDecision.labels())

    classifierNaive = nltk.classify.NaiveBayesClassifier.train(subTrain)
    sorted(classifierNaive.labels())

    LinearSVC_classifier = SklearnClassifier(LinearSVC())
    LinearSVC_classifier.train(subTrain)

    a = []
    a = LinearSVC_classifier.classify_many(subTest)

    b = []
    b = classifierDecision.classify_many(subTest)

    c = []
    c = classifierNaive.classify_many(subTest)

    print('Real values', realValues)
    print('SVM:', a)
    print('DEC:', b)
    print('NAI:', c)

    print('Recall of SVM: ', recall_score(realValues,a,pos_label='featurEnvy'))
    print('Precision of SVM: ', precision_score(realValues, a, pos_label='featurEnvy'))
    print('Recall of DEC:', recall_score(realValues, b, pos_label='featurEnvy'))
    print('Precision of DEC:', precision_score(realValues, b, pos_label='featurEnvy'))
    print('Recall of NAI:', recall_score(realValues, c, pos_label='featurEnvy'))
    print('Precision of NAI:', precision_score(realValues, c, pos_label='featurEnvy'))
    acrSVM = acrSVM+accuracy_score(realValues, a)
    acrDEC = acrDEC + accuracy_score(realValues, b)
    acrNAI = acrNAI + accuracy_score(realValues, c)
    preSVM=preSVM+precision_score(realValues, a, pos_label='featurEnvy')
    recSVM=recSVM+ recall_score(realValues,a,pos_label='featurEnvy')
    preDEC = preDEC + precision_score(realValues, b, pos_label='featurEnvy')
    recDEC = recDEC + recall_score(realValues, b, pos_label='featurEnvy')
    preNAI = preNAI + precision_score(realValues, c, pos_label='featurEnvy')
    recNAI = recNAI + recall_score(realValues, c, pos_label='featurEnvy')
    print('Accuracy SVM:', accuracy_score(realValues, a))
    print('Accuracy DEC:', accuracy_score(realValues, b))
    print('Accuracy NAI:', accuracy_score(realValues, c))
    print('')
print('Average accuracy of SVM: ', acrSVM/nSplit)
print('Average precision of SVM: ', preSVM/nSplit)
print('Average recall of SVM: ', recSVM/nSplit)
print('')
print('Average accuracy of DEC: ', acrDEC/nSplit)
print('Average precision of DEC: ', preDEC/nSplit)
print('Average recall of DEC: ', recDEC/nSplit)
print('')
print('Average accuracy of NAI: ', acrNAI/nSplit)
print('Average precision of NAI: ', preNAI/nSplit)
print('Average recall of NAI: ', recNAI/nSplit)

print("***********************************")


'''
qry=\'''SELECT mi.METHOD_NAme,mi.Class_name FROM METHOD_INVOCATION mi
			  LEFT OUTER JOIN VARIABLE_INVOCATION vi ON  mi.VARIABLE_NAME=vi.OBJECT_NAME
			  LEFT OUTER JOIN IGNORE_TYPE_TABLE TY ON TY.TYPE_NAME=vi.OBJECT_TYPE
			  WHERE  TY.TYPE_NAME is null
			  group by mi.METHOD_NAME,mi.Class_name\'''

returnList=cursor.execute(qry)
returnTemp = []
returnList1 = []
for e in cursor:
    returnTemp.append(e)
'''


