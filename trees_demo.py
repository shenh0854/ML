# -*- coding: utf-8 -*-
import sys,os
import operator
import treePlotter_demo
from math import log

def calcShannonEnt(dataSet):  #信息熵的计算
    numEntries = len(dataSet)
    labelCounts = {}
    for featVec in dataSet:
        currentLabel = featVec[-1]
        if currentLabel not in labelCounts.keys():labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key])/numEntries
        shannonEnt -= prob * log(prob,2)
    return shannonEnt

def splitDataSet(dataSet,axis,value):  #按照特定的特征划分数据集  axis为特征编号，value为特征实际值
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet

def chooseBestFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0])-1
    baseEntropy = calcShannonEnt(dataSet)
    bestInfoGain = 0.0
    bestFeature = -1
    for i in range(numFeatures):
        featList = [example[i] for example in dataSet]    #此行代码是列表推到式，是构建新列表的一种映射的方式
        uniqueVals = set(featList)  #set函数构造唯一元素的无序集合
        newEnropy = 0.0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet,i,value)   #遍历所有特征值并按照特征值划分数据集，比较划分后的信息熵找到最佳划分的特征值
            prob = len(subDataSet)/float(len(dataSet))
            newEnropy += prob * calcShannonEnt(subDataSet)
        infoGain = baseEntropy - newEnropy
        if infoGain>bestInfoGain:
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature

def majorityCount(classList):       # 当叶子节点无法继续划分且内部类别不唯一时进行投票表决选出叶子节点的分类类别
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys():classCount[vote] = 0
        classCount += 1
    sortedClassCount = sorted(classCount.iteritems(),key=operator.itemgetter(1),reverse=True)
    return sortedClassCount[0][0]

def createTree(dataSet,labels):  #利用递归生成决策树
    classList = [example[-1] for example in dataSet]
    if classList.count(classList[0]) == len(classList):   #类别完全相同时停止继续划分
        return classList[0]
    if len(dataSet[0]) == 1:              #遍历完所有特征值，但是此时决策树还没生成完成，就使用majorityCount函数投票选出类别生成叶子节点
        return majorityCount(classList)
    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel:{}}
    del(labels[bestFeat])
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels[:]    #复制类标签并将其储存在新的列表中
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet,bestFeat,value),subLabels)

    return myTree

def createDataSet():
    dataSet = [1,1,'yes'],[1,1,'yes'],[1,0,'no'],[0,1,'no'],[0,1,'no']
    labels = ['no surfacing','flippers']
    return dataSet,labels


def classify(inputTree,featLabels,testVec):
    firstStr = inputTree.keys()[0]
    secondDict = inputTree[firstStr]
    featIndex = featLabels.index(firstStr)
    for key in secondDict.keys():
        if testVec[featIndex] == key:
            if type(secondDict[key]).__name__=='dict':
                classLabel = classify(secondDict[key],featLabels,testVec)
            else:
                classLabel = secondDict[key]

    return classLabel



def main():   #主程序清单
    myDat,labels = createDataSet()
    print calcShannonEnt(myDat)
    print chooseBestFeatureToSplit(myDat)
    #
    myTree = treePlotter_demo.retrieveTree(0)

    print myTree
    classify(myTree,labels,[1,0])
    classify(myTree,labels,[1,1])

    #分类隐形眼镜
    fr = open('lenses.txt')
    lenses = [inst.strip().split('\t') for inst in fr.readlines()]
    lensesLabels = ['age','prescipt','astigmatic','tearRate']
    lensesTree = createTree(lenses,lensesLabels)
    print lensesTree
    treePlotter_demo.createPlot(lensesTree)
if __name__=="__main__":
     main()

