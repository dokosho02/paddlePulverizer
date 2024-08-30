from operator import itemgetter
import numpy as np

from loguru import logger
from tqdm import tqdm

# necessary for image, not pdf


linespacePixels = 20    # pixel value

# ----------------------------
def numberInRange(element, testNumber, limitLower, limitUpper, bList):
    # group parts by divider
    if (testNumber >= limitLower) and (testNumber < limitUpper):
        bList.append(element)
    return bList
# ----------------------------
def arrangeVerticalSubOrder(sg):
    # arrange vetical order
    sk = sg
    for i in range(  len(sg) ):
        for j in range( len(sg) ):
            if j==i:
                continue
            y_i = sg[i][1]
            y_j = sg[j][1]

            if (np.absolute(y_i - y_j) < linespacePixels ):
                sk[j][1] = sk[i][1]
            
    sk = sorted(sk, key=itemgetter(1,0))

    return sk
# ----------------------------
def arrangeSubgroupsByColumn(xywhUncolumnedGroup, imagePagewidth, columns=1, pageColumnPercents=[]):
    # modified on 2021-04-02 at Uji
    subgroups = []                                        
    [ subgroups.append( [] ) for i in range(columns) ]    # list<list>, n subgroups for n columns

    divNumber = len(pageColumnPercents)
    if (columns==1):    # 1 column, divNumber == 0
        subgroups[0] = xywhUncolumnedGroup
    elif (divNumber>0):   # multi-column
        for xywh in xywhUncolumnedGroup:
            x,y,w,h = xywh
            xCenter = x + w/2

            if (xCenter < imagePagewidth*pageColumnPercents[0]/100.0):    # the first column
                subgroups[0].append(xywh)
            elif (xCenter >= imagePagewidth*pageColumnPercents[-1]/100.0):   # the last colum
                subgroups[-1].append(xywh)

            # the middle columns
            if ( divNumber > 1):
                for j in range(divNumber-1):
                    lower = imagePagewidth*pageColumnPercents[j]/100.0
                    upper = imagePagewidth*pageColumnPercents[j+1]/100.0
                    subgroups[j+1] = numberInRange(
                        element    = xywh,
                        testNumber = xCenter,
                        limitLower = lower,
                        limitUpper = upper,
                        bList      = subgroups[j+1]
                        )

    for i in range( len(subgroups) ):
        subgroups[i] = arrangeVerticalSubOrder(subgroups[i])

    xywhColumnedGroup = []
    for i in subgroups:
        xywhColumnedGroup = xywhColumnedGroup + i

    return xywhColumnedGroup


def removeDuplicate0(gl):
    k = []
    for i in range(1, len(gl) ):
            if ( gl[i-1] != gl[i] ):
                # groupFinal.remove(groupFinal[i])
                k.append(gl[i-1])
    k.append(gl[-1])

    # g = k
    # for i in range( len(g) ):
    #     x1,y1,w1,h1 = g[i]
    #     for j in range( len(g) ):
    #         if i==j:
    #             continue
    #         x2,y2,w2,h2 = g[j]

    #         if (x2>=x1) and (y2>=y1) and (x2+w2<=x1+w1) and (y2+h2<=y1+h1):
    #             k.remove( g[j] )

    return k
def removeDuplicate(gl):
    seen = []
    for i in gl:
        if i not in seen:
            seen.append(i)

    return seen
        


def showBlockPercents(xywh, imagePagewidth):
    x,y,w,h = xywh
    x2 = x + w
    y2 = y + h
    m = [x,x2]
    for i in range( len(m) ):
        m[i] = 100.0*m[i]/imagePagewidth
    logger.debug(m)
# ---------------------------------------
def arrangeOrder(xywhList,
        imagePagewidth,
        columns,
        pageDividerPercent,    # int
        pageColumnPercents):   # list<int>
    # logger.debug(pagewidth)

    vDividers = []
    kList = xywhList
    kList = sorted( kList, key=itemgetter(1) )

    # find dividers for multi-column page
    if (columns > 1):
        for xywh in kList:
            x,y,w,h= xywh    # the 3rd element is width parameter
            if w > imagePagewidth*pageDividerPercent/100.0:
                vDividers.append(xywh)
                # showBlockPercents(xywh, imagePagewidth)

    dividerNumber = len(vDividers)
    groups = []             # groups of blocks
    [ groups.append( [] ) for i in range(dividerNumber*2+1) ]    # list<list>, n dividers will generate n + 1 + n groups
    
    e_index = 1
    
    if ( dividerNumber < 1 ):   # divider does not exist
        groups[0] = kList      # len(groups) == 1
    else:                      # divider exists, number > 0
        for xywh in kList:
            x,y,w,h = xywh
            yCenter = y + h/2.0         # int?, center of y

            # the divider will be added to the latter part
            if   (yCenter < vDividers[0][e_index]):   # the first part
                groups[0].append(xywh)
            elif (yCenter > vDividers[-1][e_index] + vDividers[-1][-1] ):  # the last part, divider is added as the first element
                groups[-1].append(xywh)
            
            groups[1].append(vDividers[0])

            if dividerNumber > 1:
                for j in range(1, dividerNumber):   # the middle parts
                    groups[j*2] = numberInRange(
                        element     = xywh,
                        testNumber  = yCenter,
                        limitLower  = vDividers[j-1][e_index],
                        limitUpper  = vDividers[j][e_index],
                        bList       = groups[j*2]
                        )
                    groups[j*2+1]   = [ vDividers[j] ]

    
    # arrange horizontal position in subgroup
    for i in range( len(groups) ):
        groups[i] = sorted( groups[i], key=itemgetter(1) )

        if len(groups[i])>1:
            if (dividerNumber==0):    # no divider
                groups[i] = arrangeSubgroupsByColumn(groups[i],imagePagewidth,columns, pageColumnPercents)

            elif (dividerNumber>0):
                for j in vDividers:
                    if j not in groups[i]:
                        groups[i] = arrangeSubgroupsByColumn(groups[i],imagePagewidth,columns, pageColumnPercents)
    # one group with all block in correct order
    groupFinal = []
    for i in groups:
        if len(i)>0:
            groupFinal = groupFinal + i

    # remove duplicate
    k = groupFinal
    try:
        k = removeDuplicate(groupFinal)
    except:
        pass
    

    return k

# modified in Feb., 2022