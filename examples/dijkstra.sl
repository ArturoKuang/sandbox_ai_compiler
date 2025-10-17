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

function dijkstra(int graph, int n, int src, int dest) {
    int pqPriorities = [999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999];
    int pqValues = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
    int pqSize = 0;

    int dist = [999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999, 999999];
    int visited = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
    int inQueue = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];

    dist[src] = 0;
    pqSize = pq_insert(pqPriorities, pqValues, pqSize, 0, src);
    inQueue[src] = 1;

    while (pq_is_empty(pqSize) == 0) {
        int u = pq_extract_min_value(pqPriorities, pqValues, pqSize);
        pqSize = pqSize - 1;
        inQueue[u] = 0;

        if (visited[u] == 1) {
            int dummy = 0;
        } else {
            visited[u] = 1;

            int v = 0;
            while (v < n) {
                int weight = graph[u * n + v];
                if (visited[v] == 0 && weight != 0 && dist[u] != 999999) {
                    int newDist = dist[u] + weight;
                    if (newDist < dist[v]) {
                        dist[v] = newDist;
                        pqSize = pq_insert(pqPriorities, pqValues, pqSize, newDist, v);
                        inQueue[v] = 1;
                    }
                }
                v = v + 1;
            }
        }
    }

    return dist[dest];
}

int n = 6;
int graph = [
    0, 7, 9, 0, 0, 14,
    7, 0, 10, 15, 0, 0,
    9, 10, 0, 11, 0, 2,
    0, 15, 11, 0, 6, 0,
    0, 0, 0, 6, 0, 9,
    14, 0, 2, 0, 9, 0
];

int result = dijkstra(graph, n, 0, 5);
print(result);
