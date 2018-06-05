import plyj.parser as plyj
import pyodbc
import zipfile

# global variable
rtrnValArr=[]
rtrnVal_=''
sayac = 0
def Insert_Method_Invocation(class_name, project_name, method_name, variable_name, called_method_name, method_code,path):
    qry = '''INSERT INTO METHOD_INVOCATION
             (CLASS_NAME, PROJECT_NAME,METHOD_NAME,VARIABLE_NAME,CALLED_METHOD_NAME,METHOD_CODE,PATH)
             VALUES(?, ?,?,?,?,?,?)'''

    #print(class_name ,"-",variable_name)

    if(class_name== variable_name):
        variable_name = 'ownMethod'

    param_values = [class_name, project_name, method_name,
                    variable_name,
                    called_method_name, method_code,path]
    cursor.execute(qry, param_values)

    cursor.commit()

def Insert_Variable_Invocation(class_name, project_name,method_name,object_name,object_type,method_code,path):
    qry = '''INSERT INTO VARIABLE_INVOCATION
                                                       (CLASS_NAME, PROJECT_NAME,METHOD_NAME,OBJECT_NAME,OBJECT_TYPE,METHOD_CODE,PATH)
                                                       VALUES(?, ?,?,?,?,?,?)'''

    param_values = [class_name, project_name, method_name,
                    object_name,
                    object_type, method_code,path]
    cursor.execute(qry, param_values)

    cursor.commit()

def Recursive_Find_target(trgt):
    try:

        if hasattr(trgt,'value'):
            rtrnValArr.append(trgt.value)

            return rtrnValArr
        else:
            if (hasattr(trgt,'name')):
                rtrnValArr.append(trgt.name)
                Recursive_Find_target(trgt.target)

    except Exception as e:
        print(e)

def mergeMethodNames(rtrnValArr1,bodyName,default=0):

    if(default==0 and len(rtrnValArr1)>0):
        rtrnValArr1.pop()
    rtrnValArr1 = list(reversed(rtrnValArr1))
    rtrnValArr1.append(bodyName)
    mName = ""
    for val in rtrnValArr1:
        mName = mName + "--->" + val + "()";
    return mName

def returnHandler(body,cName,file_path,pMethodName):
    try:
        rtrnValArr =[]
        oName=''
        if hasattr(body,'target'):
            trgt = body.target
            while hasattr(trgt,'target'):
                if hasattr(trgt,'name'):
                    rtrnValArr.append(trgt.name)
                    trgt= trgt.target

            if hasattr(trgt, 'value'):
                oName=trgt.value
            else:
                oName='ownMethod'

            if hasattr(trgt,'type'):
                rtrnValArr.append(trgt.type.name.value)

            Insert_Method_Invocation(cName, 'baz.java', pMethodName,
                                     oName,
                                     mergeMethodNames(rtrnValArr, body.name, 1), sayac, file_path)

            #print()
        if hasattr(body,'if_true'):
            ifElseHandler(body, cName, file_path, pMethodName)

    except Exception as e:
        print(e)

def variableHandler(body,cName,file_path):
    methodVariables = body.variable_declarators
    for params in methodVariables:
        rtrnValArr = []

        if (params.initializer.target == None):
            rtrnValArr.append(params.initializer.name)

        try:
            trgt = params.initializer.target

            if hasattr(params.initializer, 'expression'):
                trgt = params.initializer.expression.target

            while hasattr(trgt, 'name'):
                if (hasattr(trgt, 'name')):
                    rtrnValArr.append(trgt.name)
                    if hasattr(trgt, 'target'):
                        trgt = trgt.target
                    else:
                        rtrnValArr.append(trgt.name.value)
                        break
            if (hasattr(trgt, 'value')):
                rtrnValArr.append(trgt.value)

        except Exception as e:
            print(e, file_path)
        # Recursive_Find_target(params.initializer.target)
        # print(rtrnValArr)
        if (len(rtrnValArr) == 0):
            rtrnValArr.append('ownMethod')
        objectName = rtrnValArr[-1]

        initializerName = ""

        if hasattr(params.initializer, 'expression'):
            initializerName = params.initializer.expression.name
        if hasattr(params.initializer, 'name'):
            initializerName = params.initializer.name

        DBMethodName = mergeMethodNames(rtrnValArr, initializerName)

        parentMethodName = "-"

        if hasattr(MethodDec, 'name'):
            parentMethodName = MethodDec.name

        Insert_Method_Invocation(cName, 'baz.java', parentMethodName,
                                 objectName,
                                 DBMethodName, sayac, file_path)

        Insert_Variable_Invocation(cName, 'baz.java', parentMethodName,
                                   params.variable.name,
                                   body.type.name.value,
                                   sayac, file_path)

def methodHandler  (body,cName,file_path):
       if hasattr(body, 'name'):
                        rtrnValArr = []
                        try:
                            trgt = body.target

                            while hasattr(trgt, 'name'):
                                if (hasattr(trgt, 'name')):
                                    rtrnValArr.append(trgt.name)
                                    trgt = trgt.target
                            if hasattr(trgt, 'value'):
                                rtrnValArr.append(trgt.value)

                        except Exception as e:
                            print(e, file_path)

                        # Recursive_Find_target(body.target)
                        # print(rtrnValArr)

                        if (len(rtrnValArr) == 0):
                            rtrnValArr.append('ownMethod')

                        objectName = rtrnValArr[-1]

                        DBMethodName = mergeMethodNames(rtrnValArr, body.name)

                        Insert_Method_Invocation(cName, 'baz.java', MethodDec.name,
                                                 objectName,
                                                 DBMethodName, sayac, file_path)


def ifElseHandler(body,cName,file_path,pMethodName):
    statements =[]

    if hasattr(body,'if_true'):
        if hasattr(body.if_true,'statements'):
            statements = body.if_true.statements

    if hasattr(body,'if_false'):
        if hasattr(body.if_false,'statements'):
            statements.extend(body.if_false.statements)
        if hasattr(body.if_false,'if_true'):
            statements.extend(body.if_false.if_true.statements)

    for statement in statements:
        if hasattr(statement,'block'):
            tryBlockHandler(statement,cName,file_path,pMethodName)
        if hasattr(statement,'if_true'):
            ifElseHandler(statement,cName,file_path,pMethodName)
        if hasattr(statement,'result'):
            returnHandler(statement,cName,file_path,pMethodName)
        if hasattr(statement,'variable_declarators'):
            variableHandler(statement,cName,file_path)
        if hasattr(statement,'name'):
            methodHandler(statement,cName,file_path)
    if hasattr(body.if_true,'target'):
        methodHandler(body.if_true, cName, file_path)
    if hasattr(body.if_false, 'target'):
        methodHandler(body.if_false, cName, file_path)
    if hasattr(body.predicate, 'target'):
        methodHandler(body.predicate, cName, file_path)


def tryBlockHandler(body,cName,file_path,pMethodName):
    if hasattr(body,'variable_declarators'):
        methodVariables = body.variable_declarators
        for params in methodVariables:
            rtrnValArr = []

            if (params.initializer.target == None):
                rtrnValArr.append("ownMethod")

            try:
                trgt = params.initializer.target

                while hasattr(trgt, 'name'):
                    if (hasattr(trgt, 'name')):
                        rtrnValArr.append(trgt.name)
                        trgt = trgt.target
                if (hasattr(trgt, 'value')):
                    rtrnValArr.append(trgt.value)

            except Exception as e:
                print(e,file_path)
            # Recursive_Find_target(params.initializer.target)

            if (len(rtrnValArr) == 0):
                rtrnValArr.append('ownMethod')
            objectName = rtrnValArr[-1]
            DBMethodName = mergeMethodNames(rtrnValArr, params.initializer.name)
            parentMethodName = "-"

            if hasattr(MethodDec, 'name'):
                parentMethodName = MethodDec.name

            Insert_Method_Invocation(cName, 'baz.java', parentMethodName,
                                     objectName,
                                     DBMethodName, sayac, file_path)

            Insert_Variable_Invocation(cName, 'baz.java', parentMethodName,
                                       params.variable.name,
                                       body.type.name.value,
                                       sayac, file_path)


            if hasattr(body, 'block'):
                if hasattr(body.block, 'statements'):
                    declarations = body.block.statements
                    for dec in declarations:
                        transactions(dec, cName, file_path)

    if hasattr(body,'name'):
            if hasattr(body, 'name'):
                rtrnValArr = []
                try:
                    trgt = body.target

                    while hasattr(trgt, 'name'):
                        if (hasattr(trgt, 'name')):
                            rtrnValArr.append(trgt.name)
                            trgt = trgt.target
                    if hasattr(trgt, 'value'):
                        rtrnValArr.append(trgt.value)

                except Exception as e:
                    print(e,file_path)

                # Recursive_Find_target(body.target)
                #print(rtrnValArr)

                if (len(rtrnValArr) == 0):
                    rtrnValArr.append('ownMethod')

                objectName = rtrnValArr[-1]

                DBMethodName = mergeMethodNames(rtrnValArr, body.name)

                Insert_Method_Invocation(cName, 'baz.java', MethodDec.name,
                                         objectName,
                                         DBMethodName, sayac, file_path)

    if hasattr(body,'result'):
        returnHandler(body.result,cName,file_path,pMethodName)
    if hasattr (body,'if_true') :
        ifElseHandler(body,cName,file_path,pMethodName)

def transactions(MethodDec,cName,file_path,sayac):

    try:
        if hasattr(MethodDec, 'name'):

            methodParams = MethodDec.parameters

            for params in methodParams:
                objectType = ''

                if hasattr(params.type, 'name'):
                    objectType = params.type.name.value
                else:
                    objectType = params.type

                Insert_Variable_Invocation(cName, 'baz.java', MethodDec.name, params.variable.name,
                                           objectType, sayac, file_path)

            # method invacation
            if hasattr(MethodDec, 'body'):
                methodBody = MethodDec.body
                for body in methodBody:

                    if hasattr(body, 'name'):
                        rtrnValArr = []
                        try:
                            trgt= body.target

                            while hasattr(trgt,'name'):
                                if (hasattr(trgt, 'name')):
                                    rtrnValArr.append(trgt.name)
                                    trgt= trgt.target
                            if hasattr(trgt,'value'):
                                rtrnValArr.append(trgt.value)

                        except Exception as e:
                            print(e, file_path)

                        #Recursive_Find_target(body.target)
                        #print(rtrnValArr)

                        if (len(rtrnValArr) == 0):
                            rtrnValArr.append('ownMethod')

                        objectName = rtrnValArr[-1]

                        DBMethodName = mergeMethodNames(rtrnValArr, body.name)

                        Insert_Method_Invocation(cName, 'baz.java', MethodDec.name,
                                                 objectName,
                                                 DBMethodName, sayac, file_path)


                    else:
                        if hasattr(body, 'variable_declarators'):
                            variableHandler(body,cName,file_path)

                        if hasattr(body,'block'):
                            if hasattr(body.block, 'statements'):
                                declarations = body.block.statements
                                for dec in declarations:
                                    tryBlockHandler(dec,cName,file_path,MethodDec.name)
                                    #transactions(dec,cName,file_path)
                        if hasattr(body,'if_true'):
                            ifElseHandler(body,cName,file_path,MethodDec.name)
                        if hasattr(body,'result'):
                            returnHandler(body.result,cName,file_path,MethodDec.name)

            # constructro declaration
            if hasattr(MethodDec, 'block'):
                constructorName = MethodDec.name

                for block in MethodDec.block:
                    if hasattr(block, 'rhs'):
                        constructorMethodName = block.rhs.type.name.value


        else:
            methodParams = MethodDec.variable_declarators
            for params in methodParams:
                Insert_Variable_Invocation(cName, 'baz.java', '-', params.variable.name,
                                           MethodDec.type.name.value,
                                           sayac, file_path)

    except Exception as e:
        print(e, file_path)

parser = plyj.Parser()

try:
    srczip = zipfile.ZipFile('server-develop.zip', mode='r')
    #onlyfiles = [f for f in listdir('srczip') if isfile(join('srczip', f))]
    onlyfiles=[];
    for file in srczip.filelist:

      if (len(file.filename.split('.'))>1):
        if(file.filename.split('.')[1] == 'java'):
            onlyfiles.append(file.filename)

except Exception as e:
    print('hata', e)

conn1 = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};'
                       'SERVER=94.73.150.3;'
                       'Trusted_Connection=no;'
                       'DATABASE=u7307120_zenep;'
                       'UID=u7307120_zenep;'
                       'PWD=EBkd63D2')
cursor = conn1.cursor()



for file in onlyfiles:

    info = srczip.getinfo(file)
    srcfile = srczip.read(info)
    str = srcfile.decode("utf-8")
    tree = parser.parse_string(str)
    ClassNames = tree.type_declarations

    for className in ClassNames:
        print(' ClassName: ', className.name)

        methodDecs = className.body

        for MethodDec in methodDecs:
            sayac=sayac+1
            if hasattr(MethodDec, 'extends'):
                allClasses =MethodDec.body
                for classs in allClasses:
                   transactions(classs,MethodDec.name,file,sayac)
            else:
                transactions(MethodDec,className.name,file,sayac)

