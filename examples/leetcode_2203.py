dist1_0: int = 0
dist1_1: int = 999999
dist1_2: int = 999999
dist1_3: int = 999999
dist1_4: int = 999999
dist1_5: int = 999999
dist2_0: int = 999999
dist2_1: int = 0
dist2_2: int = 999999
dist2_3: int = 999999
dist2_4: int = 999999
dist2_5: int = 999999
distR_0: int = 999999
distR_1: int = 999999
distR_2: int = 999999
distR_3: int = 999999
distR_4: int = 999999
distR_5: int = 0
iterations: int = 0
while (iterations < 6):
    if ((dist1_0 + 2) < dist1_2):
        dist1_2 = (dist1_0 + 2)
    if ((dist1_0 + 6) < dist1_5):
        dist1_5 = (dist1_0 + 6)
    if ((dist1_1 + 3) < dist1_0):
        dist1_0 = (dist1_1 + 3)
    if ((dist1_1 + 5) < dist1_4):
        dist1_4 = (dist1_1 + 5)
    if ((dist1_2 + 1) < dist1_1):
        dist1_1 = (dist1_2 + 1)
    if ((dist1_2 + 3) < dist1_3):
        dist1_3 = (dist1_2 + 3)
    if ((dist1_3 + 2) < dist1_4):
        dist1_4 = (dist1_3 + 2)
    if ((dist1_4 + 1) < dist1_5):
        dist1_5 = (dist1_4 + 1)
    iterations = (iterations + 1)
iterations = 0
while (iterations < 6):
    if ((dist2_0 + 2) < dist2_2):
        dist2_2 = (dist2_0 + 2)
    if ((dist2_0 + 6) < dist2_5):
        dist2_5 = (dist2_0 + 6)
    if ((dist2_1 + 3) < dist2_0):
        dist2_0 = (dist2_1 + 3)
    if ((dist2_1 + 5) < dist2_4):
        dist2_4 = (dist2_1 + 5)
    if ((dist2_2 + 1) < dist2_1):
        dist2_1 = (dist2_2 + 1)
    if ((dist2_2 + 3) < dist2_3):
        dist2_3 = (dist2_2 + 3)
    if ((dist2_3 + 2) < dist2_4):
        dist2_4 = (dist2_3 + 2)
    if ((dist2_4 + 1) < dist2_5):
        dist2_5 = (dist2_4 + 1)
    iterations = (iterations + 1)
iterations = 0
while (iterations < 6):
    if ((distR_2 + 2) < distR_0):
        distR_0 = (distR_2 + 2)
    if ((distR_5 + 6) < distR_0):
        distR_0 = (distR_5 + 6)
    if ((distR_0 + 3) < distR_1):
        distR_1 = (distR_0 + 3)
    if ((distR_4 + 5) < distR_1):
        distR_1 = (distR_4 + 5)
    if ((distR_1 + 1) < distR_2):
        distR_2 = (distR_1 + 1)
    if ((distR_3 + 3) < distR_2):
        distR_2 = (distR_3 + 3)
    if ((distR_4 + 2) < distR_3):
        distR_3 = (distR_4 + 2)
    if ((distR_5 + 1) < distR_4):
        distR_4 = (distR_5 + 1)
    iterations = (iterations + 1)
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
print(minWeight)