"""
This is a simple script for compiling various output files from multiple simulations. For example, you can use this
script to compile all of the phenotypic heterogeneity data from 50 simulations.
"""

import sys

"""
Argument List Structure
[0, 1, 2, 3, 4, 5]
[0]----'Single_file.py'
[1]----File names to condense (leaving off the simulation number)
[2]----Lower loop bound
[3]----Upper loop bound
[4]----New Line?
[5]----Out File name
"""

core_name = sys.argv[1]
new_file = open(sys.argv[5] + ".csv", "a")

for i in range(int(sys.argv[2]), int(sys.argv[3]) + 1):
    current_file = open(core_name + str(i) + '.txt', "r")
    new_file.write(current_file.read())
    if sys.argv[4] == 'yes':
        new_file.write("\n")
    current_file.close()
