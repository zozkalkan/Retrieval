import zipfile
import lizard

srczip = zipfile.ZipFile('mergeZip.zip', mode='r')
# onlyfiles = [f for f in listdir('srczip') if isfile(join('srczip', f))]
onlyfiles = [];
for file in srczip.filelist:

    if (len(file.filename.split('.')) > 1):
        if (file.filename.split('.')[1] == 'java'):
            onlyfiles.append(file.filename)

for file in onlyfiles:
    info = srczip.getinfo(file)
    srcfile = srczip.read(info)
    str = srcfile.decode("utf-8")
    i = lizard.analyze_file.analyze_source_code(file,str)

    if hasattr(i,'function_list'):
        for function in i.function_list:
            print('File:',file,'Method name:',function.name,'CC:',function.cyclomatic_complexity,)

