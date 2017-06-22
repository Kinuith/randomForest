# coding=utf-8

import fileinput

def calGeni(dataset): # the data

    dataclass = {}

    for dt in dataset:
        dataclass[dt[-1]] = dataclass.get(dt[-1],0) +1

    geni = 1.0

    num  = len(dataset)

    for key ,value in dataclass.items():
        geni -= (value*1.0/num)**2

    return geni

def calGeniForDataSet(index, splitValue,dataset):

    dataclass = [{},{}]
    datacount =[0,0]

    for dt in dataset:
        if dt[index] <splitValue:
            dataclass[0][dt[-1]] = dataclass[0].get(dt[-1], 0) + 1
            datacount[0]+=1
        else:
            dataclass[1][dt[-1]] = dataclass[1].get(dt[-1], 0) + 1
            datacount[1] += 1

    geni = [1.0,1.0]


    for key,value in dataclass[0].items():
        geni[0] -= (value * 1.0 / datacount[0]) ** 2
    for key,value in dataclass[1].items():
        geni[1] -= (value * 1.0 / datacount[1]) ** 2

    totalgeni = 0.0
    for i in range(2):
        totalgeni = datacount[i]*1.0/len(dataset) *geni[i]

    return totalgeni

def majorClass(classList):
    classDict = {}
    for cls in classList:
        classDict[cls] = classDict.get(cls, 0) + 1
    sortClass = sorted(classDict.items(), key=lambda item: item[1])
    return sortClass[-1][0]

def importData(file):

    dataset = []

    for line in fileinput.input([file]):
        ll = map(lambda x:float(x.strip('\r\n ')),line.split(','))
        ll[-1] =int(ll[-1])

        dataset.append(ll)

    return dataset





