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
    returnVec = [0]*len(vocabList)
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
    p0Num = zeros(numWords)
    p1Num = zeros(numWords)
    p0Denom = 0.0
    p1Denom = 0.0
    for i in range(numTrainDocs):
        if trainCatogary[i] == 1:        #p1为侮辱性词语，p0为正常词语，分别统计
            p1Num += trainMatrix[i]
            p1Denom += sum(trainMatrix[i])
        else:
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])
    p1Vect = p1Num/p1Denom
    p0Vect = p0Num/p0Denom

    return p0Vect,p1Vect,pAbusive


def main():   #主程序清单
    listOPosts,listClasses = loadDataSet()
    myvocabList = createVocabList(listOPosts)

    print myvocabList

    print setOfWords2Vec(myvocabList,listOPosts[0])
    print setOfWords2Vec(myvocabList,listOPosts[3])



if __name__=="__main__":
     main()
