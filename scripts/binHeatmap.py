#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
File name: binHeatmap.py
Author: CrazyHsu @ crazyhsu9527@gmail.com 
Created on: 2018-10-29 18:36:47
Last modified: 2018-10-29 18:36:48
'''

import argparse

#=================Parse Arguments===============
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--sourceBin", default="sourceBin.txt", type=str,
                    help="This is the source file you input to draw plot.")
parser.add_argument("-b", "--binInfo", default="binInfo.txt", type=str,
                    help="This is the bin info in each chromosome.")
parser.add_argument("-l", "--nameList", default=None, type=str,
                    help="This is the variaty name list you want to specify.")
parser.add_argument("-c", "--chr", default=None, type=str,
                    help="This is chromosome id you specified."
                         "Note: the id should be consitent with the id in bin info file.")
parser.add_argument("-i", "--intervel", default=None, type=str,
                    help="This is the intervel you want to specified."
                         "The format like: chrX:pos1-pos2."
                         "Note: the chrX should be consistent with the chromosome number in binInfo file!")
parser.add_argument("-t", "--transpose", default=False, action="store_true",
                    help="Transpose the figure in output directory if you specify the option!")
parser.add_argument("-o", "--out", default="output", type=str,
                    help="This is the output directory.")
args = parser.parse_args()

#===============================================
import pandas as pd
from plotGraph import *

def main():
    assert validateFile(args.sourceBin) and validateFile(args.binInfo)
    sourceBin = args.sourceBin
    binInfoFile = args.binInfo
    outDir = args.out
    chrId = args.chr
    transOutFig = args.transpose
    intervel = args.intervel
    if args.nameList:
        validateFile(args.nameList)
        nameList = getListFromFile(args.nameList)
    else:
        nameList = []
    binInfo = ParseBin(binInfoFile)
    sourceData = pd.read_table(sourceBin, index_col=0, header=0)
    try:
        assert validateDir(outDir)
    except:
        os.mkdir(outDir)
    if intervel:
        try:
            chrId = re.split("[:|-]", intervel)[0]
        except:
            raise Exception("You should input the right intervel format!")
    if chrId:
        if not chrId or chrId not in binInfo.binInfo.allChr:
            raise Exception("You should input the correct chromosome id in your source file!")
        else:
            plotSpecChr(chrId, binInfo, sourceData, nameList, outDir, intervel)
    else:
        for i in binInfo.binInfo.allChr:
            plotSpecChr(i, binInfo, sourceData, nameList, outDir, intervel)

if __name__ == "__main__":
    main()