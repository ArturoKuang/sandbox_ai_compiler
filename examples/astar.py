def pq_swap(priorities: int, values: int, i: int, j: int) -> int:
    tempPriority: int = priorities[i]
    priorities[i] = priorities[j]
    priorities[j] = tempPriority
    tempValue: int = values[i]
    values[i] = values[j]
    values[j] = tempValue
    return 0

def pq_heapify_up(priorities: int, values: int, idx: int) -> int:
    while (idx > 0):
        parent: int = ((idx - 1) // 2)
        if (priorities[idx] < priorities[parent]):
            dummy: int = pq_swap(priorities, values, idx, parent)
            idx = parent
        else:
            return 0
    return 0

def pq_heapify_down(priorities: int, values: int, size: int, idx: int) -> int:
    while (1 == 1):
        left: int = ((2 * idx) + 1)
        right: int = ((2 * idx) + 2)
        smallest: int = idx
        if ((left < size) and (priorities[left] < priorities[smallest])):
            smallest = left
        if ((right < size) and (priorities[right] < priorities[smallest])):
            smallest = right
        if (smallest != idx):
            dummy: int = pq_swap(priorities, values, idx, smallest)
            idx = smallest
        else:
            return 0
    return 0

def pq_insert(priorities: int, values: int, size: int, priority: int, value: int) -> int:
    priorities[size] = priority
    values[size] = value
    dummy: int = pq_heapify_up(priorities, values, size)
    return (size + 1)

def pq_extract_min_value(priorities: int, values: int, size: int) -> int:
    if (size == 0):
        return (- 1)
    minValue: int = values[0]
    priorities[0] = priorities[(size - 1)]
    values[0] = values[(size - 1)]
    dummy: int = pq_heapify_down(priorities, values, (size - 1), 0)
    return minValue

def pq_is_empty(size: int) -> int:
    if (size == 0):
        return 1
    return 0

def abs(x: int) -> int:
    if (x < 0):
        return (0 - x)
    return x

def manhattan(x1: int, y1: int, x2: int, y2: int) -> int:
    dx: int = abs((x2 - x1))
    dy: int = abs((y2 - y1))
    return (dx + dy)

def astar(grid: int, width: int, height: int, startX: int, startY: int, goalX: int, goalY: int) -> int:
    maxSize: int = (width * height)
    pqPriorities: int = [999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999]
    pqValues: int = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    pqSize: int = 0
    closedSet: int = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    gScore: int = [999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999]
    inQueue: int = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    startIdx: int = ((startY * width) + startX)
    goalIdx: int = ((goalY * width) + goalX)
    gScore[startIdx] = 0
    startF: int = manhattan(startX, startY, goalX, goalY)
    pqSize = pq_insert(pqPriorities, pqValues, pqSize, startF, startIdx)
    inQueue[startIdx] = 1
    iterations: int = 0
    maxIterations: int = 100
    while ((iterations < maxIterations) and (pq_is_empty(pqSize) == 0)):
        current: int = pq_extract_min_value(pqPriorities, pqValues, pqSize)
        pqSize = (pqSize - 1)
        inQueue[current] = 0
        if (current == goalIdx):
            return gScore[current]
        closedSet[current] = 1
        currentX: int = (current % width)
        currentY: int = (current // width)
        dir: int = 0
        while (dir < 4):
            neighborX: int = currentX
            neighborY: int = currentY
            if (dir == 0):
                neighborY = (neighborY - 1)
            if (dir == 1):
                neighborX = (neighborX + 1)
            if (dir == 2):
                neighborY = (neighborY + 1)
            if (dir == 3):
                neighborX = (neighborX - 1)
            if ((((neighborX >= 0) and (neighborX < width)) and (neighborY >= 0)) and (neighborY < height)):
                neighborIdx: int = ((neighborY * width) + neighborX)
                if ((closedSet[neighborIdx] == 0) and (grid[neighborIdx] == 0)):
                    tentativeG: int = (gScore[current] + 1)
                    if (tentativeG < gScore[neighborIdx]):
                        gScore[neighborIdx] = tentativeG
                        fScore: int = (tentativeG + manhattan(neighborX, neighborY, goalX, goalY))
                        if (inQueue[neighborIdx] == 0):
                            pqSize = pq_insert(pqPriorities, pqValues, pqSize, fScore, neighborIdx)
                            inQueue[neighborIdx] = 1
            dir = (dir + 1)
        iterations = (iterations + 1)
    return (- 1)

width: int = 4
height: int = 4
grid: int = [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
result: int = astar(grid, width, height, 0, 0, 3, 3)
print(result)