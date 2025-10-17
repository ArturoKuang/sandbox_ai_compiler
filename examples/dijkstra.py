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

def dijkstra(graph: int, n: int, src: int, dest: int) -> int:
    pqPriorities: int = [999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999]
    pqValues: int = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    pqSize: int = 0
    dist: int = [999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999]
    visited: int = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    inQueue: int = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    dist[src] = 0
    pqSize = pq_insert(pqPriorities, pqValues, pqSize, 0, src)
    inQueue[src] = 1
    while (pq_is_empty(pqSize) == 0):
        u: int = pq_extract_min_value(pqPriorities, pqValues, pqSize)
        pqSize = (pqSize - 1)
        inQueue[u] = 0
        if (visited[u] == 1):
            dummy: int = 0
        else:
            visited[u] = 1
            v: int = 0
            while (v < n):
                weight: int = graph[((u * n) + v)]
                if (((visited[v] == 0) and (weight != 0)) and (dist[u] != 999999)):
                    newDist: int = (dist[u] + weight)
                    if (newDist < dist[v]):
                        dist[v] = newDist
                        pqSize = pq_insert(pqPriorities, pqValues, pqSize, newDist, v)
                        inQueue[v] = 1
                v = (v + 1)
    return dist[dest]

n: int = 6
graph: int = [0, 7, 9, 0, 0, 14, 7, 0, 10, 15, 0, 0, 9, 10, 0, 11, 0, 2, 0, 15, 11, 0, 6, 0, 0, 0, 0, 6, 0, 9, 14, 0, 2, 0, 9, 0]
result: int = dijkstra(graph, n, 0, 5)
print(result)