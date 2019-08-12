#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
File name: plotGraph.py
Author: CrazyHsu @ crazyhsu9527@gmail.com 
Created on: 2018-11-01 12:47:29
Last modified: 2018-11-01 12:47:30
'''

from commonFunc import *
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches

#==================Variables===================
COLOR = ["#E60012", "#EB6100", "#F39800", "#FCC800", "#FFF100", "#CFDB00", "#8FC31F", "#22AC38",
         "#009944", "#009B6B", "#009E96", "#00A0C1", "#00A0E9", "#0086D1", "#0068B7", "#00479D",
         "#1D2088", "#601986", "#920783", "#BE0081", "#E4007F", "#E5006A", "#E5004F", "#E60033"]
FEMALENUM = range(1, 25)
FEMALECOLOR = dict(zip(FEMALENUM, COLOR))

PLOTHEIGHT, PLOTWIDTH = 11.0, 8.5
DISPLAY_HEIGHT = 0.98
AXIS_LEFT = 0.08
AXIS_WIDTH = 0.84
X_PAD_FRACTION = 0.01
Y_PAD_FRACTION = 0.01
PLOT_AREA_SPECS = {'font.weight': 'normal', 'legend.borderaxespad': 0.01, 'legend.handlelength': 0.02, \
                     'legend.handletextpad': 0.01, 'legend.labelspacing': 0.008}

#==================Methods=====================
def initPlots(width, height, **args):
    matplotlib.rcParams.update(PLOT_AREA_SPECS)
    matplotlib.rcParams['figure.figsize'] = width, height
    matplotlib.rcParams['font.size'] = 12
    matplotlib.rcParams['legend.fontsize'] = 3

def plot(plotObjs, chrLen, ax, tmpIndex):
    colNum = len(plotObjs)
    colWidth = 1.0/colNum
    paddingX = X_PAD_FRACTION
    paddingY = Y_PAD_FRACTION
    left = 0
    patchList = []
    nameList = []
    for obj in plotObjs:
        bottomLine = 0
        for i in range(len(obj)):
            # if i == 0: bottomLine = 0
            color = FEMALECOLOR[obj[i].name]
            height = obj[i].__len__()/float(chrLen)
            patch = patches.Rectangle((left, bottomLine), colWidth, height, fc=color, ec=None, lw=0)
            if obj[i].name not in nameList:
                patchList.append(patch)
                nameList.append(obj[i].name)
            bottomLine += height
            ax.add_patch(patch)
        left += colWidth
    newpatchList = [x for _, x in sorted(zip(nameList, patchList))]
    newNameList = sorted(nameList)
    # ax.legend(patchList, nameList, loc=7, fontsize="medium", handlelength=1, fancybox=True, bbox_to_anchor=(1.08, 0.5))

    ax.legend(newpatchList, newNameList, loc=7, fontsize="medium", handlelength=1, handletextpad=0.2,
              fancybox=True, bbox_to_anchor=(1.08, 0.5))
    ax.set_xlabel("Plant name")
    ax.set_xticks([])
    ax.set_xticklabels([])
    ax.set_xlim(0-paddingX, 1+paddingX)
    minIndex, maxIndex = min(tmpIndex), max(tmpIndex)
    ax.set_ylabel("Bin number")
    ax.set_yticks([0, 1])
    ax.set_yticklabels([minIndex, maxIndex])
    ax.set_ylim(0-paddingY, 1+paddingY)


def plotSpecChr(chrId, binInfo, sourceData, nameList, outDir, intervel):
    figOut = os.path.join(outDir, chrId+".pdf")
    if intervel:
        chrId, specStart, specEnd = re.split("[-|:]", intervel)
        specStart, specEnd = float(specStart), float(specEnd)
        if specStart > specEnd: raise Exception("You should input the right intervel format!")
        tmpIndexs = getIndexByOverlap(specStart, specEnd, binInfo, chrId)
        tmpIndexLen = reduce(lambda x, y: x + y, [binInfo.binInfo.allBins[i].length for i in tmpIndexs])
    else:
        tmpIndexs = binInfo.binInfo.allChr[chrId].keys()
        tmpIndexLen = binInfo.binInfo.allChrLen[chrId]
    tmpIndexs.sort(key=int)
    tmpData = getTmpDataFromSourceData(sourceData, nameList, tmpIndexs)
    plotObjs = getPlotObj(tmpData, binInfo, tmpIndexs)
    # chrLen = binInfo.binInfo.allChrLen[chrId]

    initPlots(PLOTHEIGHT, PLOTWIDTH)
    height = 0.9
    bottomLine = DISPLAY_HEIGHT - height
    ax = plt.axes([AXIS_LEFT, bottomLine, AXIS_WIDTH, height])
    plot(plotObjs, tmpIndexLen, ax, tmpIndexs)
    plt.savefig(figOut)