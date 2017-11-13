import sys,os
from numpy import *
import matplotlib
#matplotlib是python2d数据处理绘图的常用工具
import matplotlib.pyplot as plt
import operator

def createDataSet():
    group = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels = ['A','A','B','B']
    return group,labels

def classify0(inx, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]
    diffMat = tile(inx, (dataSetSize,1))-dataSet
    sqDiffMat = diffMat**2
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances**0.5
    sortedDistIndicies = distances.argsort()
    classCount = {}
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel,0)+1
    sortedClassCount = sorted(classCount.iteritems(),
     key = operator.itemgetter(1),reverse=True)
    return sortedClassCount[0][0]

def file2matrix(filename):   #文件读入
    fr = open(filename)
    arrayOLines = fr.readlines()
    numberOfLines = len(arrayOLines)
    returnMat = zeros((numberOfLines,3))
    classLabelVector = []
    index = 0
    for line in arrayOLines:
        line = line.strip()
        listFormLine = line.split('\t')
        returnMat[index,:] = listFormLine[0:3]
        classLabelVector.append(int(listFormLine[-1]))
        index += 1
    return returnMat,classLabelVector

def autoNorm(dataSet):
    #归一化特征值，用于加权平衡变量
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    normDataSet = zeros(shape(dataSet))
    m = dataSet.shape[0]
    normDataSet = dataSet - tile(minVals,(m,1))
    normDataSet = normDataSet/tile(ranges,(m,1))
    return normDataSet,ranges,minVals


def main():   #主程序清单
    datingDataMat,datingLabels = file2matrix('datingTestSet2.txt')
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(datingDataMat[:,1],datingDataMat[:,2])
    plt.show()


if __name__=="__main__":
     main()

