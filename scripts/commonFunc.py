#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
File name: commonFunc.py
Author: CrazyHsu @ crazyhsu9527@gmail.com 
Created on: 2018-10-30 15:11:45
Last modified: 2018-10-30 15:11:46
'''
import re, os

#===============Classes==================

class BinLine(object):
    def __init__(self, binNum, chrId, start, end, length, **args):
        self.binNum = binNum
        self.chrId = chrId
        self.start = start
        self.end = end
        self.length = length

    def __str__(self):
        return "bin:{} chr{}:{}-{} length:{}".format(self.binNum, self.chrId, self.start, self.end, self.length)

    __repr__ = __str__

class Bin(object):
    def __init__(self):
        self.allChr = {}
        self.allBins = {}
        self.allChrLen = {}

    def updateChr(self, chrId, binLineObj):
        binNum = binLineObj.binNum
        if chrId not in self.allChr:
            self.allChr[chrId] = {binNum: binLineObj}
        else:
            self.allChr[chrId].update({binNum: binLineObj})

    def updateBin(self, binLineObj):
        binNum = binLineObj.binNum
        self.allBins[binNum] = binLineObj

    def updateChrLen(self):
        for chrId in self.allChr:
            length = 0
            for binNum in self.allChr[chrId]:
                length += self.allChr[chrId][binNum].length
            self.allChrLen[chrId] = length

class RegionGroup(object):
    def __init__(self, binList, binInfo, name):
        self.binList = binList
        self.binInfo = binInfo
        self.name = name
        self.regionStart = min(binList)
        self.regionEnd = max(binList)

    def __len__(self):
        myLen = 0
        for binNum in self.binList:
            myLen += self.binInfo.binInfo.allBins[binNum].length
        return myLen

    def __str__(self):
        return "Region bins from {}-{}, length {}".format(self.regionStart, self.regionEnd, self.__len__())

    # __repr__ = __str__

class ParseBin(object):
    def __init__(self, binInfoFile, **args):
        self.binInfo = self.parseBin(binInfoFile)

    def parseBin(self, binInfoFile):
        binInfo = Bin()
        with open(binInfoFile) as f:
            for line in f.readlines()[1:]:
                binNum, chrId, start, end, length = re.split("\t", line.strip("\n"))
                binLineObj = BinLine(int(binNum), chrId, float(start), float(end), float(length))
                binInfo.updateChr(chrId, binLineObj)
                binInfo.updateBin(binLineObj)
        binInfo.updateChrLen()
        return binInfo

    def __str__(self):
        return "{} chromosomes, {} bins".format(len(self.binInfo.allChr.keys()), len(self.binInfo.allBins.keys()))

#===============Methods==================
def getAttribute(key, default, **args):
    return default if key not in args else args[key]

def getListFromFile(myFile):
    with open(myFile) as f:
        myList = []
        for line in f:
            if line.startswith("#"): continue
            myList.append(line.strip("\n"))
        return myList

def getIndexByOverlap(specStart, specEnd, binInfo, chrId):
    objs = binInfo.binInfo.allChr[chrId]
    objsKey = objs.keys()
    objsKey.sort(key=int)
    tmpIndex = []
    for i in objsKey:
        if objs[i].end <= specStart: continue
        if objs[i].start >= specEnd: break
        tmpIndex.append(objs[i].binNum)
    return tmpIndex

def getPlotObj(tmpData, binInfo, tmpIndexs):
    # columnValues = tmpData.columns.values
    tmpdf = tmpData.apply(lambda x: splitByBin(x, binInfo), axis=0)
    if len(tmpIndexs) == 1:
        tmpdf = tmpdf.iloc[0].apply(lambda x: [x])
    return tmpdf

def getTmpDataFromSourceData(sourceData, nameList, tmpIndex):
    if nameList:
        return sourceData.loc[tmpIndex, nameList]
    else:
        return sourceData.loc[tmpIndex, :]

def splitByBin(columnSeries, binInfo):
    grouped = columnSeries.groupby(columnSeries)
    tmpList, myList = [], []
    tmpName = []
    for name, group in grouped:
        for i in group.index:
            if not tmpList:
                tmpList.append(int(i))
                tmpName.append(name)
            else:
                if int(i) == tmpList[-1] + 1:
                    tmpList.append(int(i))
                else:
                    preName = tmpName.pop()
                    myList.append(RegionGroup(tmpList, binInfo, preName))
                    tmpList = [int(i)]
                    tmpName.append(name)
    preName = tmpName.pop()
    myList.append(RegionGroup(tmpList, binInfo, preName))
    return sorted(myList, key=lambda x: x.regionStart)

def validateFile(myFile):
    if not os.path.exists(myFile):
        raise Exception("File '%s' not found! Please input again!" % myFile)

    if not os.path.isfile(myFile):
        raise Exception("File '%s' is not a file! Please input again!" % myFile)

    return True

def validateDir(myDir):
    if not os.path.exists(myDir):
        raise Exception("Dir '%s' not found! Please input again!" % myDir)

    if not os.path.isdir(myDir):
        raise Exception("Dir '%s' is not a directory! Please input again!" % myDir)

    return True