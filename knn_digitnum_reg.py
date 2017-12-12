# -*- coding: utf-8 -*-
import sys,os
from numpy import *
from os import listdir
from knn_demo import classify0
import matplotlib
#matplotlib是python2d数据处理绘图的常用工具
import matplotlib.pyplot as plt
import operator

def img2vector(filename):
    returnVect = zeros((1,1024))
    fr = open(filename)
    for i in range(32):
        lineStr = fr.readline()
        for j in range(32):
            returnVect[0,32*i+j] = int(lineStr[j])
    return returnVect

def handwrittingClassTest():
    hwlabels = []
    trainingFileList = listdir('trainingDigits')
    m = len(trainingFileList)
    trainingMat = zeros((m,1024))
    for i in range(m):
        fileNameStr = trainingFileList[i]
        fileStr = fileNameStr.split('.')[0]
        classNumStr = int(fileStr.split('_')[0])
        hwlabels.append(classNumStr)
        trainingMat[i,:] = img2vector('trainingDigits/%s' % fileNameStr)
    testfilelist = listdir('testDigits')
    errorCount = 0.0
    mTest = len(testfilelist)
    for i in range(mTest):
        fileNameStr = testfilelist[i]
        fileStr = fileNameStr.split('.')[0]
        classNumStr = int(fileStr.split('_')[0])
        vectorUnderTest = img2vector('testDigits/%s' % fileNameStr)
        classifierResult = classify0(vectorUnderTest,trainingMat,hwlabels,3)  #直接使用knn分类算法计算1024维向量之间的距离
        print "the classifier came back with:%d, the real answer is:%d" % (classifierResult,classNumStr)
        if (classifierResult!=classNumStr):errorCount+=1.0
    print "\nthe total number of errors is: %d" % errorCount
    print "\nthe total error rate is: %f" % (errorCount/float(mTest))


def main():   #主程序清单
    handwrittingClassTest()

if __name__=="__main__":
     main()
