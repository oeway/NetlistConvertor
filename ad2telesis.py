# -*- coding: cp936 -*-

specialChars =' +-/\.'
DATA = '' #current folder
replaceFile = DATA+'replaceList.txt'
inputFile = DATA+'cjy.NET'
outputFile = DATA + 'netlist_out.tel'

class package:
    footprint = ''
    comment = ''
    designator = ''
class net:
    name = ''
    nodes = []

#read the replacement content
rpFile = open(replaceFile)
rpDict = {}
#generate the replace list
for line in rpFile:
    tmp = line.split('\t')
    rpDict[tmp[0].strip()] = tmp[1].strip()
#replace
packageList = []
netList = []
section = ''
currentNet = net()
f = open(inputFile)
for line in f:
    #print(line)
    if '$' in line :
        section = line.strip().upper()
        if section =='$END':
            if(currentNet.name != ''):
                netList.append(currentNet)
            break;
        else:
            continue
    if section == '$PACKAGES' and '!' in line :
        tmp = line.split('!')
        pkg = package()
        pkg.footprint = tmp[0].strip() #去空格
        if ';' in tmp[1] :
            tmp = tmp[1].split(';')
            pkg.comment = tmp[0].strip()
        tmp = tmp[1].strip()
        if ' ' in tmp :
            pkg.designator = tmp.split(' ') #用空格分隔 拆分成1个list的元素
        else:
            pkg.designator = tmp
        packageList.append(pkg)
    elif section == '$NETS':
        if ';' in line :      #识别到下一行 存储上一行
            if currentNet.name != '' :
                netList.append(currentNet)
            tmp = line.split(';')
            currentNet = net()
            currentNet.name = tmp[0].strip()
            tmp = tmp[1].replace(',','').strip()  #两边去空格
            currentNet.nodes = tmp.split(' ')     
        else:
            tmp = line.replace(',','').strip()
            currentNet.nodes +=  tmp.split(' ')
print('Analysis completed!\npackages:{0} nets:{1}'.format(len(packageList),len(netList)))


outFile = open(outputFile,'w')
outFile.write('(AD to Allegro NetList By OEway)\n')
outFile.write('$PACKAGES\n')
print ('Generating the netlist file for allegro...')
for pkg in packageList:
    footprint = pkg.footprint
    if rpDict.has_key(pkg.footprint):
        footprint = rpDict[pkg.footprint]
    for c in specialChars:
        footprint = footprint.replace(c,'_')
    outFile.write("{0} ! {1} ! '{3}' ; {2}\n".format(footprint,footprint,pkg.designator,pkg.comment))
outFile.write('$NETS\n')
for net in netList:
    name = net.name
    for c in specialChars:
        if c in name:
            name = "'" + name + "'"
            break;
    outFile.write('{0} ; {1}\n'.format(name,' '.join(net.nodes)))
outFile.write('$END\n')
outFile.close()
print('Complete!\nOutput file:{0}'.format(outputFile))
