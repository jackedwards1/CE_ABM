"""
This script was used to extract the VAFs from the clonal architecture data. It outputs 2 files, one containing the
actual VAFs, and a "key" file containing the number of mutations in the simulation.
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
"""
input_file = sys.argv[1]
gens = int(sys.argv[2])
domain = sys.argv[3]
lower_bound = int(sys.argv[4])
upper_bound = int(sys.argv[5])
mutation_rate = 0.0007
death_rate = 0.15


def lineage_check(clone_id):
    if clone_id > 0:
        return True
    else:
        return False


for r in range(lower_bound, upper_bound + 1):
    current_file = input_file + str(r) + ".txt"
    with open(current_file, 'rt') as f:
        csv_reader = csv.reader(f)
        population = next(csv_reader)
        parents = next(csv_reader)
        daughters = next(csv_reader)
        next(csv_reader)
        total = float(population[gens])
        VAFs = []
        clone = next(csv_reader)
        VAFs.append([int(clone[0]), 1.0])
        for c in range(0, len(daughters)):
            clone = next(csv_reader)
            frequency = int(clone[8 + gens]) / total
            if frequency > 0:
                cid = int(clone[0])
                while lineage_check(cid):
                    new_clone = "yes"
                    for v in range(0, len(VAFs)):
                        if cid == VAFs[v][0]:
                            VAFs[v][1] += frequency
                            new_clone = "no"
                    if new_clone == "yes":
                        VAFs.append([cid, frequency])
                    parent_found = "no"
                    for p in range(0, len(daughters)):
                        if cid == int(daughters[p]):
                            cid = int(parents[p])
                            parent_found = "yes"
                    if parent_found == "no":
                        print("Error, no parent found")
                        cid = 0
    f.close()

    key_file = open("VAFs_key_DS" + domain + "_" + str(gens) + ".csv", "a")
    key_file.write(str(len(VAFs)))
    key_file.write("\n")
    key_file.close()

    new_file = open("VAFs_DS" + domain + "_" + str(gens) + ".csv", "a")
    line_holder = str(VAFs[0][1])
    for v in range(1, len(VAFs)):
        line_holder += ',' + str(VAFs[v][1])
    new_file.write(line_holder)
    new_file.write("\n")
    new_file.close()
