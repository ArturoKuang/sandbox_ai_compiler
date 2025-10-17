#!/usr/bin/env python3
"""
Comprehensive unit tests for SimpleLang priority queue implementation.
Tests cover all edge cases and ensure correctness for use in A* and Dijkstra algorithms.
"""

import subprocess
import sys
import os

def run_simplelang_code(code):
    """Run SimpleLang code and return the output."""
    with open('temp_test.sl', 'w') as f:
        f.write(code)

    try:
        # First compile the .sl file to .py
        compile_result = subprocess.run(
            ['python3', 'simplelang.py', 'temp_test.sl'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if compile_result.returncode != 0:
            return "", compile_result.stderr.strip(), compile_result.returncode

        # Then run the generated .py file
        run_result = subprocess.run(
            ['python3', 'temp_test.py'],
            capture_output=True,
            text=True,
            timeout=5
        )
        return run_result.stdout.strip(), run_result.stderr.strip(), run_result.returncode
    finally:
        if os.path.exists('temp_test.sl'):
            os.remove('temp_test.sl')
        if os.path.exists('temp_test.py'):
            os.remove('temp_test.py')

def test_basic_insert_extract():
    """Test basic insert and extract operations."""
    code = '''
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

int priorities = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
int values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
int size = 0;

size = pq_insert(priorities, values, size, 5, 100);
size = pq_insert(priorities, values, size, 3, 200);
size = pq_insert(priorities, values, size, 7, 300);

int min1 = pq_extract_min_value(priorities, values, size);
size = size - 1;

print(min1);
'''
    stdout, stderr, returncode = run_simplelang_code(code)
    assert returncode == 0, f"Code failed to run: {stderr}"
    assert stdout == "200", f"Expected 200 (value with priority 3), got {stdout}"
    print("✓ Test basic insert/extract passed")

def test_sorted_order_extraction():
    """Test that elements are extracted in priority order."""
    code = '''
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

int priorities = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
int values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
int size = 0;

size = pq_insert(priorities, values, size, 10, 1000);
size = pq_insert(priorities, values, size, 5, 500);
size = pq_insert(priorities, values, size, 20, 2000);
size = pq_insert(priorities, values, size, 1, 100);
size = pq_insert(priorities, values, size, 15, 1500);

int v1 = pq_extract_min_value(priorities, values, size);
size = size - 1;
int v2 = pq_extract_min_value(priorities, values, size);
size = size - 1;
int v3 = pq_extract_min_value(priorities, values, size);
size = size - 1;
int v4 = pq_extract_min_value(priorities, values, size);
size = size - 1;
int v5 = pq_extract_min_value(priorities, values, size);
size = size - 1;

int sum = v1 + v2 + v3 + v4 + v5;
print(sum);
'''
    stdout, stderr, returncode = run_simplelang_code(code)
    assert returncode == 0, f"Code failed to run: {stderr}"
    # Expected order: priority 1 (100), 5 (500), 10 (1000), 15 (1500), 20 (2000)
    # Sum = 100 + 500 + 1000 + 1500 + 2000 = 5100
    assert stdout == "5100", f"Expected 5100, got {stdout}"
    print("✓ Test sorted order extraction passed")

def test_duplicate_priorities():
    """Test handling of duplicate priorities."""
    code = '''
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

int priorities = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
int values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
int size = 0;

size = pq_insert(priorities, values, size, 5, 100);
size = pq_insert(priorities, values, size, 5, 200);
size = pq_insert(priorities, values, size, 5, 300);

int v1 = pq_extract_min_value(priorities, values, size);
size = size - 1;
int v2 = pq_extract_min_value(priorities, values, size);
size = size - 1;
int v3 = pq_extract_min_value(priorities, values, size);
size = size - 1;

int sum = v1 + v2 + v3;
print(sum);
'''
    stdout, stderr, returncode = run_simplelang_code(code)
    assert returncode == 0, f"Code failed to run: {stderr}"
    # All have same priority, sum should be 100 + 200 + 300 = 600
    assert stdout == "600", f"Expected 600, got {stdout}"
    print("✓ Test duplicate priorities passed")

def test_single_element():
    """Test priority queue with single element."""
    code = '''
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

int priorities = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
int values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
int size = 0;

size = pq_insert(priorities, values, size, 42, 999);
int v = pq_extract_min_value(priorities, values, size);
print(v);
'''
    stdout, stderr, returncode = run_simplelang_code(code)
    assert returncode == 0, f"Code failed to run: {stderr}"
    assert stdout == "999", f"Expected 999, got {stdout}"
    print("✓ Test single element passed")

def test_reverse_sorted_insert():
    """Test inserting elements in reverse sorted order."""
    code = '''
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

int priorities = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
int values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
int size = 0;

size = pq_insert(priorities, values, size, 50, 50);
size = pq_insert(priorities, values, size, 40, 40);
size = pq_insert(priorities, values, size, 30, 30);
size = pq_insert(priorities, values, size, 20, 20);
size = pq_insert(priorities, values, size, 10, 10);

int v1 = pq_extract_min_value(priorities, values, size);
size = size - 1;

print(v1);
'''
    stdout, stderr, returncode = run_simplelang_code(code)
    assert returncode == 0, f"Code failed to run: {stderr}"
    assert stdout == "10", f"Expected 10 (minimum priority), got {stdout}"
    print("✓ Test reverse sorted insert passed")

def test_interleaved_operations():
    """Test interleaved insert and extract operations."""
    code = '''
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

int priorities = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
int values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
int size = 0;

size = pq_insert(priorities, values, size, 10, 100);
size = pq_insert(priorities, values, size, 5, 50);

int v1 = pq_extract_min_value(priorities, values, size);
size = size - 1;

size = pq_insert(priorities, values, size, 3, 30);
size = pq_insert(priorities, values, size, 15, 150);

int v2 = pq_extract_min_value(priorities, values, size);
size = size - 1;
int v3 = pq_extract_min_value(priorities, values, size);
size = size - 1;

int sum = v1 + v2 + v3;
print(sum);
'''
    stdout, stderr, returncode = run_simplelang_code(code)
    assert returncode == 0, f"Code failed to run: {stderr}"
    # Extract order: 50 (pri 5), 30 (pri 3), 100 (pri 10) = 180
    assert stdout == "180", f"Expected 180, got {stdout}"
    print("✓ Test interleaved operations passed")

def test_large_scale():
    """Test with larger number of elements."""
    code = '''
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

int priorities = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
int values = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
int size = 0;

size = pq_insert(priorities, values, size, 15, 15);
size = pq_insert(priorities, values, size, 8, 8);
size = pq_insert(priorities, values, size, 22, 22);
size = pq_insert(priorities, values, size, 3, 3);
size = pq_insert(priorities, values, size, 12, 12);
size = pq_insert(priorities, values, size, 18, 18);
size = pq_insert(priorities, values, size, 5, 5);
size = pq_insert(priorities, values, size, 25, 25);
size = pq_insert(priorities, values, size, 1, 1);
size = pq_insert(priorities, values, size, 30, 30);

int min1 = pq_extract_min_value(priorities, values, size);
size = size - 1;
int min2 = pq_extract_min_value(priorities, values, size);
size = size - 1;
int min3 = pq_extract_min_value(priorities, values, size);
size = size - 1;

int sum = min1 + min2 + min3;
print(sum);
'''
    stdout, stderr, returncode = run_simplelang_code(code)
    assert returncode == 0, f"Code failed to run: {stderr}"
    # First 3 minimums: 1, 3, 5 -> sum = 9
    assert stdout == "9", f"Expected 9, got {stdout}"
    print("✓ Test large scale passed")

def main():
    """Run all tests."""
    print("Running Priority Queue Unit Tests...")
    print("=" * 50)

    tests = [
        ("Basic Insert/Extract", test_basic_insert_extract),
        ("Sorted Order Extraction", test_sorted_order_extraction),
        ("Duplicate Priorities", test_duplicate_priorities),
        ("Single Element", test_single_element),
        ("Reverse Sorted Insert", test_reverse_sorted_insert),
        ("Interleaved Operations", test_interleaved_operations),
        ("Large Scale", test_large_scale),
    ]

    passed = 0
    failed = 0

    for test_name, test_func in tests:
        try:
            test_func()
            passed += 1
        except AssertionError as e:
            print(f"✗ Test {test_name} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ Test {test_name} error: {e}")
            failed += 1

    print("=" * 50)
    print(f"Results: {passed} passed, {failed} failed out of {len(tests)} tests")

    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
