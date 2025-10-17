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

function pq_peek_min_value(int values, int size) {
    if (size == 0) {
        return -1;
    }
    return values[0];
}

function pq_peek_min_priority(int priorities, int size) {
    if (size == 0) {
        return -1;
    }
    return priorities[0];
}

function pq_is_empty(int size) {
    if (size == 0) {
        return 1;
    }
    return 0;
}
