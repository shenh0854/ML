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

def createVocabList(dataSet):
    vocabSet = set([])
    for document in dataSet:
        vocabSet = vocabSet | set(document)
    return list(vocabSet)

def setOfWords2Vec(vocabList,inputSet):
    returnVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else:
            print 'the word: %s is not in my vocabulary' %word

    return returnVec


def main():   #主程序清单
    listOPosts,listClasses = loadDataSet()
    myvocabList = createVocabList(listOPosts)

    print myvocabList

    print setOfWords2Vec(myvocabList,listOPosts[0])
    print setOfWords2Vec(myvocabList,listOPosts[3])

if __name__=="__main__":
     main()
