function pq_swap(int priorities, int values, int i, int j) {
    int tempPriority = priorities[i];
    priorities[i] = priorities[j];
    priorities[j] = tempPriority;

    int tempValue = values[i];
    values[i] = values[j];
    values[j] = tempValue;

    return 0;
}

function pq_heapify_up(int priorities, int values, int idx) {
    while (idx > 0) {
        int parent = (idx - 1) / 2;

        if (priorities[idx] < priorities[parent]) {
            int dummy = pq_swap(priorities, values, idx, parent);
            idx = parent;
        } else {
            return 0;
        }
    }
    return 0;
}

function pq_heapify_down(int priorities, int values, int size, int idx) {
    while (1 == 1) {
        int left = 2 * idx + 1;
        int right = 2 * idx + 2;
        int smallest = idx;

        if (left < size && priorities[left] < priorities[smallest]) {
            smallest = left;
        }

        if (right < size && priorities[right] < priorities[smallest]) {
            smallest = right;
        }

        if (smallest != idx) {
            int dummy = pq_swap(priorities, values, idx, smallest);
            idx = smallest;
        } else {
            return 0;
        }
    }
    return 0;
}

function pq_insert(int priorities, int values, int size, int priority, int value) {
    priorities[size] = priority;
    values[size] = value;

    int dummy = pq_heapify_up(priorities, values, size);

    return size + 1;
}

function pq_extract_min_value(int priorities, int values, int size) {
    if (size == 0) {
        return -1;
    }

    int minValue = values[0];

    priorities[0] = priorities[size - 1];
    values[0] = values[size - 1];

    int dummy = pq_heapify_down(priorities, values, size - 1, 0);

    return minValue;
}

function pq_is_empty(int size) {
    if (size == 0) {
        return 1;
    }
    return 0;
}

function abs(int x) {
    if (x < 0) {
        return 0 - x;
    }
    return x;
}

function manhattan(int x1, int y1, int x2, int y2) {
    int dx = abs(x2 - x1);
    int dy = abs(y2 - y1);
    return dx + dy;
}

function astar(int grid, int width, int height, int startX, int startY, int goalX, int goalY) {
    int maxSize = width * height;
    int pqPriorities = [999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999];
    int pqValues = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
    int pqSize = 0;

    int closedSet = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
    int gScore = [999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999];
    int inQueue = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];

    int startIdx = startY * width + startX;
    int goalIdx = goalY * width + goalX;

    gScore[startIdx] = 0;
    int startF = manhattan(startX, startY, goalX, goalY);
    pqSize = pq_insert(pqPriorities, pqValues, pqSize, startF, startIdx);
    inQueue[startIdx] = 1;

    int iterations = 0;
    int maxIterations = 100;

    while (iterations < maxIterations && pq_is_empty(pqSize) == 0) {
        int current = pq_extract_min_value(pqPriorities, pqValues, pqSize);
        pqSize = pqSize - 1;
        inQueue[current] = 0;

        if (current == goalIdx) {
            return gScore[current];
        }

        closedSet[current] = 1;

        int currentX = current % width;
        int currentY = current / width;

        int dir = 0;
        while (dir < 4) {
            int neighborX = currentX;
            int neighborY = currentY;

            if (dir == 0) {
                neighborY = neighborY - 1;
            }
            if (dir == 1) {
                neighborX = neighborX + 1;
            }
            if (dir == 2) {
                neighborY = neighborY + 1;
            }
            if (dir == 3) {
                neighborX = neighborX - 1;
            }

            if (neighborX >= 0 && neighborX < width && neighborY >= 0 && neighborY < height) {
                int neighborIdx = neighborY * width + neighborX;

                if (closedSet[neighborIdx] == 0 && grid[neighborIdx] == 0) {
                    int tentativeG = gScore[current] + 1;

                    if (tentativeG < gScore[neighborIdx]) {
                        gScore[neighborIdx] = tentativeG;
                        int fScore = tentativeG + manhattan(neighborX, neighborY, goalX, goalY);

                        if (inQueue[neighborIdx] == 0) {
                            pqSize = pq_insert(pqPriorities, pqValues, pqSize, fScore, neighborIdx);
                            inQueue[neighborIdx] = 1;
                        }
                    }
                }
            }

            dir = dir + 1;
        }

        iterations = iterations + 1;
    }

    return -1;
}

int width = 4;
int height = 4;
int grid = [
    0, 0, 0, 0,
    0, 1, 1, 0,
    0, 0, 0, 0,
    0, 0, 0, 0
];

int result = astar(grid, width, height, 0, 0, 3, 3);
print(result);
