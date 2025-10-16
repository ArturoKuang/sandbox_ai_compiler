def minimumWeight(n: int, src1: int, src2: int, dest: int) -> int:
    dist1_0: int = 999999
    dist1_1: int = 999999
    dist1_2: int = 999999
    dist1_3: int = 999999
    dist1_4: int = 999999
    dist1_5: int = 999999
    dist2_0: int = 999999
    dist2_1: int = 999999
    dist2_2: int = 999999
    dist2_3: int = 999999
    dist2_4: int = 999999
    dist2_5: int = 999999
    distR_0: int = 999999
    distR_1: int = 999999
    distR_2: int = 999999
    distR_3: int = 999999
    distR_4: int = 999999
    distR_5: int = 999999
    visited1_0: bool = False
    visited1_1: bool = False
    visited1_2: bool = False
    visited1_3: bool = False
    visited1_4: bool = False
    visited1_5: bool = False
    visited2_0: bool = False
    visited2_1: bool = False
    visited2_2: bool = False
    visited2_3: bool = False
    visited2_4: bool = False
    visited2_5: bool = False
    visitedR_0: bool = False
    visitedR_1: bool = False
    visitedR_2: bool = False
    visitedR_3: bool = False
    visitedR_4: bool = False
    visitedR_5: bool = False
    if (src1 == 0):
        dist1_0 = 0
    if (src1 == 1):
        dist1_1 = 0
    if (src1 == 2):
        dist1_2 = 0
    if (src1 == 3):
        dist1_3 = 0
    if (src1 == 4):
        dist1_4 = 0
    if (src1 == 5):
        dist1_5 = 0
    if (src2 == 0):
        dist2_0 = 0
    if (src2 == 1):
        dist2_1 = 0
    if (src2 == 2):
        dist2_2 = 0
    if (src2 == 3):
        dist2_3 = 0
    if (src2 == 4):
        dist2_4 = 0
    if (src2 == 5):
        dist2_5 = 0
    if (dest == 0):
        distR_0 = 0
    if (dest == 1):
        distR_1 = 0
    if (dest == 2):
        distR_2 = 0
    if (dest == 3):
        distR_3 = 0
    if (dest == 4):
        distR_4 = 0
    if (dest == 5):
        distR_5 = 0
    proc1: int = 0
    while (proc1 < n):
        minDist: int = 999999
        minNode: int = (- 1)
        if ((not visited1_0) and (dist1_0 < minDist)):
            minDist = dist1_0
            minNode = 0
        if ((not visited1_1) and (dist1_1 < minDist)):
            minDist = dist1_1
            minNode = 1
        if ((not visited1_2) and (dist1_2 < minDist)):
            minDist = dist1_2
            minNode = 2
        if ((not visited1_3) and (dist1_3 < minDist)):
            minDist = dist1_3
            minNode = 3
        if ((not visited1_4) and (dist1_4 < minDist)):
            minDist = dist1_4
            minNode = 4
        if ((not visited1_5) and (dist1_5 < minDist)):
            minDist = dist1_5
            minNode = 5
        if (minNode == (- 1)):
            proc1 = n
        if (minNode == 0):
            visited1_0 = True
            if ((dist1_0 + 2) < dist1_2):
                dist1_2 = (dist1_0 + 2)
            if ((dist1_0 + 6) < dist1_5):
                dist1_5 = (dist1_0 + 6)
        if (minNode == 1):
            visited1_1 = True
            if ((dist1_1 + 3) < dist1_0):
                dist1_0 = (dist1_1 + 3)
            if ((dist1_1 + 5) < dist1_4):
                dist1_4 = (dist1_1 + 5)
        if (minNode == 2):
            visited1_2 = True
            if ((dist1_2 + 1) < dist1_1):
                dist1_1 = (dist1_2 + 1)
            if ((dist1_2 + 3) < dist1_3):
                dist1_3 = (dist1_2 + 3)
        if (minNode == 3):
            visited1_3 = True
            if ((dist1_3 + 2) < dist1_4):
                dist1_4 = (dist1_3 + 2)
        if (minNode == 4):
            visited1_4 = True
            if ((dist1_4 + 1) < dist1_5):
                dist1_5 = (dist1_4 + 1)
        if (minNode == 5):
            visited1_5 = True
        proc1 = (proc1 + 1)
    proc2: int = 0
    while (proc2 < n):
        minDist2: int = 999999
        minNode2: int = (- 1)
        if ((not visited2_0) and (dist2_0 < minDist2)):
            minDist2 = dist2_0
            minNode2 = 0
        if ((not visited2_1) and (dist2_1 < minDist2)):
            minDist2 = dist2_1
            minNode2 = 1
        if ((not visited2_2) and (dist2_2 < minDist2)):
            minDist2 = dist2_2
            minNode2 = 2
        if ((not visited2_3) and (dist2_3 < minDist2)):
            minDist2 = dist2_3
            minNode2 = 3
        if ((not visited2_4) and (dist2_4 < minDist2)):
            minDist2 = dist2_4
            minNode2 = 4
        if ((not visited2_5) and (dist2_5 < minDist2)):
            minDist2 = dist2_5
            minNode2 = 5
        if (minNode2 == (- 1)):
            proc2 = n
        if (minNode2 == 0):
            visited2_0 = True
            if ((dist2_0 + 2) < dist2_2):
                dist2_2 = (dist2_0 + 2)
            if ((dist2_0 + 6) < dist2_5):
                dist2_5 = (dist2_0 + 6)
        if (minNode2 == 1):
            visited2_1 = True
            if ((dist2_1 + 3) < dist2_0):
                dist2_0 = (dist2_1 + 3)
            if ((dist2_1 + 5) < dist2_4):
                dist2_4 = (dist2_1 + 5)
        if (minNode2 == 2):
            visited2_2 = True
            if ((dist2_2 + 1) < dist2_1):
                dist2_1 = (dist2_2 + 1)
            if ((dist2_2 + 3) < dist2_3):
                dist2_3 = (dist2_2 + 3)
        if (minNode2 == 3):
            visited2_3 = True
            if ((dist2_3 + 2) < dist2_4):
                dist2_4 = (dist2_3 + 2)
        if (minNode2 == 4):
            visited2_4 = True
            if ((dist2_4 + 1) < dist2_5):
                dist2_5 = (dist2_4 + 1)
        if (minNode2 == 5):
            visited2_5 = True
        proc2 = (proc2 + 1)
    procR: int = 0
    while (procR < n):
        minDistR: int = 999999
        minNodeR: int = (- 1)
        if ((not visitedR_0) and (distR_0 < minDistR)):
            minDistR = distR_0
            minNodeR = 0
        if ((not visitedR_1) and (distR_1 < minDistR)):
            minDistR = distR_1
            minNodeR = 1
        if ((not visitedR_2) and (distR_2 < minDistR)):
            minDistR = distR_2
            minNodeR = 2
        if ((not visitedR_3) and (distR_3 < minDistR)):
            minDistR = distR_3
            minNodeR = 3
        if ((not visitedR_4) and (distR_4 < minDistR)):
            minDistR = distR_4
            minNodeR = 4
        if ((not visitedR_5) and (distR_5 < minDistR)):
            minDistR = distR_5
            minNodeR = 5
        if (minNodeR == (- 1)):
            procR = n
        if (minNodeR == 0):
            visitedR_0 = True
            if ((distR_0 + 3) < distR_1):
                distR_1 = (distR_0 + 3)
        if (minNodeR == 1):
            visitedR_1 = True
            if ((distR_1 + 1) < distR_2):
                distR_2 = (distR_1 + 1)
        if (minNodeR == 2):
            visitedR_2 = True
            if ((distR_2 + 2) < distR_0):
                distR_0 = (distR_2 + 2)
            if ((distR_2 + 3) < distR_3):
                distR_3 = (distR_2 + 3)
        if (minNodeR == 3):
            visitedR_3 = True
            if ((distR_3 + 2) < distR_4):
                distR_4 = (distR_3 + 2)
        if (minNodeR == 4):
            visitedR_4 = True
            if ((distR_4 + 1) < distR_5):
                distR_5 = (distR_4 + 1)
            if ((distR_4 + 5) < distR_1):
                distR_1 = (distR_4 + 5)
        if (minNodeR == 5):
            visitedR_5 = True
            if ((distR_5 + 1) < distR_4):
                distR_4 = (distR_5 + 1)
            if ((distR_5 + 6) < distR_0):
                distR_0 = (distR_5 + 6)
        procR = (procR + 1)
    minWeight: int = 999999
    total0: int = ((dist1_0 + dist2_0) + distR_0)
    if (total0 < minWeight):
        minWeight = total0
    total1: int = ((dist1_1 + dist2_1) + distR_1)
    if (total1 < minWeight):
        minWeight = total1
    total2: int = ((dist1_2 + dist2_2) + distR_2)
    if (total2 < minWeight):
        minWeight = total2
    total3: int = ((dist1_3 + dist2_3) + distR_3)
    if (total3 < minWeight):
        minWeight = total3
    total4: int = ((dist1_4 + dist2_4) + distR_4)
    if (total4 < minWeight):
        minWeight = total4
    total5: int = ((dist1_5 + dist2_5) + distR_5)
    if (total5 < minWeight):
        minWeight = total5
    return minWeight

numNodes: int = 6
source1: int = 0
source2: int = 1
destination: int = 5
result: int = minimumWeight(numNodes, source1, source2, destination)
print(result)