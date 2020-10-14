"""
This scripts takes the VAFs from simulations and calculates the cumulative mutation distribution so that the inverse
VAFs can be plotted against the CMD.
"""

import sys
import csv

"""
Argument List Structure
[0]---- "VAF_converter"
[1]---- Input File Name
[2]---- Generations
[3]---- Domain Size
[4]---- Lower Bound
[5]---- Upper Bound
[6]---- # of Data Points
[7]---- Minimum Frequency Depth
"""
input_file = sys.argv[1]
gens = int(sys.argv[2])
domain = sys.argv[3]
lower_bound = int(sys.argv[4])
upper_bound = int(sys.argv[5])
data_points = int(sys.argv[6])
min_freq = float(sys.argv[7])


def lineage_check(clone_id):
    if clone_id > 0:
        return True
    else:
        return False


current_file = input_file + ".csv"
with open(current_file, 'rt') as f:
    csv_reader = csv.reader(f)
    for r in range(lower_bound, upper_bound + 1):
        vaf_holder = next(csv_reader)
        VAFs = []
        for v in range(0, len(vaf_holder)):
            VAFs.append(float(vaf_holder[v]))
        M_f = []
        inverse_freq = []
        for i in range(0, data_points):
            inverse_freq.append(1 / (min_freq * data_points) * i)
            M_f.append(0)
            for v in range(0, len(VAFs)):
                if (1 / VAFs[v]) <= inverse_freq[i]:
                    M_f[i] += 1

        plot_file = open("Inverse_VAFS_DS" + domain + "_" + str(gens) + "_dp" + str(data_points) + "_r" + str(int(1 / (min_freq * data_points))) + ".csv", "a")
        freq_holder = str(inverse_freq[0])
        clone_holder = str(M_f[0])
        for p in range(1, len(inverse_freq)):
            freq_holder += ',' + str(inverse_freq[p])
            clone_holder += ',' + str(M_f[p])
        plot_file.write(freq_holder)
        plot_file.write("\n")
        plot_file.write(clone_holder)
        plot_file.write("\n")
        plot_file.close()
