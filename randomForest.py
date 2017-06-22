# coding=utf-8

import fileinput
import math
import copy
import random
import json
import sys,os

import utils

class randomforest(object):
    def __init__(self,dataset = None, treeNum = 20):
        if dataset ==None:
            raise ('There is no dataset! ')
        else:
            self.dataset = dataset
        self.datanum = len(dataset)
        self.idxnum = len(dataset[0])-1
        self.treeNum = treeNum
        self.RootNode =None
        self.count=0

    def readTree(self,filename):

        f = open(filename,'r')
        self.RootNode = json.load(f,encoding='utf-8')


    def setTreeNumber(self,num):
        self.treeNum = num


    def getRandomForest(self,name = 'random_forest'):
        self.RootNode = {}

        for i in range(self.treeNum):
            self.count += 1
            datasample = self.generateSample()
            subtree = self.selectIndex([],0,self.datanum,datasample)
            self.RootNode[unicode(str(i),'utf-8')] = subtree

            print 'Have generate Tree ' +str(self.count)+' !'


        self.saveTree(name)


    def generateSample(self,num=None):

        if num==None:
            snum = len(self.dataset)
        else:
            snum = num
        datasample =[]

        for i in range(snum):
            idx = random.randint(0,len(self.dataset)-1)
            datasample.append(self.dataset[idx])

        print 'Have generate one Sample for tree '+str(self.count)+' with num: '+ str(snum)

        return datasample


    def saveTree(self,name):

        path = sys.path[0] + '/tree_json/' +name +'.txt'

        f =open(path,'w')
        test=  json.dump(self.RootNode,f)
        f.close()

        print 'Have saved the random forest in :' + path



    def selectIndex(self,forbiddenIndex,startLoc,endLoc,dataset):
        backup_index = [ i for i in range(self.idxnum) if i not in forbiddenIndex]
        newindex = None
        newgeni = 2
        newsplit= None
        subtree= {}

        if len(backup_index) ==1:
            sureclass= self.majorClass([dataset[i][-1] for i in range(startLoc,endLoc)])
            subtree ={u'node': u'leaf',u'class':sureclass}
        else:
            subtree[u'type'] = u'node'
            for i in backup_index:
                splitValue = self.getSortSplitValue(i,dataset,startLoc,endLoc)

                for sv in splitValue:
                    geni = self.calGeniForDataSet(i,sv,dataset,startLoc,endLoc)
                    if geni < newgeni:
                        newindex = i
                        newgeni =geni
                        newsplit = sv

            if newindex ==None or newsplit ==None:
                sureclass = self.majorClass([dataset[i][-1] for i in range(startLoc, endLoc)])
                subtree = {u'node': u'leaf', u'class': sureclass}
            else:
                newend,dataset = self.changeLocation(newindex,newsplit,startLoc,endLoc,dataset)
                forbid = copy.deepcopy(forbiddenIndex)
                forbid.append(newindex)

                if startLoc <newend and newend<endLoc:
                    subtree[u'splitvalue'] = newsplit
                    subtree[u'splitindex'] = newindex
                    tree = self.selectIndex(forbid,startLoc,newend,dataset)
                    subtree[u'<'] = tree
                    self.selectIndex(forbid,newend,endLoc,dataset)
                    subtree[u'>'] = tree
                elif startLoc ==newend or newend ==endLoc:
                    sureclass = self.majorClass([dataset[i][-1] for i in range(startLoc, endLoc)])
                    subtree = {u'node': u'leaf', u'class': sureclass}

        return subtree

    def getSortSplitValue(self,index,dataset,startLoc,endLoc):

        values = [dataset[j][index] for j in range(startLoc,endLoc)]


        values=sorted(list(set(values)))

        splitValue = []
        for i in range(len(values)-1):
            splitValue.append( (values[i]+values[i+1])*0.5)


        return splitValue



    def calGeniForDataSet(self,index, splitValue, dataset,startLoc,endLoc):

        dataclass = [{}, {}]
        datacount = [0, 0]

        for i in range(startLoc,endLoc):
            if dataset[i][index] < splitValue:
                dataclass[0][dataset[i][-1]] = dataclass[0].get(dataset[i][-1], 0) + 1
                datacount[0] += 1
            else:
                dataclass[1][dataset[i][-1]] = dataclass[1].get(dataset[i][-1], 0) + 1
                datacount[1] += 1

        geni = [1.0, 1.0]

        for key, value in dataclass[0].items():
            geni[0] -= (value * 1.0 / datacount[0]) ** 2
        for key, value in dataclass[1].items():
            geni[1] -= (value * 1.0 / datacount[1]) ** 2

        totalgeni = 0.0
        for i in range(2):
            totalgeni += datacount[i] * 1.0 / len(dataset) * geni[i]

        return totalgeni

    def majorClass(self,classList):
        classDict = {}
        for cls in classList:
            classDict[cls] = classDict.get(cls, 0) + 1
        sortClass = sorted(classDict.items(), key=lambda item: item[1])
        return sortClass[-1][0]

    def changeLocation(self,index,splitValue,startLoc,endLoc,dataset):
        idx1 =startLoc
        idx2 = endLoc-1
        tmp =None

        while idx1 <idx2:
            if dataset[idx1][index]<=splitValue:
                idx1+=1
            elif dataset[idx1][index]> splitValue:
                tmp = dataset[idx2]
                dataset[idx2] = dataset[idx1]
                dataset[idx1] =tmp
                idx2-=1

        return idx1,dataset

    def getClass(self,tree,data):

        stree = tree
        while stree[u'type'] ==u'node':
            sv = stree[u'splitvalue']
            if data[stree[u'splitindex']] <= sv:
                stree = stree[u'<']
            else:
                stree = stree[u'>']

        return stree[u'class']

    def getRandomForestClass(self,data):
        sureclass = {}

        if self.RootNode==None:
            raise ('There is no Random Forest! ')
        else:
            for key,value in self.RootNode.items():
                tclass = self.getClass(value,data)
                sureclass[tclass] = sureclass.get(tclass,0)+ 1

        ans = max(sureclass.items(), key=lambda x: x[1])

        return ans[0]



if __name__ == '__main__':
    dataset = utils.importData(sys.path[0]+'/data/wine.txt')

    rf = randomforest(dataset=dataset,treeNum=10)

    rf.getRandomForest(name='test1')
    print rf.RootNode

    rf.saveTree('test1')

    rf.readTree(sys.path[0] + '/tree_json/test1.txt')

    print rf.RootNode
