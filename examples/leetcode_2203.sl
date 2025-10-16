function minimumWeight(int n, int src1, int src2, int dest) {
    int dist1_0 = 999999;
    int dist1_1 = 999999;
    int dist1_2 = 999999;
    int dist1_3 = 999999;
    int dist1_4 = 999999;
    int dist1_5 = 999999;

    int dist2_0 = 999999;
    int dist2_1 = 999999;
    int dist2_2 = 999999;
    int dist2_3 = 999999;
    int dist2_4 = 999999;
    int dist2_5 = 999999;

    int distR_0 = 999999;
    int distR_1 = 999999;
    int distR_2 = 999999;
    int distR_3 = 999999;
    int distR_4 = 999999;
    int distR_5 = 999999;

    bool visited1_0 = false;
    bool visited1_1 = false;
    bool visited1_2 = false;
    bool visited1_3 = false;
    bool visited1_4 = false;
    bool visited1_5 = false;

    bool visited2_0 = false;
    bool visited2_1 = false;
    bool visited2_2 = false;
    bool visited2_3 = false;
    bool visited2_4 = false;
    bool visited2_5 = false;

    bool visitedR_0 = false;
    bool visitedR_1 = false;
    bool visitedR_2 = false;
    bool visitedR_3 = false;
    bool visitedR_4 = false;
    bool visitedR_5 = false;

    if (src1 == 0) {
        dist1_0 = 0;
    }
    if (src1 == 1) {
        dist1_1 = 0;
    }
    if (src1 == 2) {
        dist1_2 = 0;
    }
    if (src1 == 3) {
        dist1_3 = 0;
    }
    if (src1 == 4) {
        dist1_4 = 0;
    }
    if (src1 == 5) {
        dist1_5 = 0;
    }

    if (src2 == 0) {
        dist2_0 = 0;
    }
    if (src2 == 1) {
        dist2_1 = 0;
    }
    if (src2 == 2) {
        dist2_2 = 0;
    }
    if (src2 == 3) {
        dist2_3 = 0;
    }
    if (src2 == 4) {
        dist2_4 = 0;
    }
    if (src2 == 5) {
        dist2_5 = 0;
    }

    if (dest == 0) {
        distR_0 = 0;
    }
    if (dest == 1) {
        distR_1 = 0;
    }
    if (dest == 2) {
        distR_2 = 0;
    }
    if (dest == 3) {
        distR_3 = 0;
    }
    if (dest == 4) {
        distR_4 = 0;
    }
    if (dest == 5) {
        distR_5 = 0;
    }

    int proc1 = 0;
    while (proc1 < n) {
        int minDist = 999999;
        int minNode = -1;

        if (!visited1_0 && dist1_0 < minDist) {
            minDist = dist1_0;
            minNode = 0;
        }
        if (!visited1_1 && dist1_1 < minDist) {
            minDist = dist1_1;
            minNode = 1;
        }
        if (!visited1_2 && dist1_2 < minDist) {
            minDist = dist1_2;
            minNode = 2;
        }
        if (!visited1_3 && dist1_3 < minDist) {
            minDist = dist1_3;
            minNode = 3;
        }
        if (!visited1_4 && dist1_4 < minDist) {
            minDist = dist1_4;
            minNode = 4;
        }
        if (!visited1_5 && dist1_5 < minDist) {
            minDist = dist1_5;
            minNode = 5;
        }

        if (minNode == -1) {
            proc1 = n;
        }

        if (minNode == 0) {
            visited1_0 = true;
            if (dist1_0 + 2 < dist1_2) {
                dist1_2 = dist1_0 + 2;
            }
            if (dist1_0 + 6 < dist1_5) {
                dist1_5 = dist1_0 + 6;
            }
        }
        if (minNode == 1) {
            visited1_1 = true;
            if (dist1_1 + 3 < dist1_0) {
                dist1_0 = dist1_1 + 3;
            }
            if (dist1_1 + 5 < dist1_4) {
                dist1_4 = dist1_1 + 5;
            }
        }
        if (minNode == 2) {
            visited1_2 = true;
            if (dist1_2 + 1 < dist1_1) {
                dist1_1 = dist1_2 + 1;
            }
            if (dist1_2 + 3 < dist1_3) {
                dist1_3 = dist1_2 + 3;
            }
        }
        if (minNode == 3) {
            visited1_3 = true;
            if (dist1_3 + 2 < dist1_4) {
                dist1_4 = dist1_3 + 2;
            }
        }
        if (minNode == 4) {
            visited1_4 = true;
            if (dist1_4 + 1 < dist1_5) {
                dist1_5 = dist1_4 + 1;
            }
        }
        if (minNode == 5) {
            visited1_5 = true;
        }

        proc1 = proc1 + 1;
    }

    int proc2 = 0;
    while (proc2 < n) {
        int minDist2 = 999999;
        int minNode2 = -1;

        if (!visited2_0 && dist2_0 < minDist2) {
            minDist2 = dist2_0;
            minNode2 = 0;
        }
        if (!visited2_1 && dist2_1 < minDist2) {
            minDist2 = dist2_1;
            minNode2 = 1;
        }
        if (!visited2_2 && dist2_2 < minDist2) {
            minDist2 = dist2_2;
            minNode2 = 2;
        }
        if (!visited2_3 && dist2_3 < minDist2) {
            minDist2 = dist2_3;
            minNode2 = 3;
        }
        if (!visited2_4 && dist2_4 < minDist2) {
            minDist2 = dist2_4;
            minNode2 = 4;
        }
        if (!visited2_5 && dist2_5 < minDist2) {
            minDist2 = dist2_5;
            minNode2 = 5;
        }

        if (minNode2 == -1) {
            proc2 = n;
        }

        if (minNode2 == 0) {
            visited2_0 = true;
            if (dist2_0 + 2 < dist2_2) {
                dist2_2 = dist2_0 + 2;
            }
            if (dist2_0 + 6 < dist2_5) {
                dist2_5 = dist2_0 + 6;
            }
        }
        if (minNode2 == 1) {
            visited2_1 = true;
            if (dist2_1 + 3 < dist2_0) {
                dist2_0 = dist2_1 + 3;
            }
            if (dist2_1 + 5 < dist2_4) {
                dist2_4 = dist2_1 + 5;
            }
        }
        if (minNode2 == 2) {
            visited2_2 = true;
            if (dist2_2 + 1 < dist2_1) {
                dist2_1 = dist2_2 + 1;
            }
            if (dist2_2 + 3 < dist2_3) {
                dist2_3 = dist2_2 + 3;
            }
        }
        if (minNode2 == 3) {
            visited2_3 = true;
            if (dist2_3 + 2 < dist2_4) {
                dist2_4 = dist2_3 + 2;
            }
        }
        if (minNode2 == 4) {
            visited2_4 = true;
            if (dist2_4 + 1 < dist2_5) {
                dist2_5 = dist2_4 + 1;
            }
        }
        if (minNode2 == 5) {
            visited2_5 = true;
        }

        proc2 = proc2 + 1;
    }

    int procR = 0;
    while (procR < n) {
        int minDistR = 999999;
        int minNodeR = -1;

        if (!visitedR_0 && distR_0 < minDistR) {
            minDistR = distR_0;
            minNodeR = 0;
        }
        if (!visitedR_1 && distR_1 < minDistR) {
            minDistR = distR_1;
            minNodeR = 1;
        }
        if (!visitedR_2 && distR_2 < minDistR) {
            minDistR = distR_2;
            minNodeR = 2;
        }
        if (!visitedR_3 && distR_3 < minDistR) {
            minDistR = distR_3;
            minNodeR = 3;
        }
        if (!visitedR_4 && distR_4 < minDistR) {
            minDistR = distR_4;
            minNodeR = 4;
        }
        if (!visitedR_5 && distR_5 < minDistR) {
            minDistR = distR_5;
            minNodeR = 5;
        }

        if (minNodeR == -1) {
            procR = n;
        }

        if (minNodeR == 0) {
            visitedR_0 = true;
            if (distR_0 + 3 < distR_1) {
                distR_1 = distR_0 + 3;
            }
        }
        if (minNodeR == 1) {
            visitedR_1 = true;
            if (distR_1 + 1 < distR_2) {
                distR_2 = distR_1 + 1;
            }
        }
        if (minNodeR == 2) {
            visitedR_2 = true;
            if (distR_2 + 2 < distR_0) {
                distR_0 = distR_2 + 2;
            }
            if (distR_2 + 3 < distR_3) {
                distR_3 = distR_2 + 3;
            }
        }
        if (minNodeR == 3) {
            visitedR_3 = true;
            if (distR_3 + 2 < distR_4) {
                distR_4 = distR_3 + 2;
            }
        }
        if (minNodeR == 4) {
            visitedR_4 = true;
            if (distR_4 + 1 < distR_5) {
                distR_5 = distR_4 + 1;
            }
            if (distR_4 + 5 < distR_1) {
                distR_1 = distR_4 + 5;
            }
        }
        if (minNodeR == 5) {
            visitedR_5 = true;
            if (distR_5 + 1 < distR_4) {
                distR_4 = distR_5 + 1;
            }
            if (distR_5 + 6 < distR_0) {
                distR_0 = distR_5 + 6;
            }
        }

        procR = procR + 1;
    }

    int minWeight = 999999;

    int total0 = dist1_0 + dist2_0 + distR_0;
    if (total0 < minWeight) {
        minWeight = total0;
    }

    int total1 = dist1_1 + dist2_1 + distR_1;
    if (total1 < minWeight) {
        minWeight = total1;
    }

    int total2 = dist1_2 + dist2_2 + distR_2;
    if (total2 < minWeight) {
        minWeight = total2;
    }

    int total3 = dist1_3 + dist2_3 + distR_3;
    if (total3 < minWeight) {
        minWeight = total3;
    }

    int total4 = dist1_4 + dist2_4 + distR_4;
    if (total4 < minWeight) {
        minWeight = total4;
    }

    int total5 = dist1_5 + dist2_5 + distR_5;
    if (total5 < minWeight) {
        minWeight = total5;
    }

    return minWeight;
}

int numNodes = 6;
int source1 = 0;
int source2 = 1;
int destination = 5;

int result = minimumWeight(numNodes, source1, source2, destination);
print(result);
