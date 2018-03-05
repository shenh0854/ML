# -*- coding: utf-8 -*-
import sys,os
from numpy import *
from os import listdir
import matplotlib
#matplotlib是python2d数据处理绘图的常用工具
import matplotlib.pyplot as plt
import operator


def loadDataSet():
    postingList = [['my','dog','has','flea','problems','help','please'],
                   ['maybe','not','take','him','to','dog','park','stupid'],
                   ['my','dalmation','is','so','cute','I','love','him'],
                   ['stop','posting','stupid','worthless','garbage'],
                   ['mr','licks','ate','my','steak','how','to','stop','him'],
                   ['quit','buying','worthless','dog','food','stupid']]
    classVec = [0,1,0,1,0,1]
    return postingList,classVec

def createVocabList(dataSet):           #创建字典，字典内为所有出现在文档中且不重复的字
    vocabSet = set([])
    for document in dataSet:
        vocabSet = vocabSet | set(document)
    return list(vocabSet)

def setOfWords2Vec(vocabList,inputSet):        #对每个文档，统计其中是否出现过字典内的词，有则标注1，没有标注0
                                               #形成一个长度等于字典词数的向量，根据这一向量对文档进行分类
    returnVec = [0]*len(vocabList)   #生成list的一种方式，个数乘以长度
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else:
            print 'the word: %s is not in my vocabulary' %word
    return returnVec

def trainNB0(trainMatrix,trainCatogary):  #输入为文档矩阵（向量）和文档类别标签
    numTrainDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])
    pAbusive = sum(trainCatogary)/float(numTrainDocs)
    # p0Num = zeros(numWords)
    # p1Num = zeros(numWords)
    # p0Denom = 0.0
    # p1Denom = 0.0
    p0Num = ones(numWords)       #为计算多个概率的乘积最后得到该文档类别的概率，避免因某一概率为0最后出现整体为0而做出的调整
    p1Num = ones(numWords)
    p0Denom = 2.0
    p1Denom = 2.0
    for i in range(numTrainDocs):
        if trainCatogary[i] == 1:        #p1为侮辱性词语，p0为正常词语，分别统计
            p1Num += trainMatrix[i]
            p1Denom += sum(trainMatrix[i])
        else:
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])
    # p1Vect = p1Num/p1Denom               #计算得到所占比例
    # p0Vect = p0Num/p0Denom

    p1Vect = log(p1Num/p1Denom)
    p0Vect = log(p0Num/p0Denom)            #避免概率相乘，乘积过小而产生的下溢出

    return p0Vect,p1Vect,pAbusive


def testingNB():                           #封装所有操作
    listOPosts,listClasses = loadDataSet()
    myVocabList = createVocabList(listOPosts)
    trainMat = []
    for postinDoc in listOPosts:
        trainMat.append(setOfWords2Vec(myVocabList, postinDoc))
    p0V, p1V, pAb = trainNB0(array(trainMat), array(listClasses))
    testEntry = ['love', 'my', 'dalmation']
    thisDoc = array(setOfWords2Vec(myVocabList, testEntry))
    print testEntry, 'classified as: ', classifyNB(thisDoc, p0V, p1V, pAb)
    testEntry = ['stupid', 'garbage']
    thisDoc = array(setOfWords2Vec(myVocabList, testEntry))
    print testEntry, 'classified as: ', classifyNB(thisDoc, p0V, p1V, pAb)


def classifyNB(vec2Classify,p0Vec,p1Vec,pClass1):
    p1 = sum(vec2Classify*p1Vec)+log(pClass1)
    p0 = sum(vec2Classify*p0Vec)+log(1.0 - pClass1)

    if p1>p0:
        return 1
    else:
        return 0

def bagOfWord2VecMN(vocabList,inputSet):
    returnVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] += 1
    return returnVec

def textParse(bigString):
    import re
    listOfTokens = re.split(r'W*',bigString)
    return [tok.lower()for tok in listOfTokens if len(tok)>2]           #剔除分词结果中长度小于2的单词

def spamTest():
    docList = []
    classList = []
    fullText = []
    for i in range(1,26):
        wordList = textParse(open('email/spam/%d.txt'%i).read())
        docList.append(wordList)
        fullText.append(wordList)
        classList.append(1)
        wordList = textParse(open('email/ham/%d.txt'%i).read())
        docList.append(wordList)
        fullText.append(wordList)
        classList.append(0)

    vocabList = createVocabList(docList)
    trainingSet = range(50)
    testSet = []

    for i in range(10):
        randIndex = int(random.uniform(0,len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])

    trainMat = []
    trainClasses = []
    for docIndex in trainingSet:
        trainMat.append(setOfWords2Vec(vocabList,docList[docIndex]))
        trainClasses.append(classList[docIndex])

    p0V,p1V,pSpam = trainNB0(array(trainMat),array(trainClasses))
    errorCount = 0
    for docIndex in testSet:
        wordVector = setOfWords2Vec(vocabList,docList[docIndex])
        if classifyNB(array(wordVector),p0V,p1V,pSpam)!=classList[docIndex]:
            errorCount += 1

    print 'the error rate is',float(errorCount/len(testSet))

def main():   #主程序清单
    # listOPosts,listClasses = loadDataSet()
    # myvocabList = createVocabList(listOPosts)
    #
    # # print myvocabList
    #
    # # print setOfWords2Vec(myvocabList,listOPosts[0])
    # # print setOfWords2Vec(myvocabList,listOPosts[3])
    #
    # trainMat = []
    # for postinDoc in listOPosts:
    #     trainMat.append(setOfWords2Vec(myvocabList,postinDoc))
    #
    # p0V,p1V,pab = trainNB0(trainMat,listClasses)
    #
    # print p0V,p1V,pab

    spamTest()


if __name__=="__main__":
     main()
