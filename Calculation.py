import pyodbc

conn1 = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};'
                       'SERVER=94.73.150.3;'
                       'Trusted_Connection=no;'
                       'DATABASE=u7307120_zenep;'
                       'UID=u7307120_zenep;'
                       'PWD=EBkd63D2')
cursor = conn1.cursor()

conn2 = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};'
                       'SERVER=94.73.150.3;'
                       'Trusted_Connection=no;'
                       'DATABASE=u7307120_zenep;'
                       'UID=u7307120_zenep;'
                       'PWD=EBkd63D2')
cursor1 = conn2.cursor()

className='UpgradedDataLoadTest'
sql = '''select VARIABLE.CLASS_NAME,METHOD.METHOD_NAME,METHOD.VARIABLE_NAME, VARIABLE.OBJECT_TYPE,IGNORE.TYPE_NAME,count(*) from VARIABLE_INVOCATION VARIABLE Inner JOIN METHOD_INVOCATION METHOD ON METHOD.VARIABLE_NAME=VARIABLE.OBJECT_NAME AND METHOD.CLASS_NAME = VARIABLE.CLASS_NAME left JOIN IGNORE_TYPE_TABLE IGNORE ON IGNORE.TYPE_NAME = VARIABLE.OBJECT_TYPE WHERE   IGNORE.TYPE_NAME is NULL  GROUP BY VARIABLE.CLASS_NAME,METHOD.METHOD_NAME,METHOD.VARIABLE_NAME,VARIABLE.OBJECT_TYPE,IGNORE.TYPE_NAME ORDER BY VARIABLE.CLASS_NAME '''
#param_values = [className]
#result = cursor.execute(sql,param_values),
cursor.execute(sql),
methodname =""
className =""
FEC=[]
FECRow = []
calledCount=0
ownMethodCount=0
tempMethodName=""
tempClassName=""
for i in cursor:

     #print(i[0], i[1], i[2], i[3],i[4],i[5] )
     methodname = i[1]
     className = i[0]
     ownMethod='ownMethod'
     UpgradedDataLoadTest='UpgradedDataLoadTest'

     if (tempMethodName == "" and tempClassName == ""):
         tempMethodName = methodname
         tempClassName = className
         calledCount = calledCount + i[5]
         #print(calledCount)
     elif (methodname == tempMethodName and className == tempClassName):
         calledCount = calledCount + i[5]
         #print("*",calledCount)
     else: #(methodname != tempMethodName or className != tempClassName):
         qry = '''select   count(*)    from METHOD_INVOCATION    where   VARIABLE_NAME =(?)  AND METHOD_NAME = (?) AND CLASS_NAME = (?)  '''
         param_values = [ownMethod, tempMethodName, tempClassName]
         cursor1.execute(qry, param_values)

         for e in cursor1:
             ownMethodCount = e[0]

         fec = calledCount / (ownMethodCount + calledCount)
         FECRow.append(tempClassName)
         FECRow.append(tempMethodName)
         FECRow.append(fec)
         FEC.append(FECRow)
         #print(FECRow, "-", calledCount)
         FECRow = []

         calledCount = 0

         calledCount = calledCount + i[5]
         #print(FECRow, "-", calledCount)





     tempMethodName = methodname
     #print(tempMethodName)
     tempClassName = className
     #print(tempClassName)
for abc in FEC:
    print(abc)