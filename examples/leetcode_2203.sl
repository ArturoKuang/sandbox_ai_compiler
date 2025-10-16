function minimumWeight(int n, int src1, int src2, int dest) {
    int dist_src1_0 = 999999;
    int dist_src1_1 = 999999;
    int dist_src1_2 = 999999;
    int dist_src1_3 = 999999;
    int dist_src1_4 = 999999;
    int dist_src1_5 = 999999;

    int dist_src2_0 = 999999;
    int dist_src2_1 = 999999;
    int dist_src2_2 = 999999;
    int dist_src2_3 = 999999;
    int dist_src2_4 = 999999;
    int dist_src2_5 = 999999;

    int dist_dest_0 = 999999;
    int dist_dest_1 = 999999;
    int dist_dest_2 = 999999;
    int dist_dest_3 = 999999;
    int dist_dest_4 = 999999;
    int dist_dest_5 = 999999;

    if (src1 == 0) {
        dist_src1_0 = 0;
    }
    if (src1 == 1) {
        dist_src1_1 = 0;
    }
    if (src1 == 2) {
        dist_src1_2 = 0;
    }
    if (src1 == 3) {
        dist_src1_3 = 0;
    }
    if (src1 == 4) {
        dist_src1_4 = 0;
    }
    if (src1 == 5) {
        dist_src1_5 = 0;
    }

    if (src2 == 0) {
        dist_src2_0 = 0;
    }
    if (src2 == 1) {
        dist_src2_1 = 0;
    }
    if (src2 == 2) {
        dist_src2_2 = 0;
    }
    if (src2 == 3) {
        dist_src2_3 = 0;
    }
    if (src2 == 4) {
        dist_src2_4 = 0;
    }
    if (src2 == 5) {
        dist_src2_5 = 0;
    }

    if (dest == 0) {
        dist_dest_0 = 0;
    }
    if (dest == 1) {
        dist_dest_1 = 0;
    }
    if (dest == 2) {
        dist_dest_2 = 0;
    }
    if (dest == 3) {
        dist_dest_3 = 0;
    }
    if (dest == 4) {
        dist_dest_4 = 0;
    }
    if (dest == 5) {
        dist_dest_5 = 0;
    }

    int i = 0;
    while (i < n) {
        if (dist_src1_0 + 2 < dist_src1_2) {
            dist_src1_2 = dist_src1_0 + 2;
        }
        if (dist_src1_0 + 6 < dist_src1_5) {
            dist_src1_5 = dist_src1_0 + 6;
        }
        if (dist_src1_1 + 3 < dist_src1_0) {
            dist_src1_0 = dist_src1_1 + 3;
        }
        if (dist_src1_1 + 5 < dist_src1_4) {
            dist_src1_4 = dist_src1_1 + 5;
        }
        if (dist_src1_2 + 1 < dist_src1_1) {
            dist_src1_1 = dist_src1_2 + 1;
        }
        if (dist_src1_2 + 3 < dist_src1_3) {
            dist_src1_3 = dist_src1_2 + 3;
        }
        if (dist_src1_3 + 2 < dist_src1_4) {
            dist_src1_4 = dist_src1_3 + 2;
        }
        if (dist_src1_4 + 1 < dist_src1_5) {
            dist_src1_5 = dist_src1_4 + 1;
        }

        if (dist_src2_0 + 2 < dist_src2_2) {
            dist_src2_2 = dist_src2_0 + 2;
        }
        if (dist_src2_0 + 6 < dist_src2_5) {
            dist_src2_5 = dist_src2_0 + 6;
        }
        if (dist_src2_1 + 3 < dist_src2_0) {
            dist_src2_0 = dist_src2_1 + 3;
        }
        if (dist_src2_1 + 5 < dist_src2_4) {
            dist_src2_4 = dist_src2_1 + 5;
        }
        if (dist_src2_2 + 1 < dist_src2_1) {
            dist_src2_1 = dist_src2_2 + 1;
        }
        if (dist_src2_2 + 3 < dist_src2_3) {
            dist_src2_3 = dist_src2_2 + 3;
        }
        if (dist_src2_3 + 2 < dist_src2_4) {
            dist_src2_4 = dist_src2_3 + 2;
        }
        if (dist_src2_4 + 1 < dist_src2_5) {
            dist_src2_5 = dist_src2_4 + 1;
        }

        if (dist_dest_2 + 2 < dist_dest_0) {
            dist_dest_0 = dist_dest_2 + 2;
        }
        if (dist_dest_5 + 6 < dist_dest_0) {
            dist_dest_0 = dist_dest_5 + 6;
        }
        if (dist_dest_0 + 3 < dist_dest_1) {
            dist_dest_1 = dist_dest_0 + 3;
        }
        if (dist_dest_4 + 5 < dist_dest_1) {
            dist_dest_1 = dist_dest_4 + 5;
        }
        if (dist_dest_1 + 1 < dist_dest_2) {
            dist_dest_2 = dist_dest_1 + 1;
        }
        if (dist_dest_3 + 3 < dist_dest_2) {
            dist_dest_2 = dist_dest_3 + 3;
        }
        if (dist_dest_4 + 2 < dist_dest_3) {
            dist_dest_3 = dist_dest_4 + 2;
        }
        if (dist_dest_5 + 1 < dist_dest_4) {
            dist_dest_4 = dist_dest_5 + 1;
        }

        i = i + 1;
    }

    int minWeight = 999999;

    int total0 = dist_src1_0 + dist_src2_0 + dist_dest_0;
    if (total0 < minWeight) {
        minWeight = total0;
    }

    int total1 = dist_src1_1 + dist_src2_1 + dist_dest_1;
    if (total1 < minWeight) {
        minWeight = total1;
    }

    int total2 = dist_src1_2 + dist_src2_2 + dist_dest_2;
    if (total2 < minWeight) {
        minWeight = total2;
    }

    int total3 = dist_src1_3 + dist_src2_3 + dist_dest_3;
    if (total3 < minWeight) {
        minWeight = total3;
    }

    int total4 = dist_src1_4 + dist_src2_4 + dist_dest_4;
    if (total4 < minWeight) {
        minWeight = total4;
    }

    int total5 = dist_src1_5 + dist_src2_5 + dist_dest_5;
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
