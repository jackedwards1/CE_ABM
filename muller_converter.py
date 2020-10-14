"""
This is the script I used to convert the output file with the clonal architecture into a format readable by
EvoFreq. This was an integral part of my Muller Plot pipeline.
"""

import sys
import csv

"""
Argument List Structure
[0]----'Single_file.py'
[1]----File names to condense
[2]----Column# (length of simulation)
[3]----Lower loop bound
[4]----Upper loop bound
[5]----Domain Size
[6]----Skip Parameter (Use 1 to include all time points, use n>1 to only include every nth time point)
[7]----Threshold (In Percent)
"""

timing = int(sys.argv[6])
columns = int(sys.argv[2]) / timing
threshold = float(sys.argv[7]) / 100

for i in range(int(sys.argv[3]), int(sys.argv[4]) + 1):
    core_name = sys.argv[1] + str(i)
    new_file = open("DS_" + sys.argv[5] + "_" + str(i) + ".csv", "a")
    data = [['parents', 'clones']]
    for t in range(0, columns + 1):
        data[0].append(t * timing)
    with open(core_name + '.txt', 'rt') as f:
        csv_reader = csv.reader(f)
        population = next(csv_reader)
        parents = next(csv_reader)
        clones = next(csv_reader)
        next(csv_reader)
        data.append([0, 0])
        initial_pop = next(csv_reader)
        for t in range(0, columns + 1):
            data[1].append(int(initial_pop[t * timing + 8]))
        for l in range(0, len(clones)):
            data.append([])
            data[l + 2].append(int(parents[l]))
            data[l + 2].append(int(clones[l]))
            pop = next(csv_reader)
            for t in range(0, columns + 1):
                data[l + 2].append(int(pop[t * timing + 8]))
    f.close()
    for r in range(0, len(data)):
        line_holder = str(data[r][0])
        for c in range(1, len(data[r])):
            line_holder += ',' + str(data[r][c])
        new_file.write(line_holder)
        new_file.write("\n")
    new_file.close()



