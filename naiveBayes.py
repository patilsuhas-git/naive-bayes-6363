import numpy as np
import pandas as pd
import csv
import math
import random as rn

def readCSV( filename,dataset ):
    lines = csv.reader(open(filename, "rb"))
    dataset = list(lines)
    for i in range(len(dataset)):
        try:
            dataset[i] = [float(x) for x in dataset[i]]
        except:
            dataset[i] = [x for x in dataset[i]]
    return dataset

def splitDataSet( dataset, splitRatio ):
    countRow = 0
    trainSet = []
    testSet = []
    rn.shuffle(dataset)
    halfWay = len(dataset)/2
    for i in range(len(dataset)):
        if( countRow >= halfWay) :
            trainSet.append(dataset[i])
        else :
            testSet.append(dataset[i])
        countRow += 1
    return [trainSet, testSet]

def splitTrainingDatabyClass(dataset) :
    dividedSet = {}
    for i in range(len(dataset)):
        vector = dataset[i]
        if (vector[-1] not in dividedSet):
            dividedSet[vector[-1]] = []
        dividedSet[vector[-1]].append(vector)
    return dividedSet

def probabilityClass( rowTrainPSet, rowTrainESet, rowTrainSet ) :
    return [ rowTrainPSet/rowTrainSet, rowTrainESet/rowTrainSet ]

def uniqueDictList ( trainSet ) :
    # print trainSet
    columnUniqueValueDict = []
    columnCount = 0
    for row in trainSet:
        for columnCountLoop in range(len(row)):
            columnCount = columnCountLoop
        break

    for i in range(columnCount+1) :
        tempDict = {}
        columnUniqueValueDict.append(tempDict)

    # print len(columnUniqueValueDict)

    for row in trainSet:
        print row
        for columnIndex in range(len(row)):
            # print columnUniqueValueDict
            # print row[columnIndex]
            # print row
            # print row[columnIndex], columnUniqueValueDict[columnIndex]
            if row[columnIndex] in columnUniqueValueDict[columnIndex]:
                # print 'check clas'
                columnUniqueValueDict[columnIndex][row[columnIndex]] = columnUniqueValueDict[columnIndex][row[columnIndex]] + 1
            else :
                columnUniqueValueDict[columnIndex][row[columnIndex]] = 1

    return columnUniqueValueDict

def main( filename, split ):
    filename = filename
    dataset = []
    dataset = readCSV( filename, dataset=[] )
    trainingDataSet = []
    testDataSet = []

    trainingDataSet, testDataSet = splitDataSet(dataset, split)
    dividedSet = {}
    dividedSet = splitTrainingDatabyClass(trainingDataSet)

    trainPoisonousList = []
    trainEdibleList = []

    for key, value in dividedSet.iteritems():
        if (key == 'p'):
            trainPoisonousList.extend( dividedSet[key] )
        else :
            trainEdibleList.extend( dividedSet[key] )
    probability_poisonous, probability_edible = probabilityClass( float(len(trainPoisonousList)), float(len(trainEdibleList)), float(len(trainingDataSet)) )


    columnUniqueValueDictPoisonous = uniqueDictList(trainPoisonousList)
    columnUniqueValueDictEdible = uniqueDictList(trainEdibleList)

    print '********************edible*********************'
    for i in range(len(columnUniqueValueDictEdible)):
        # print columnUniqueValueDictEdible[i]
        for k in columnUniqueValueDictEdible[i]:
            # print columnUniqueValueDictEdible[i][k]/len(trainEdibleList)
            columnUniqueValueDictEdible[i][k] = float(columnUniqueValueDictEdible[i][k])/float(len(trainEdibleList))

    print columnUniqueValueDictEdible

    print '********************Poisonous*********************'
    for i in range(len(columnUniqueValueDictPoisonous)):
        # print columnUniqueValueDictPoisonous[i]
        for k in columnUniqueValueDictPoisonous[i]:
            # print columnUniqueValueDictEdible[i][k]/len(trainEdibleList)
            columnUniqueValueDictPoisonous[i][k] = float(columnUniqueValueDictPoisonous[i][k])/float(len(trainPoisonousList))

    print columnUniqueValueDictPoisonous

    classifiedProbability = {}

    rowCount = 0
    for row in testDataSet:
        poisonousProbability = 1
        edibleProbability = 1
        for column in range(len(row)-1):
            if row[column] in columnUniqueValueDictPoisonous[column]:
                poisonousProbability = float(poisonousProbability) * float(columnUniqueValueDictPoisonous[column][row[column]])
                # print 'poisonous==>> '+str(float(poisonousProbability))
            if row[column] in columnUniqueValueDictEdible[column]:
                edibleProbability *= columnUniqueValueDictEdible[column][row[column]]
                # print 'edible====>>'+str(float(edibleProbability))

        if poisonousProbability > edibleProbability:
            classifiedProbability[rowCount] = 'p'
        else :
            classifiedProbability[rowCount] = 'e'
        rowCount += 1

    # print classifiedProbability

    correctCount = 0
    for row in range(len(testDataSet)):
        if row in classifiedProbability:
            if str(testDataSet[row][-1]) == str(classifiedProbability[row]):
                correctCount += 1
            print 'Actual Class = ' + str(testDataSet[row][-1]) + ' Predicted class = '+ str(classifiedProbability[row])

    accuracy = (float(correctCount)/float(len(testDataSet))) * 100.0;
    print accuracy

main(filename='data/mushroom.csv', split=.50 )
