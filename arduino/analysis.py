import numpy as np
import math

if __name__ == "__main__":

    file = "data.txt"

    # open file
    # read, strip and parse each line
    with open(file) as f:
        lines = [np.array([int(y) for y in x.strip()]) for x in f.readlines()]

    # normalize length
    min_len = len(lines[0])
    for line in lines[1:]:
        min_len = min(min_len, len(line))

    lines = [line[0:min_len] for line in lines]

    # init matrix to compute hamming distances
    hamming_distances = np.zeros((len(lines), len(lines)))

    # init array to compute stability
    summ = np.zeros(len(lines[0]))

    for i in range(0, len(lines)):

        # sum each line element-wise
        summ += np.array(lines[i])

        # for each pair of lines compute their hamming distance
        for j in range(i, len(lines)):
            hamming_distances[i, j] = (
                np.count_nonzero(lines[i] != lines[j]) if i != j else 0
            )
            hamming_distances[j, i] = hamming_distances[i, j]

    # if result is 0 or is exactly equal to the number of strings,
    # then the bit was always 0 or 1 respectively
    #
    # set to 0 stable bits and to 1 unstable bits
    # unstable means that they change at least once
    changes = [0 if x == len(lines) or x == 0 else 1 for x in summ]

    print(f"strings of {len(lines[0])} bits ({math.ceil(len(lines[0])/8)} bytes)")

    # count and unstable bits
    unstable_bits = []
    for i, bit in enumerate(changes):
        if bit != 0 and bit != len(lines):
            unstable_bits.append(i)
    print(
        f"number of bits changing at least once : {len(unstable_bits)} ({len(unstable_bits)/len(changes)*100} %)"
    )
    print(unstable_bits)

    # compute hammind distance percentages
    hamming_distances_perc = (hamming_distances / len(lines[0])) * 100

    # remove diagonal, i.e. do not consider the same string in comparison
    triu_indexes = np.triu_indices_from(hamming_distances_perc, k=1)
    hamming_distances_perc_nodiag = hamming_distances_perc[triu_indexes]

    print(f"max hd  (%) : {round(np.max(hamming_distances_perc_nodiag),6)}")
    print(f"min hd  (%) : {round(np.min(hamming_distances_perc_nodiag),6)}")
    print(f"mean hd (%) : {round(np.mean(hamming_distances_perc_nodiag),6)}")

    # count average number of ones
    number_of_ones = math.ceil(
        sum(np.count_nonzero(line) for line in lines) / len(lines)
    )
    print(f"|1s| : {number_of_ones} , |0s| : {len(lines[0]) - number_of_ones}")
    print(
        f"uniformity : {round(max(number_of_ones, len(lines[0]) - number_of_ones) / len(lines[0]) * 100,3)} %"
    )
