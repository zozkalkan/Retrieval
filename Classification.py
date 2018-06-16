import nltk as nltk
import pyodbc
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.svm import SVC, LinearSVC
from sklearn import cross_validation
from sklearn.model_selection import KFold

conn1 = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};'
                       'SERVER=94.73.150.3;'
                       'Trusted_Connection=no;'
                       'DATABASE=u7307120_zenep;'
                       'UID=u7307120_zenep;'
                       'PWD=EBkd63D2')
cursor = conn1.cursor()
cursor1 = conn1.cursor()

train = [
    (dict(cc=2,loc=4,cm=2,om=1),  'featurEnvy'), #getPropertyArrykey
    (dict(cc=2,loc=14,cm=3,om=0), 'featurEnvy'), #getversionresourceces
    (dict(cc=6,loc=28,cm=2,om=0,), 'featurEnvy'), #updateotherprpproperties
    (dict(cc=5,loc=24,cm=2,om=0), 'featurEnvy'), #getOtherprpproperties
    (dict(cc=1,loc=13,cm=2,om=2), 'featurEnvy'), #adddomain
    (dict(cc=7,loc=17,cm=5,om=2),  'featurEnvy'),
   # (dict(cc=1,loc=6,cm=3,om=0), 'featurEnvy'),
   # (dict(cc=5,loc=10,cm=4,om=0), 'featurEnvy'),
    (dict(cc=1,loc=13,cm=2,om=2), 'notfeaturEnvy'), #addDomain
    #(dict(cc=4,loc=72,cm=13,om=9), 'notfeaturEnvy'), #getDomain
    (dict(cc=11,loc=50,cm=5,om=5), 'notfeaturEnvy'), #getDomain
    (dict(cc=7,loc=45,cm=5,om=0), 'notfeaturEnvy'), #getDomain
   #(dict(cc=19,loc=122,cm=7,om=1), 'notfeaturEnvy'), #getDomain
   # (dict(cc=3,loc=6,cm=0,om=1), 'notfeaturEnvy'), #getDomain
    (dict(cc=2,loc=28,cm=5,om=2), 'notfeaturEnvy'), #getDomain
    #(dict(cc=1,loc=2,cm=1,om=1), 'notfeaturEnvy'), #Sallamasyon
    #(dict(cc=0,loc=0,cm=0,om=0), 'notfeaturEnvy'), #Sallamasyon
   ]


qry='''SELECT mi.METHOD_NAme,mi.Class_name FROM METHOD_INVOCATION mi 
			  LEFT OUTER JOIN VARIABLE_INVOCATION vi ON  mi.VARIABLE_NAME=vi.OBJECT_NAME
			  LEFT OUTER JOIN IGNORE_TYPE_TABLE TY ON TY.TYPE_NAME=vi.OBJECT_TYPE
			  WHERE  TY.TYPE_NAME is null
			  group by mi.METHOD_NAME,mi.Class_name'''

returnList=cursor.execute(qry)
returnTemp = []
returnList1 = []
for e in cursor:
    returnTemp.append(e)
test = [
(dict(cc=3,loc=6,cm=0,om=1)),
(dict(cc=1,loc=6,cm=3,om=0)),
(dict(cc=5,loc=10,cm=4,om=0)),
(dict(cc=19,loc=122,cm=7,om=1))


]

classifierDecision = nltk.classify.DecisionTreeClassifier.train(train)
sorted(classifierDecision.labels())

classifierNaive = nltk.classify.NaiveBayesClassifier.train(train)
sorted(classifierNaive.labels())

LinearSVC_classifier = SklearnClassifier(LinearSVC())
LinearSVC_classifier.train(train)


a=[]
a=LinearSVC_classifier.classify_many(test)

b=[]
b=classifierDecision.classify_many(test)

c=[]
c=classifierNaive.classify_many(test)
#count=0
#countfe=0;
#countnfe=0;
#value = 'featurEnvy'
'''for pdist in classifier.prob_classify_many(test):
    if (pdist.prob('featurEnvy') > pdist.prob('notfeaturEnvy')):
        countfe = countfe + 1
        value = 'featurEnvy'
    else:
        countnfe = countnfe + 1
        value = 'notFeaturEnvy'
    print('fe: ',pdist.prob('featurEnvy'),' nfe:', pdist.prob('notfeaturEnvy'),value)
print(countfe, countnfe)'''
print('SVM:' ,a)
print('DEC:' ,b)
print('NAI:' ,c)
#print("LinearSVC_classifier accuracy percent:", (nltk.classify.accuracy(LinearSVC_classifier, test))*100)
y = (['FeaturEnvy','notFeaturEnvy'])

#import nltk
#from sklearn import cross_validation
#training_set = nltk.classify.apply_features(y, train)
cv = cross_validation.KFold(len(train), n_folds=10, indices=True, shuffle=False, random_state=None, k=None)

for traincv, testcv in cv:
    print(train[traincv[0]:traincv[len(traincv)-1]])
    #classifier = nltk.NaiveBayesClassifier.train(training_set[traincv[0]:traincv[len(traincv)-1]])
    #print 'accuracy:', nltk.classify.util.accuracy(classifier, training_set[testcv[0]:testcv[len(testcv)-1]])

#X = np.array([[1, 2], [3, 4], [1, 2], [3, 4]])
#y = np.array(['featureEnvy','featureEnvy'])
kf = KFold(n_splits=2)
#kf.get_n_splits(X)
kf = KFold(n_splits=2)
KFold(n_splits=2, random_state=None, shuffle=False)
for train_index, test_index in kf.split(train):
    print("TRAIN:", train_index, "TEST:", test_index)
    X_train, X_test = train[train_index], train[test_index]
    y_train, y_test = y[train_index], y[test_index]



