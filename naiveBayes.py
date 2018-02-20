import numpy as np
import pandas as pd
import csv
import math
import random as rn

def readCSV( filename,dataset ):
    lines = csv.reader(open(filename, "rb"))
    dataset = list(lines)

    cleandataset = []
    for row in dataset:
        isClean = True
        for column in range(len(row)):
            if row[column] == '?':
                isClean = False
        if isClean :
            cleandataset.append(row)

    for i in range(len(cleandataset)):
        try:
            cleandataset[i] = [float(x) for x in cleandataset[i]]
        except:
            cleandataset[i] = [x for x in cleandataset[i]]
    return cleandataset

def splitDataSet( dataset, splitRatio ):
    countRow = 0
    trainSet = []
    testSet = []
    rn.shuffle(dataset)
    # halfWay = len(dataset)/2
    ratioValue = len(dataset) * splitRatio
    rangeValue = len(dataset) - ratioValue

    for i in range(len(dataset)):
        if( countRow < rangeValue) :
            testSet.append(dataset[i])
        else :
            trainSet.append(dataset[i])
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
    columnUniqueValueDict = []
    columnCount = 0
    for row in trainSet:
        for columnCountLoop in range(len(row)):
            columnCount = columnCountLoop
        break

    for i in range(columnCount+1) :
        tempDict = {}
        columnUniqueValueDict.append(tempDict)

    for row in trainSet:
        for columnIndex in range(len(row)):
            if row[columnIndex] in columnUniqueValueDict[columnIndex]:
                columnUniqueValueDict[columnIndex][row[columnIndex]] = columnUniqueValueDict[columnIndex][row[columnIndex]] + 1
            else :
                columnUniqueValueDict[columnIndex][row[columnIndex]] = 1

    return columnUniqueValueDict

def probabilityAttributeGivenClass(columnUniqueValueDict, trainSet):
    for i in range(len(columnUniqueValueDict)):
        for k in columnUniqueValueDict[i]:
            columnUniqueValueDict[i][k] = float(columnUniqueValueDict[i][k])/float(len(trainSet))

    return columnUniqueValueDict

def getClass( columnUniqueValueDictPoisonous, columnUniqueValueDictEdible, testDataSet, trainEdibleList, trainPoisonousList, probability_poisonous, probability_edible ):
    rowCount = 0
    classifiedProbability = {}
    for row in testDataSet:
        poisonousProbability = 1
        edibleProbability = 1
        for column in range(len(row)-1):
            if row[column] in columnUniqueValueDictPoisonous[column]:
                poisonousProbability = float(poisonousProbability) * float(columnUniqueValueDictPoisonous[column][row[column]])
            else :
                poisonousProbability = float(poisonousProbability) * float(1/len(trainPoisonousList))
            if row[column] in columnUniqueValueDictEdible[column]:
                edibleProbability *= float(edibleProbability) * float(columnUniqueValueDictEdible[column][row[column]])
            else :
                edibleProbability = float(edibleProbability) * float(1/len(trainEdibleList))

        poisonousProbability = poisonousProbability * probability_poisonous
        edibleProbability = edibleProbability * probability_edible
        if poisonousProbability > edibleProbability:
            classifiedProbability[rowCount] = 'p'
        else :
            classifiedProbability[rowCount] = 'e'
        rowCount += 1

    return classifiedProbability

def computeAccuracy(classifiedProbability, testDataSet):
    correctCount = 0
    correctPoisnousCount = 0
    incorrectPoisnousCount = 0
    correctEdibleCount = 0
    incorrectEdibleCount = 0
    countp = 0
    counte = 0

    for row in range(len(testDataSet)):
        if row in classifiedProbability:
            if str(testDataSet[row][-1]) == 'p' :
                countp += 1
                if str(testDataSet[row][-1]) == str(classifiedProbability[row]):
                    correctCount += 1
                    correctPoisnousCount +=1
                else:
                    incorrectPoisnousCount += 1
            else:
                counte += 1
                if str(testDataSet[row][-1]) == str(classifiedProbability[row]):
                    correctCount += 1
                    correctEdibleCount +=1
                else:
                    incorrectEdibleCount += 1

    accuracy = (float(correctCount)/float(len(testDataSet))) * 100.0
    print '***************************************************'
    print 'Accuracy = '+ str(accuracy)
    return[accuracy, correctEdibleCount, correctPoisnousCount, incorrectEdibleCount, incorrectPoisnousCount]

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

    columnUniqueValueDictEdible  = probabilityAttributeGivenClass(columnUniqueValueDictEdible, trainEdibleList)
    columnUniqueValueDictPoisonous = probabilityAttributeGivenClass(columnUniqueValueDictPoisonous, trainPoisonousList)

    classifiedProbability = {}
    classifiedProbability = getClass( columnUniqueValueDictPoisonous, columnUniqueValueDictEdible, testDataSet, trainEdibleList, trainPoisonousList, probability_poisonous, probability_edible )


    accuracy, correctEdibleCount, correctPoisnousCount, incorrectEdibleCount, incorrectPoisnousCount = computeAccuracy( classifiedProbability, testDataSet )

    confusion_matrix = [['E/P', 'E', 'P'],['E', str(correctEdibleCount), str(incorrectEdibleCount)], ['P', str(incorrectPoisnousCount), str(correctPoisnousCount)]]
    print '***************************************************'
    print 'Confusion Matrix : '
    for row in confusion_matrix:
        print row
    print '***************************************************'


main( filename='data/mushroom.csv', split=.71 )
