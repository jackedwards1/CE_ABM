# Version 2.6.0


# Imports
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import random as rd
import sys

# Program Loop
"""
Input Parameters:
[0] File Name
[1] Loop Size
[2] Gland Size
[3] Generations
[4] Image Frequency
[5] Loop Start
[6] Factor Graphics
[7] Neutral Statistics (Old Muller)
[8] Driver Impact
"""

initial = int(sys.argv[5])
executions = int(sys.argv[1])
gens = int(sys.argv[3])
initial_grid = int(sys.argv[2])
initial_membrane = 10
initial_cells = 25              # ideally a perfect square
time_skip = int(sys.argv[4])
file_name = 'T_' + str(gens) + '_DomainSize_' + str(initial_grid) + '_Run_'
file_type = '.txt'
muller_file_name = 'T_' + str(gens) + '_M_DomainSize_' + str(initial_grid) + '_Run_'
image_file_name = 'Run_' + str(gens) + '_' + str(initial_grid) + '_Images_'
plot_name = 'P_' + str(gens) + '_DS_' + str(initial_grid) + '_Run_'
factor_graphics = sys.argv[6]
muller = sys.argv[7]
impact = sys.argv[8]            # either 'low' or 'reg'
distinct_num = 4
max_frequency = 1

# Global Variables
g_start = initial_grid
switch = 'off'
max_grid = 601
passenger_rate = 0.5
driver_rate = 0.07
selfish_bias = 0              # the amount favoring mutating selfish vs cooperative
base_fitness = 50             # in percent
switch_frequency = 0.002
selfish_driver_min = 0
selfish_driver_max = 0
cooperator_driver_min = 0
cooperator_driver_max = 0
if impact == 'low':
    selfish_driver_min = 2.5
    selfish_driver_max = 7.5
    cooperator_driver_min = 2.5
    cooperator_driver_max = 7.5
elif impact == 'reg':
    selfish_driver_min = 10.5
    selfish_driver_max = 20
    cooperator_driver_min = 10.5
    cooperator_driver_max = 20
switching_punishment = 1
switching_penalty = 10          # in percent
passenger_mod_range = 0.05      # in percent
mod_resolution = 0.001          # in percent
bin_number = 100
factor_produce_chance = 40      # in percent
base_death_rate = 15            # in percent
s_penalty = 0                   # in percent
c_penalty = 0
factor_radius = 2
factor_threshold_perCell = 10
cell_density_threshold = 80     # in percent
chunk_size = 1
membrane_thickness = initial_membrane - 1
membrane_gap = initial_grid - 1
gx_min = max_grid / 2 - g_start / 2 - 1
gy_min = max_grid / 2 - g_start / 2 - 1
gx_max = max_grid / 2 + g_start / 2 + 2
gy_max = max_grid / 2 + g_start / 2 + 2
if g_start == max_grid:
    gx_min = 0
    gy_min = 0
    gx_max = max_grid
    gy_max = max_grid
rows = []
n_rows = []
data_rows = np.zeros((max_grid, max_grid))
factor_grid = np.zeros((max_grid, max_grid))
gsize = 2
m_y = 2000
scaling = 3
m_x = gens * scaling
division_counter = 0
passenger_counter = 0
driver_counter = 0
clone_ID_counter = 0

if factor_graphics == 'on':
    max_color = factor_radius + 1
    for f in range(1, factor_radius + 1):
        max_color += (factor_radius + 1 - f) * (2 * f + 1) ** 2 - 1

if g_start == 25:
    frame_shift_g = membrane_gap + 1
    frame_shift_m = membrane_thickness / 3 - 1
if g_start == 51:
    frame_shift_g = membrane_gap / 2 + membrane_thickness / 2 + 1
    frame_shift_m = 0
if g_start == 101:
    frame_shift_g = 4 * membrane_gap / 5 + membrane_thickness / 2 - 1
    frame_shift_m = 0
if g_start == 301:
    frame_shift_g = membrane_gap / 2 + membrane_thickness
    frame_shift_m = 0
if g_start == 601:
    frame_shift_g = 0
    frame_shift_m = 0
membrane_counter_x = frame_shift_m
gap_counter_x = frame_shift_g
membrane_counter_y = frame_shift_m
gap_counter_y = frame_shift_g
t_counter = 0
initial_xes = 0

# print('Starting array')
# Array Establishment
for y in xrange(0, max_grid):
    rows.append([])
    n_rows.append([])
    for x in xrange(0, max_grid):
        rows[y].append(['E'])
        n_rows[y].append(['E'])
for y in xrange(0, max_grid):
    for x in xrange(0, max_grid):
        if gap_counter_x <= membrane_gap:
            gap_counter_x += 1
        elif membrane_counter_x <= membrane_thickness:
            rows[y][x] = ['X']
            n_rows[y][x] = ['X']
            if y == 0 or y == max_grid - 1 or x == 0 or x == max_grid - 1:
                initial_xes += 1
            membrane_counter_x += 1
        else:
            gap_counter_x = 1
            membrane_counter_x = 0
    gap_counter_x = frame_shift_g
    membrane_counter_x = frame_shift_m
for x in xrange(0, max_grid):
    for y in xrange(0, max_grid):
        if gap_counter_y <= membrane_gap:
            gap_counter_y += 1
        elif membrane_counter_y <= membrane_thickness:
            rows[y][x] = ['X']
            n_rows[y][x] = ['X']
            if y == 0 or y == max_grid - 1 or x == 0 or x == max_grid - 1:
                initial_xes += 1
            membrane_counter_y += 1
        else:
            gap_counter_y = 1
            membrane_counter_y = 0
    gap_counter_y = frame_shift_g
    membrane_counter_y = frame_shift_m
side_len = int(initial_cells ** 0.5)
for y in xrange(side_len / 2 - side_len + 1, side_len / 2 + 1):
    for x in xrange(side_len / 2 - side_len + 1, side_len / 2 + 1):
        rows[max_grid // 2 + y][max_grid // 2 + x] = ['N', [0, 0], 0, 0, 0, 0, 0, 0, -12 + 110, 0]
        n_rows[max_grid // 2 + y][max_grid // 2 + x] = ['N', [0, 0], 0, 0, 0, 0, 0, 0, -12 + 110, 0]

# print('Array done')
"""
    ['0', [1, 1], 2, 3, 4, 5, 6, 7, 8, 9]
    [0]----Cell Type    'E'--Empty      'N'--Normal      'S'--Selfish      'C'--Cooperative         'X'--Membrane           'D'--Dead
    [1]----[Selfish Drivers, Cooperative Drivers] 
    [2]----Cooperator Mutation Switch
    [3]----Expansion Factor Switch
    [4]----Proliferation Bonus (in percent) 
    [5]----Cooperation Bonus  (in percent)   
    [6]----Passenger Counter  
    [7]----Clone ID #           Gets the latest driver counter value when mutating
    [8]----Phenotype ID #       Gets the color value of the cell based on [0] and its bin number
    [9]----Invisible Passengers
"""


# Growth Functions
def mutation(fi, si, m_type, time):
    global driver_counter
    global passenger_counter
    global clone_ID_counter
    cell_type = n_rows[fi][si][0]
    if m_type == 'driver':
        driver_counter += 1
        clone_ID_counter += 1
        if cell_type == 'N':
            if 50 - selfish_bias <= rd.randint(1, 100):
                n_rows[fi][si][0] = 'S'
                n_rows[fi][si][1][0] += 1
                n_rows[fi][si][2] = 0
                min_int = selfish_driver_min / mod_resolution
                max_int = selfish_driver_max / mod_resolution
                n_rows[fi][si][4] += mod_resolution * rd.randint(min_int, max_int)
                color_bin = bin_sorter(fi, si)
                n_rows[fi][si][8] = 20 - color_bin + 110
            else:
                n_rows[fi][si][0] = 'C'
                n_rows[fi][si][1][1] += 1
                n_rows[fi][si][2] = 1
                min_int = cooperator_driver_min / mod_resolution
                max_int = cooperator_driver_max / mod_resolution
                n_rows[fi][si][5] += mod_resolution * rd.randint(min_int, max_int)
                color_bin = bin_sorter(fi, si)
                n_rows[fi][si][8] = -20 + color_bin + 110
        elif cell_type == 'S':
            if 50 - selfish_bias <= rd.randint(1, 100) or switch == 'off':
                n_rows[fi][si][1][0] += 1
                n_rows[fi][si][2] = 0
                min_int = selfish_driver_min / mod_resolution
                max_int = selfish_driver_max / mod_resolution
                n_rows[fi][si][4] += mod_resolution * rd.randint(min_int, max_int)
                color_bin = bin_sorter(fi, si)
                n_rows[fi][si][8] = 20 - color_bin + 110
            else:
                n_rows[fi][si][0] = 'C'
                n_rows[fi][si][1][0] = n_rows[fi][si][1][0] - switching_punishment
                n_rows[fi][si][1][1] += 1
                n_rows[fi][si][2] = 1
                n_rows[fi][si][4] = n_rows[fi][si][4] - switching_punishment * switching_penalty
                min_int = cooperator_driver_min / mod_resolution
                max_int = cooperator_driver_max / mod_resolution
                n_rows[fi][si][5] += mod_resolution * rd.randint(min_int, max_int)
                if n_rows[fi][si][1][0] < 0:
                    n_rows[fi][si][1][0] = 0
                    n_rows[fi][si][4] = 0
                    pass_int = passenger_mod_range / mod_resolution
                    for v in range(0, n_rows[fi][si][6]):
                        n_rows[fi][si][4] += mod_resolution * rd.randint(-pass_int, 0)
                color_bin = bin_sorter(fi, si)
                n_rows[fi][si][8] = -20 + color_bin + 110
        elif cell_type == 'C':
            if 50 - selfish_bias <= rd.randint(1, 100) and switch == 'on':
                n_rows[fi][si][0] = 'S'
                n_rows[fi][si][1][0] += 1
                n_rows[fi][si][1][1] = n_rows[fi][si][1][1] - switching_punishment
                n_rows[fi][si][2] = 0
                min_int = selfish_driver_min / mod_resolution
                max_int = selfish_driver_max / mod_resolution
                n_rows[fi][si][4] += mod_resolution * rd.randint(min_int, max_int)
                n_rows[fi][si][5] = n_rows[fi][si][5] - switching_punishment * switching_penalty
                if n_rows[fi][si][1][1] < 0:
                    n_rows[fi][si][1][1] = 0
                    n_rows[fi][si][5] = 0
                    pass_int = passenger_mod_range / mod_resolution
                    for v in range(0, n_rows[fi][si][6]):
                        n_rows[fi][si][5] += mod_resolution * rd.randint(-pass_int, 0)
                color_bin = bin_sorter(fi, si)
                n_rows[fi][si][8] = 20 - color_bin + 110
            else:
                n_rows[fi][si][1][1] += 1
                n_rows[fi][si][2] = 1
                min_int = cooperator_driver_min / mod_resolution
                max_int = cooperator_driver_max / mod_resolution
                n_rows[fi][si][5] += mod_resolution * rd.randint(min_int, max_int)
                color_bin = bin_sorter(fi, si)
                n_rows[fi][si][8] = -20 + color_bin + 110
        n_rows[fi][si][7] = clone_ID_counter
        n_rows[fi][si][9] = 0
        if muller == 'on':
            local_pop_list = []
            for T in range(0, time):
                local_pop_list.append(0)
            if n_rows[fi][si][0] == 'C':
                fitness = float(n_rows[fi][si][5]) + 50.0
            else:
                fitness = float(n_rows[fi][si][4]) + 50.0
            muller_array.append(
                [n_rows[fi][si][7], n_rows[fi][si][8], 'driver', n_rows[fi][si][0], n_rows[fi][si][1][0], n_rows[fi][si][1][1],
                 n_rows[fi][si][6], fitness, local_pop_list])
            ancestor_list[len(ancestor_list) - 1][1] = n_rows[fi][si][7]
    elif m_type == 'passenger':
        passenger_counter += 1
        n_rows[fi][si][6] += 1
        if cell_type == 'N' or cell_type == 'S':
            max_int = passenger_mod_range / mod_resolution
            n_rows[fi][si][4] += mod_resolution * rd.randint(-max_int, 0)
        elif cell_type == 'C':
            max_int = passenger_mod_range / mod_resolution
            n_rows[fi][si][4] += mod_resolution * rd.randint(-max_int, 0)
        if n_rows[fi][si][9] >= distinct_num:
            clone_ID_counter += 1
            n_rows[fi][si][7] = clone_ID_counter
            n_rows[fi][si][9] = 0
            if muller == 'on':
                local_pop_list = []
                for T in range(0, time):
                    local_pop_list.append(0)
                if n_rows[fi][si][0] == 'C':
                    fitness = float(n_rows[fi][si][5]) + 50.0
                else:
                    fitness = float(n_rows[fi][si][4]) + 50.0
                muller_array.append([n_rows[fi][si][7], n_rows[fi][si][8], 'passenger', n_rows[fi][si][0], n_rows[fi][si][1][0], n_rows[fi][si][1][1], n_rows[fi][si][6], fitness, local_pop_list])
                ancestor_list[len(ancestor_list) - 1][1] = n_rows[fi][si][7]


def divide_function(fi, si, direction, time):
    global division_counter
    division_counter += 1
    parent_values = []
    for m in xrange(0, 10):
        parent_values.append(rows[fi][si][m])
    parent_values[1] = [0, 0]
    parent_values[1][0] = rows[fi][si][1][0]
    parent_values[1][1] = rows[fi][si][1][1]

    if direction == 1:
        n_rows[fi - 1][si - 1] = ['P', [0, 0], 0, 0, 0, 0, 0, 0, 0, 0, 0]
        n_rows[fi - 1][si - 1][0] = parent_values[0]
        n_rows[fi - 1][si - 1][1][0] = parent_values[1][0]
        n_rows[fi - 1][si - 1][1][1] = parent_values[1][1]
        n_rows[fi - 1][si - 1][2] = parent_values[2]
        for u in xrange(4, 10):
            n_rows[fi - 1][si - 1][u] = parent_values[u]
        if rd.randint(1, 10000) <= driver_rate * 100:
            if muller == 'on':
                ancestor_list.append([n_rows[fi][si][7], 0, time])
            mutation(fi - 1, si - 1, 'driver', time)
        elif rd.randint(1, 10000) <= passenger_rate * 100:
            if muller == 'on' and parent_values[9] >= distinct_num:
                ancestor_list.append([n_rows[fi][si][7], 0, time])
            mutation(fi - 1, si - 1, 'passenger', time)

    elif direction == 2:
        n_rows[fi - 1][si] = ['P', [0, 0], 0, 0, 0, 0, 0, 0, 0, 0]
        n_rows[fi - 1][si][0] = parent_values[0]
        n_rows[fi - 1][si][1][0] = parent_values[1][0]
        n_rows[fi - 1][si][1][1] = parent_values[1][1]
        n_rows[fi - 1][si][2] = parent_values[2]
        for u in xrange(4, 10):
            n_rows[fi - 1][si][u] = parent_values[u]
        if rd.randint(1, 10000) <= driver_rate * 100:
            if muller == 'on':
                ancestor_list.append([n_rows[fi][si][7], 0, time])
            mutation(fi - 1, si, 'driver', time)
        elif rd.randint(1, 10000) <= passenger_rate * 100:
            if muller == 'on' and parent_values[9] >= distinct_num:
                ancestor_list.append([n_rows[fi][si][7], 0, time])
            mutation(fi - 1, si, 'passenger', time)

    elif direction == 3:
        n_rows[fi - 1][si + 1] = ['P', [0, 0], 0, 0, 0, 0, 0, 0, 0, 0]
        n_rows[fi - 1][si + 1][0] = parent_values[0]
        n_rows[fi - 1][si + 1][1][0] = parent_values[1][0]
        n_rows[fi - 1][si + 1][1][1] = parent_values[1][1]
        n_rows[fi - 1][si + 1][2] = parent_values[2]
        for u in xrange(4, 10):
            n_rows[fi - 1][si + 1][u] = parent_values[u]
        if rd.randint(1, 10000) <= driver_rate * 100:
            if muller == 'on':
                ancestor_list.append([n_rows[fi][si][7], 0, time])
            mutation(fi - 1, si + 1, 'driver', time)
        elif rd.randint(1, 10000) <= passenger_rate * 100:
            if muller == 'on' and parent_values[9] >= distinct_num:
                ancestor_list.append([n_rows[fi][si][7], 0, time])
            mutation(fi - 1, si + 1, 'passenger', time)

    elif direction == 4:
        n_rows[fi][si - 1] = ['P', [0, 0], 0, 0, 0, 0, 0, 0, 0, 0]
        n_rows[fi][si - 1][0] = parent_values[0]
        n_rows[fi][si - 1][1][0] = parent_values[1][0]
        n_rows[fi][si - 1][1][1] = parent_values[1][1]
        n_rows[fi][si - 1][2] = parent_values[2]
        for u in xrange(4, 10):
            n_rows[fi][si - 1][u] = parent_values[u]
        if rd.randint(1, 10000) <= driver_rate * 100:
            if muller == 'on':
                ancestor_list.append([n_rows[fi][si][7], 0, time])
            mutation(fi, si - 1, 'driver', time)
        elif rd.randint(1, 10000) <= passenger_rate * 100:
            if muller == 'on' and parent_values[9] >= distinct_num:
                ancestor_list.append([n_rows[fi][si][7], 0, time])
            mutation(fi, si - 1, 'passenger', time)

    elif direction == 5:
        n_rows[fi][si + 1] = ['P', [0, 0], 0, 0, 0, 0, 0, 0, 0, 0]
        n_rows[fi][si + 1][0] = parent_values[0]
        n_rows[fi][si + 1][1][0] = parent_values[1][0]
        n_rows[fi][si + 1][1][1] = parent_values[1][1]
        n_rows[fi][si + 1][2] = parent_values[2]
        for u in xrange(4, 10):
            n_rows[fi][si + 1][u] = parent_values[u]
        if rd.randint(1, 10000) <= driver_rate * 100:
            if muller == 'on':
                ancestor_list.append([n_rows[fi][si][7], 0, time])
            mutation(fi, si + 1, 'driver', time)
        elif rd.randint(1, 10000) <= passenger_rate * 100:
            if muller == 'on' and parent_values[9] >= distinct_num:
                ancestor_list.append([n_rows[fi][si][7], 0, time])
            mutation(fi, si + 1, 'passenger', time)

    elif direction == 6:
        n_rows[fi + 1][si - 1] = ['P', [0, 0], 0, 0, 0, 0, 0, 0, 0, 0]
        n_rows[fi + 1][si - 1][0] = parent_values[0]
        n_rows[fi + 1][si - 1][1][0] = parent_values[1][0]
        n_rows[fi + 1][si - 1][1][1] = parent_values[1][1]
        n_rows[fi + 1][si - 1][2] = parent_values[2]
        for u in xrange(4, 10):
            n_rows[fi + 1][si - 1][u] = parent_values[u]
        if rd.randint(1, 10000) <= driver_rate * 100:
            if muller == 'on':
                ancestor_list.append([n_rows[fi][si][7], 0, time])
            mutation(fi + 1, si - 1, 'driver', time)
        elif rd.randint(1, 10000) <= passenger_rate * 100:
            if muller == 'on' and parent_values[9] >= distinct_num:
                ancestor_list.append([n_rows[fi][si][7], 0, time])
            mutation(fi + 1, si - 1, 'passenger', time)

    elif direction == 7:
        n_rows[fi + 1][si] = ['P', [0, 0], 0, 0, 0, 0, 0, 0, 0, 0]
        n_rows[fi + 1][si][0] = parent_values[0]
        n_rows[fi + 1][si][1][0] = parent_values[1][0]
        n_rows[fi + 1][si][1][1] = parent_values[1][1]
        n_rows[fi + 1][si][2] = parent_values[2]
        for u in xrange(4, 10):
            n_rows[fi + 1][si][u] = parent_values[u]
        if rd.randint(1, 10000) <= driver_rate * 100:
            if muller == 'on':
                ancestor_list.append([n_rows[fi][si][7], 0, time])
            mutation(fi + 1, si, 'driver', time)
        elif rd.randint(1, 10000) <= passenger_rate * 100:
            if muller == 'on' and parent_values[9] >= distinct_num:
                ancestor_list.append([n_rows[fi][si][7], 0, time])
            mutation(fi + 1, si, 'passenger', time)

    elif direction == 8:
        n_rows[fi + 1][si + 1] = ['P', [0, 0], 0, 0, 0, 0, 0, 0, 0, 0]
        n_rows[fi + 1][si + 1][0] = parent_values[0]
        n_rows[fi + 1][si + 1][1][0] = parent_values[1][0]
        n_rows[fi + 1][si + 1][1][1] = parent_values[1][1]
        n_rows[fi + 1][si + 1][2] = parent_values[2]
        for u in xrange(4, 10):
            n_rows[fi + 1][si + 1][u] = parent_values[u]
        if rd.randint(1, 10000) <= driver_rate * 100:
            if muller == 'on':
                ancestor_list.append([n_rows[fi][si][7], 0, time])
            mutation(fi + 1, si + 1, 'driver', time)
        elif rd.randint(1, 10000) <= passenger_rate * 100:
            if muller == 'on' and parent_values[9] >= distinct_num:
                ancestor_list.append([n_rows[fi][si][7], 0, time])
            mutation(fi + 1, si + 1, 'passenger', time)


def divide_check(fi, si, time, restriction_list):
    direction = []
    if 1 not in restriction_list:
        if 'E' in rows[fi - 1][si - 1] and 'E' in n_rows[fi - 1][si - 1]:
            direction.append(1)
        elif 'D' in rows[fi - 1][si - 1] and 'D' in n_rows[fi - 1][si - 1]:
            direction.append(1)
    if 2 not in restriction_list:
        if 'E' in rows[fi - 1][si] and 'E' in n_rows[fi - 1][si]:
            direction.append(2)
        elif 'D' in rows[fi - 1][si] and 'D' in n_rows[fi - 1][si]:
            direction.append(2)
    if 3 not in restriction_list:
        if 'E' in rows[fi - 1][si + 1] and 'E' in n_rows[fi - 1][si + 1]:
            direction.append(3)
        elif 'D' in rows[fi - 1][si + 1] and 'D' in n_rows[fi - 1][si + 1]:
            direction.append(3)
    if 4 not in restriction_list:
        if 'E' in rows[fi][si - 1] and 'E' in n_rows[fi][si - 1]:
            direction.append(4)
        elif 'D' in rows[fi][si - 1] and 'D' in n_rows[fi][si - 1]:
            direction.append(4)
    if 5 not in restriction_list:
        if 'E' in rows[fi][si + 1] and 'E' in n_rows[fi][si + 1]:
            direction.append(5)
        elif 'D' in rows[fi][si + 1] and 'D' in n_rows[fi][si + 1]:
            direction.append(5)
    if 6 not in restriction_list:
        if 'E' in rows[fi + 1][si - 1] and 'E' in n_rows[fi + 1][si - 1]:
            direction.append(6)
        elif 'D' in rows[fi + 1][si - 1] and 'D' in n_rows[fi + 1][si - 1]:
            direction.append(6)
    if 7 not in restriction_list:
        if 'E' in rows[fi + 1][si] and 'E' in n_rows[fi + 1][si]:
            direction.append(7)
        elif 'D' in rows[fi + 1][si] and 'D' in n_rows[fi + 1][si]:
            direction.append(7)
    if 8 not in restriction_list:
        if 'E' in rows[fi + 1][si + 1] and 'E' in n_rows[fi + 1][si + 1]:
            direction.append(8)
        elif 'D' in rows[fi + 1][si + 1] and 'D' in n_rows[fi + 1][si + 1]:
            direction.append(8)
    if len(direction) == 0:
        return
    else:
        rd.shuffle(direction)
    # print('Cell [' + str(fi) + '][' + str(si) + '] is dividing to ' + str(direction[0]))
        divide_function(fi, si, direction[0], time)


def divide_fitness(fi, si, time, restriction_list):
    if rows[fi][si][2] == 0:
        fitness = base_fitness + rows[fi][si][4]
        if fitness * 1000 >= rd.randint(1, 100000):
            divide_check(fi, si, time, restriction_list)
    elif rows[fi][si][2] == 1:
        fitness = base_fitness - rows[fi][si][6] * passenger_mod_range / 2
        if fitness * 1000 >= rd.randint(1, 100000):
            divide_check(fi, si, time, restriction_list)


def divide(time):
    cell_list = []
    for y in xrange(gy_min, gy_max):
        for x in xrange(gx_min, gx_max):
            if 'E' in rows[y][x]:
                pass
            elif 'D' in rows[y][x]:
                pass
            elif 'X' in rows[y][x]:
                pass
            else:
                cell_list.append([y, x])
    if len(cell_list) <= 0:
        return
    rd.shuffle(cell_list)
    while len(cell_list) > 0:
        if cell_list[0][0] != gy_min and cell_list[0][1] != gx_min and cell_list[0][0] != (gy_max - 1) \
                and cell_list[0][1] != (gx_max - 1):
            divide_fitness(cell_list[0][0], cell_list[0][1], time, [0])
        elif cell_list[0][0] == gy_min and cell_list[0][1] == gx_min:
            divide_fitness(gy_min, gx_min, time, [1, 2, 3, 4, 6])
        elif cell_list[0][0] == gy_min and cell_list[0][1] == (gx_max - 1):
            divide_fitness(gy_min, gx_max - 1, time, [1, 2, 3, 5, 8])
        elif cell_list[0][0] == (gy_max - 1) and cell_list[0][1] == gx_min:
            divide_fitness(gy_max - 1, gx_min, time, [1, 4, 6, 7, 8])
        elif cell_list[0][0] == (gy_max - 1) and cell_list[0][1] == (gx_max - 1):
            divide_fitness(gy_max - 1, gx_max - 1, time, [3, 5, 6, 7, 8])
        elif cell_list[0][0] == gy_min and cell_list[0][1] != gx_min and cell_list[0][1] != (gx_max - 1):
            divide_fitness(gy_min, cell_list[0][1], time, [1, 2, 3])
        elif cell_list[0][0] == (gy_max - 1) and cell_list[0][1] != gx_min and cell_list[0][1] != (gx_max - 1):
            divide_fitness(gy_max - 1, cell_list[0][1], time, [6, 7, 8])
        elif cell_list[0][0] != gy_min and cell_list[0][0] != (gy_max - 1) and cell_list[0][1] == gx_min:
            divide_fitness(cell_list[0][0], gx_min, time, [1, 4, 6])
        elif cell_list[0][0] != gy_min and cell_list[0][0] != (gy_max - 1) and cell_list[0][1] == (gx_max - 1):
            divide_fitness(cell_list[0][0], (gx_max - 1), time, [3, 5, 8])

        del cell_list[0]

    # Population Functions


# Population Functions
def phenotype_switch():
    for y in xrange(gy_min, gy_max):
        for x in xrange(gx_min, gx_max):
            if 'S' in n_rows[y][x]:
                if rd.randint(1, 1000) <= switch_frequency * 1000:
                    n_rows[y][x][0] = 'C'
                    n_rows[y][x][2] = 1
                    color_bin = bin_sorter(y, x)
                    n_rows[y][x][8] = -20 + color_bin + 110
            elif 'C' in n_rows[y][x]:
                if rd.randint(1, 1000) <= switch_frequency * 1000:
                    n_rows[y][x][0] = 'S'
                    n_rows[y][x][2] = 0
                    color_bin = bin_sorter(y, x)
                    n_rows[y][x][8] = 20 - color_bin + 110


def population_count(usage):
    counter = 0
    threshold = 0
    if usage == 'death':
        threshold = 10
    if usage == 'growth':
        threshold == initial_grid ** 2 / 2
    for y in xrange(gy_min, gy_max):
        for x in xrange(gx_min, gx_max):
            if 'E' not in n_rows[y][x] and 'X' not in n_rows[y][x] and 'D' not in n_rows[y][x]:
                counter += 1
                if counter > threshold:
                    return True


def bin_sorter(fi, si):
    cell_prolif = base_fitness
    cell_produce = factor_produce_chance
    divider_num = float(bin_number) / bin_number
    if n_rows[fi][si][2] == 0:
        cell_prolif += n_rows[fi][si][4]
        for b in xrange(0, bin_number):
            current_div = (b + 1) * divider_num
            if cell_prolif <= current_div:
                return b
        return bin_number - 1
    elif n_rows[fi][si][2] == 1:
        cell_produce += n_rows[fi][si][5]
        for b in xrange(0, bin_number):
            current_div = (b + 1) * divider_num
            if cell_produce <= current_div:
                return b
        return bin_number - 1


def muller_resolution(m, c):
    if m >= c:
        return m
    else:
        return c


def x_checker():
    if selfish_bins == -50:
        return False
    else:
        if gy_min > 0 or gy_max < max_grid or gx_min > 0 or gx_max < max_grid:
            return True
        else:
            xes = 0
            for y in xrange(0, max_grid):
                if 'X' in n_rows[y][0]:
                    xes += 1
                if 'X' in n_rows[y][max_grid - 1]:
                    xes += 1
            for x in xrange(1, max_grid - 1):
                if 'X' in n_rows[0][x]:
                    xes += 1
                if 'X' in n_rows[max_grid - 1][x]:
                    xes += 1
            if xes <= 0.05 * initial_xes:
                return False
            else:
                return True


def position_check(fi, si, radius):
    location = ''
    if fi - radius >= gy_min and fi + radius < gy_max and si - radius >= gx_min and si + radius < gx_max:
        location = 'clear'
    elif fi - radius < gy_min and si - radius < gx_min:
        location = 'corner top left'
    elif fi - radius < gy_min and si + radius >= gx_max:
        location = 'corner top right'
    elif fi + radius >= gy_max and si - radius < gx_min:
        location = 'corner bottom left'
    elif fi + radius >= gy_max and si + radius >= gx_max:
        location = 'corner bottom right'
    elif fi - radius < gy_min:
        location = 'edge top'
    elif si - radius < gx_min:
        location = 'edge left'
    elif si + radius >= gx_max:
        location = 'edge right'
    elif fi + radius >= gy_max:
        location = 'edge bottom'
    return location


def factor_fitness(fi, si):
    if n_rows[fi][si][2] == 1:
        fitness = factor_produce_chance + n_rows[fi][si][5]
        if fitness > rd.randint(1, 100):
            return True
        else:
            return False


def factor_check():
    for y in xrange(gy_min, gy_max):
        for x in xrange(gx_min, gx_max):
            if 'X' in n_rows[y][x] or 'E' in n_rows[y][x]:
                factor_grid[y][x] = 0
            elif 'D' not in n_rows[y][x]:
                if 'C' in n_rows[y][x]:
                    if factor_fitness(y, x):
                        n_rows[y][x][3] = 1
                        cell_radius = factor_radius + 1
                        factor_grid[y][x] = cell_radius
                        cell_radius -= 1
                        location = position_check(y, x, factor_radius)
                        if location == 'clear':
                            for Y in xrange(-cell_radius, cell_radius + 1):
                                for X in xrange(-cell_radius, cell_radius + 1):
                                    if 'X' not in n_rows[y + Y][x + X] and 'E' not in n_rows[y + Y][x + X]:
                                        if abs(Y) >= abs(X):
                                            factor_grid[y + Y][x + X] += factor_radius + 1 - abs(Y)
                                        else:
                                            factor_grid[y + Y][x + X] += factor_radius + 1 - abs(X)
                        elif location == 'edge top':
                            for Y in xrange(-y, cell_radius + 1):
                                for X in xrange(-cell_radius, cell_radius + 1):
                                    if 'X' not in n_rows[y + Y][x + X] and 'E' not in n_rows[y + Y][x + X]:
                                        if abs(Y) >= abs(X):
                                            factor_grid[y + Y][x + X] += factor_radius + 1 - abs(Y)
                                        else:
                                            factor_grid[y + Y][x + X] += factor_radius + 1 - abs(X)
                        elif location == 'edge left':
                            for Y in xrange(-cell_radius, cell_radius + 1):
                                for X in xrange(-x, cell_radius + 1):
                                    if 'X' not in n_rows[y + Y][x + X] and 'E' not in n_rows[y + Y][x + X]:
                                        if abs(Y) >= abs(X):
                                            factor_grid[y + Y][x + X] += factor_radius + 1 - abs(Y)
                                        else:
                                            factor_grid[y + Y][x + X] += factor_radius + 1 - abs(X)
                        elif location == 'edge right':
                            for Y in xrange(-cell_radius, cell_radius + 1):
                                for X in xrange(-cell_radius, gx_max - x):
                                    if 'X' not in n_rows[y + Y][x + X] and 'E' not in n_rows[y + Y][x + X]:
                                        if abs(Y) >= abs(X):
                                            factor_grid[y + Y][x + X] += factor_radius + 1 - abs(Y)
                                        else:
                                            factor_grid[y + Y][x + X] += factor_radius + 1 - abs(X)
                        elif location == 'edge bottom':
                            for Y in xrange(-cell_radius, gy_max - y):
                                for X in xrange(-cell_radius, cell_radius + 1):
                                    if 'X' not in n_rows[y + Y][x + X] and 'E' not in n_rows[y + Y][x + X]:
                                        if abs(Y) >= abs(X):
                                            factor_grid[y + Y][x + X] += factor_radius + 1 - abs(Y)
                                        else:
                                            factor_grid[y + Y][x + X] += factor_radius + 1 - abs(X)
                        elif location == 'corner top left':
                            for Y in xrange(-y, cell_radius + 1):
                                for X in xrange(-x, cell_radius + 1):
                                    if 'X' not in n_rows[y + Y][x + X] and 'E' not in n_rows[y + Y][x + X]:
                                        if abs(Y) >= abs(X):
                                            factor_grid[y + Y][x + X] += factor_radius + 1 - abs(Y)
                                        else:
                                            factor_grid[y + Y][x + X] += factor_radius + 1 - abs(X)
                        elif location == 'corner top right':
                            for Y in xrange(-y, cell_radius + 1):
                                for X in xrange(-cell_radius, gx_max - x):
                                    if 'X' not in n_rows[y + Y][x + X] and 'E' not in n_rows[y + Y][x + X]:
                                        if abs(Y) >= abs(X):
                                            factor_grid[y + Y][x + X] += factor_radius + 1 - abs(Y)
                                        else:
                                            factor_grid[y + Y][x + X] += factor_radius + 1 - abs(X)
                        elif location == 'corner bottom left':
                            for Y in xrange(-cell_radius, gy_max - y):
                                for X in xrange(-x, cell_radius + 1):
                                    if 'X' not in n_rows[y + Y][x + X] and 'E' not in n_rows[y + Y][x + X]:
                                        if abs(Y) >= abs(X):
                                            factor_grid[y + Y][x + X] += factor_radius + 1 - abs(Y)
                                        else:
                                            factor_grid[y + Y][x + X] += factor_radius + 1 - abs(X)
                        elif location == 'corner bottom right':
                            for Y in xrange(-cell_radius, gy_max - y):
                                for X in xrange(-cell_radius, gx_max - x):
                                    if 'X' not in n_rows[y + Y][x + X] and 'E' not in n_rows[y + Y][x + X]:
                                        if abs(Y) >= abs(X):
                                            factor_grid[y + Y][x + X] += factor_radius + 1 - abs(Y)
                                        else:
                                            factor_grid[y + Y][x + X] += factor_radius + 1 - abs(X)


# Death Functions
def death():
    if population_count('death'):
        for y in xrange(gy_min, gy_max):
            for x in xrange(gx_min, gx_max):
                factor_grid[y][x] = 0
                if 'E' not in n_rows[y][x]:
                    if 'X' not in n_rows[y][x]:
                        if 'D' not in n_rows[y][x]:
                            n_rows[y][x][3] = 0
                            death_rate = base_death_rate
                            if death_rate * 100 > rd.randint(1, 10000):
                                n_rows[y][x] = ['D']


# Space Functions
def soft_grid_expansion(direction, cell_info):
    global gx_min
    global gy_min
    global gx_max
    global gy_max
    y_min = cell_info[2]
    y_max = cell_info[3]
    x_min = cell_info[4]
    x_max = cell_info[5]
    expansion_type = cell_info[6]
    if direction == 'up':
        if gy_min >= 1:
            gy_min -= 1
            if expansion_type == 'f':
                center = cell_info[1]
                edge = gy_min
                for L in xrange(x_min, x_max):
                    rows[edge][center + L] = ['D']
                    n_rows[edge][center + L] = ['D']
        else:
            print('Top prevention failure')
            return
    elif direction == 'left':
        if gx_min >= 1:
            gx_min -= 1
            if expansion_type == 'f':
                center = cell_info[0]
                edge = gx_min
                for L in xrange(y_min, y_max):
                    rows[center + L][edge] = ['D']
                    n_rows[center + L][edge] = ['D']
        else:
            print('Left prevention failure')
            return
    elif direction == 'right':
        if gx_max <= max_grid - 1:
            gx_max += 1
            if expansion_type == 'f':
                center = cell_info[0]
                edge = gx_max - 1
                for L in xrange(y_min, y_max):
                    rows[center + L][edge] = ['D']
                    n_rows[center + L][edge] = ['D']
        else:
            print('Right prevention failure')
            return
    elif direction == 'down':
        if gy_max <= max_grid - 1:
            gy_max += 1
            if expansion_type == 'f':
                center = cell_info[1]
                edge = gy_max - 1
                for L in xrange(x_min, x_max):
                    rows[edge][center + L] = ['D']
                    n_rows[edge][center + L] = ['D']
        else:
            print('Bottom prevention failure')
            return


def space_check():
    # 'X' removal
    for Y in xrange(gy_min, gy_max):
        for X in xrange(gx_min, gx_max):
            if 'X' in n_rows[Y][X]:
                y_min = 0
                y_max = 0
                if -chunk_size + Y < gy_min:
                    y_min = gy_min - Y
                    y_max = chunk_size + 1
                    # print('y case 1')
                elif gy_min <= -chunk_size + Y and chunk_size + Y < gy_max:
                    y_min = -chunk_size
                    y_max = chunk_size + 1
                    # print('y case 2')
                elif chunk_size + Y >= gy_max:
                    y_min = -chunk_size
                    y_max = gy_max - Y
                    # print('y case 3')
                x_min = 0
                x_max = 0
                if -chunk_size + X < gx_min:
                    x_min = gx_min - X
                    x_max = chunk_size + 1
                    # print('x case 1')
                elif gx_min <= -chunk_size + X and chunk_size + X < gx_max:
                    x_min = -chunk_size
                    x_max = chunk_size + 1
                    # print('x case 2')
                elif chunk_size + X >= gx_max:
                    x_min = -chunk_size
                    x_max = gx_max - X
                    # print('x case 3')

                # print('Checking for X removal')
                total_factor = 0
                space_count = 0
                for y in xrange(y_min, y_max):
                    for x in xrange(x_min, x_max):
                        if 'X' in n_rows[Y + y][X + x] or 'E' in n_rows[Y + y][X + x]:
                            pass
                        else:
                            total_factor += factor_grid[Y + y][X + x]
                            space_count += 1
                # print('Total factor = ' + str(total_factor) + ', Spaces counted = ' + str(space_count))
                if total_factor > 0 and space_count > 0:
                    if total_factor / space_count >= factor_threshold_perCell:
                        n_rows[Y][X] = ['D']

    # Addition of new space
    top_cell_list = []
    if gy_min > 0:
        for X in xrange(gx_min, gx_max):
            if 'X' in n_rows[gy_min][X]:
                pass
            else:
                y_min = gy_min
                y_max = gy_min + chunk_size + 1
                x_min = 0
                x_max = 0
                if -chunk_size + X < gx_min:
                    x_min = -X
                    x_max = chunk_size + 1
                    # print('x case 1')
                elif gx_min <= -chunk_size + X and chunk_size + X < gx_max:
                    x_min = -chunk_size
                    x_max = chunk_size + 1
                    # print('x case 2')
                elif chunk_size + X >= gx_max:
                    x_min = -chunk_size
                    x_max = gx_max - X
                    # print('x case 3')
                total_factor = 0
                cell_count = 0
                space_count = 0
                for y in xrange(y_min, y_max):
                    for x in xrange(x_min, x_max):
                        if 'X' in n_rows[y][X + x] or 'E' in n_rows[y][X + x]:
                            pass
                        else:
                            total_factor += factor_grid[y][X + x]
                            space_count += 1
                            if 'D' in n_rows[y][X + x]:
                                pass
                            else:
                                cell_count += 1
                if cell_count > 0:
                    if total_factor / space_count >= factor_threshold_perCell:
                        top_cell_list.append([gy_min, X, y_min, y_max, x_min, x_max, 'f'])
                    elif cell_count * 100 / space_count >= cell_density_threshold:
                        top_cell_list.append([gy_min, X, y_min, y_max, x_min, x_max, 'c'])

    left_cell_list = []
    if gx_min > 0:
        for Y in xrange(gy_min, gy_max):
            if 'X' in n_rows[Y][gx_min]:
                pass
            else:
                y_min = 0
                y_max = 0
                x_min = gx_min
                x_max = gx_min + chunk_size + 1
                if -chunk_size + Y < gy_min:
                    y_min = -Y
                    y_max = chunk_size + 1
                    # print('y case 1')
                elif gy_min <= -chunk_size + Y and chunk_size + Y < gy_max:
                    y_min = -chunk_size
                    y_max = chunk_size + 1
                    # print('y case 2')
                elif chunk_size + Y >= gy_max:
                    y_min = -chunk_size
                    y_max = gy_max - Y
                    # print('y case 3')
                total_factor = 0
                cell_count = 0
                space_count = 0
                for y in xrange(y_min, y_max):
                    for x in xrange(x_min, x_max):
                        if 'X' in n_rows[Y + y][x] or 'E' in n_rows[Y + y][x]:
                            pass
                        else:
                            total_factor += factor_grid[Y + y][x]
                            space_count += 1
                            if 'D' in n_rows[Y + y][x]:
                                pass
                            else:
                                cell_count += 1
                if cell_count > 0:
                    if total_factor / space_count >= factor_threshold_perCell:
                        left_cell_list.append([Y, gx_min, y_min, y_max, x_min, x_max, 'f'])
                    elif cell_count * 100 / space_count >= cell_density_threshold:
                        left_cell_list.append([Y, gx_min, y_min, y_max, x_min, x_max, 'c'])

    right_cell_list = []
    if gx_max < max_grid:
        for Y in xrange(gy_min, gy_max):
            if 'X' in n_rows[Y][gx_max - 1]:
                pass
            else:
                y_min = 0
                y_max = 0
                x_min = gx_max - chunk_size - 1
                x_max = gx_max
                if -chunk_size + Y < gy_min:
                    y_min = -Y
                    y_max = chunk_size + 1
                    # print('y case 1')
                elif gy_min <= -chunk_size + Y and chunk_size + Y < gy_max:
                    y_min = -chunk_size
                    y_max = chunk_size + 1
                    # print('y case 2')
                elif chunk_size + Y >= gy_max:
                    y_min = -chunk_size
                    y_max = gy_max - Y
                    # print('y case 3')
                total_factor = 0
                cell_count = 0
                space_count = 0
                for y in xrange(y_min, y_max):
                    for x in xrange(x_min, x_max):
                        if 'X' in n_rows[Y + y][x] or 'E' in n_rows[Y + y][x]:
                            pass
                        else:
                            total_factor += factor_grid[Y + y][x]
                            space_count += 1
                            if 'D' in n_rows[Y + y][x]:
                                pass
                            else:
                                cell_count += 1
                if cell_count > 0:
                    if total_factor / space_count >= factor_threshold_perCell:
                        right_cell_list.append([Y, gx_max - 1, y_min, y_max, x_min, x_max, 'f'])
                    elif cell_count * 100 / space_count >= cell_density_threshold:
                        right_cell_list.append([Y, gx_max - 1, y_min, y_max, x_min, x_max, 'c'])

    bottom_cell_list = []
    if gy_max < max_grid:
        for X in xrange(gx_min, gx_max):
            if 'X' in n_rows[gy_max - 1][X]:
                pass
            else:
                y_min = gy_max - chunk_size - 1
                y_max = gy_max
                x_min = 0
                x_max = 0
                if -chunk_size + X < gx_min:
                    x_min = -X
                    x_max = chunk_size + 1
                    # print('x case 1')
                elif gx_min <= -chunk_size + X and chunk_size + X < gx_max:
                    x_min = -chunk_size
                    x_max = chunk_size + 1
                    # print('x case 2')
                elif chunk_size + X >= gx_max:
                    x_min = -chunk_size
                    x_max = gx_max - X
                    # print('x case 3')
                total_factor = 0
                cell_count = 0
                space_count = 0
                for y in xrange(y_min, y_max):
                    for x in xrange(x_min, x_max):
                        if 'X' in n_rows[y][X + x] or 'E' in n_rows[y][X + x]:
                            pass
                        else:
                            total_factor += factor_grid[y][X + x]
                            space_count += 1
                            if 'D' in n_rows[y][X + x]:
                                pass
                            else:
                                cell_count += 1
                if cell_count > 0:
                    if total_factor / space_count >= factor_threshold_perCell:
                        bottom_cell_list.append([gy_max - 1, X, y_min, y_max, x_min, x_max, 'f'])
                    elif cell_count * 100 / space_count >= cell_density_threshold:
                        bottom_cell_list.append([gy_max - 1, X, y_min, y_max, x_min, x_max, 'c'])

    if len(top_cell_list) > 0:
        rd.shuffle(top_cell_list)
        soft_grid_expansion('up', top_cell_list[0])
    if len(left_cell_list) > 0:
        rd.shuffle(left_cell_list)
        soft_grid_expansion('left', left_cell_list[0])
    if len(right_cell_list) > 0:
        rd.shuffle(right_cell_list)
        soft_grid_expansion('right', right_cell_list[0])
    if len(bottom_cell_list) > 0:
        rd.shuffle(bottom_cell_list)
        soft_grid_expansion('down', bottom_cell_list[0])


# Executing divisions over time
b_list = []
p_list = []
e_list = []

"""
muller array clone indexing
[0, 1, '2', '3', 4, 5, 6, 7, [8, ...]]
[0]----Clone ID
[1]----Phenotype ID
[2]----Clone type
[3]----Phenotype
[4]----Selfish drivers
[5]----Cooperative drivers
[6]----Passengers
[7]----Fitness
[8]----Population List
"""
for r in xrange(initial, executions + initial):
    index_r = r - initial

    population_stats = [[int(initial_cells ** 0.5) ** 2], [0], ['G']]

    muller_array = [[0, -12 + 110, 'original', 'N', 0, 0, 0, 50.00, [int(initial_cells ** 0.5) ** 2]]]
    ancestor_list = []

    max_population = 0
    selfish_bins = []
    cooperator_bins = []
    for b in xrange(0, bin_number):
        selfish_bins.append([0])
        cooperator_bins.append([0])
    b_list.append(25)
    p_list.append(0)
    e_list.append(0)

    # Spatial Graphics
    if 1 == 1:
        for y in xrange(0, max_grid):
            for x in xrange(0, max_grid):
                if 'E' in n_rows[y][x] or 'D' in n_rows[y][x]:
                    data_rows[y][x] = -110 + 110
                elif 'X' in n_rows[y][x]:
                    data_rows[y][x] = 100 + 110
                else:
                    if n_rows[y][x][2] == 0:
                        cell_bin = bin_sorter(y, x)
                        selfish_bins[cell_bin][0] += 1
                        dat_range = bin_number / bin_number
                        if n_rows[y][x][0] == 'N' and cell_bin == 49:
                            data_rows[y][x] = -12 + 110
                        else:
                            data_rows[y][x] = 20 - cell_bin * dat_range + 110
                    elif n_rows[y][x][2] == 1:
                        cell_bin = bin_sorter(y, x)
                        cooperator_bins[cell_bin][0] += 1
                        dat_range = bin_number / bin_number
                        data_rows[y][x] = -20 + cell_bin * dat_range + 110
        if time_skip <= gens:
            Space = np.array(data_rows)
            size = np.array(Space.shape) * gsize
            dpi = 72.0
            figsize = size[1] / float(dpi), size[0] / float(dpi)
            fig = plt.figure(figsize=figsize, dpi=dpi, facecolor="white")
            fig.add_axes([0.0, 0.0, 1.0, 1.0], frameon=False)
            plt.imshow(Space, interpolation='nearest', cmap=plt.cm.nipy_spectral_r, vmin=-110 + 110,
                       vmax=100 + 110)
            plt.xticks([]), plt.yticks([])
            plt.title('t=0')
            plt.savefig(image_file_name + str(r) + '_frame_0.png')
            plt.close('all')

    for t in xrange(1, gens + 1):
        #print('t = ' + str(t))
        t_counter += 1
        current_population = 0
        #print('Starting Divisions')
        divide(t)
        phenotype_switch()
        #print('Divisions Done')
        #print('')
        #print('Starting Deaths')
        death()
        #print('Deaths Done')
        #print('')
        #print('Starting Optimal Check')
        if x_checker():
            #print('Optimal Check Done')
            #print('')
            #print('Starting Factor')
            factor_check()
            #print('Factor Done')
            #print('')
            #print('Starting Space')
            space_check()
            #print('Space Done')
            #print('')


        #print('Starting Renewal')
        for c in xrange(0, len(muller_array)):
            muller_array[c][8].append(0)
        for b in xrange(0, bin_number):
            selfish_bins[b].append(0)
            cooperator_bins[b].append(0)
        for y in xrange(gy_min, gy_max):
            # print(n_rows[y])
            for x in xrange(gx_min, gx_max):
                rows[y][x] = n_rows[y][x]
        b_cells = 0
        p_cells = 0
        e_cells = 0

        #print('Renewal Done')
        #print('')

        #print('Starting Bin Sorting')
        # Spatial Graphics
        if 1 == 1:
            for y in xrange(gy_min, gy_max):
                for x in xrange(gx_min, gx_max):
                    if 'E' in n_rows[y][x] or 'D' in n_rows[y][x]:
                        data_rows[y][x] = -110 + 110
                    elif 'X' in n_rows[y][x]:
                        data_rows[y][x] = 100 + 110
                    else:
                        rows[y][x][3] = 0
                        n_rows[y][x][3] = 0
                        current_population += 1
                        if 'N' in n_rows[y][x]:
                            b_cells += 1
                        if 'S' in n_rows[y][x]:
                            p_cells += 1
                        if 'C' in n_rows[y][x]:
                            e_cells += 1
                        if muller == 'on':
                            muller_array[n_rows[y][x][7]][8][t] += 1
                        if n_rows[y][x][2] == 0:
                            cell_bin = bin_sorter(y, x)
                            selfish_bins[cell_bin][t] += 1
                            dat_range = bin_number / bin_number
                            if n_rows[y][x][0] == 'N' and cell_bin == 49:
                                data_rows[y][x] = -12 + 110
                            else:
                                if cell_bin <= 100:
                                    data_rows[y][x] = 20 - cell_bin * dat_range + 110
                                else:
                                    data_rows[y][x] = 30
                        elif n_rows[y][x][2] == 1:
                            cell_bin = bin_sorter(y, x)
                            cooperator_bins[cell_bin][t] += 1
                            dat_range = bin_number / bin_number
                            data_rows[y][x] = -20 + cell_bin * dat_range + 110
                    factor_grid[y][x] = factor_grid[y][x] * 8
                    if factor_grid[y][x] != 0:
                        factor_grid[y][x] += 8
            #print('Bin Sorting Done')
            #print('')
            if t_counter >= time_skip:
                #print('Starting Spatial Imaging')
                Space = np.array(data_rows)
                size = np.array(Space.shape) * gsize
                dpi = 72.0
                figsize = size[1] / float(dpi), size[0] / float(dpi)
                fig = plt.figure(figsize=figsize, dpi=dpi, facecolor="white")
                fig.add_axes([0.0, 0.0, 1.0, 1.0], frameon=False)
                plt.imshow(Space, interpolation='nearest', cmap=plt.cm.nipy_spectral_r, vmin=-110 + 110,
                           vmax=100 + 110)
                plt.xticks([]), plt.yticks([])
                plt.title('t=' + str(t))
                plt.savefig(image_file_name + str(r) + '_frame_' + str(t) + '.png')
                plt.close('all')
                #print('Spatial Imaging Done')
                #print('')
        # Factor Density
        if t_counter >= time_skip and factor_graphics == 'on':
            #print('Starting Factor Imaging')
            Space_factor = np.array(factor_grid)
            size = np.array(Space_factor.shape) * gsize
            dpi = 72.0
            figsize = size[1] / float(dpi), size[0] / float(dpi)
            fig = plt.figure(figsize=figsize, dpi=dpi, facecolor="white")
            fig.add_axes([0.0, 0.0, 1.0, 1.0], frameon=False)
            plt.imshow(Space_factor, interpolation='nearest', cmap=plt.cm.afmhot, vmin=0, vmax=max_color * 4)
            plt.xticks([]), plt.yticks([])
            plt.title('t=' + str(t))
            plt.savefig(image_file_name + str(r) + '_factor_frame_' + str(t) + '.png')
            plt.close('all')
            #print('Factor Imaging Done')
            #print('')

        if t_counter >= time_skip:
            t_counter = 0
        #print('Starting Stat Collection')

        population_stats[0].append(current_population)
        population_stats[1].append(e_cells)
        max_population = muller_resolution(max_population, current_population)
        b_list.append(b_cells)
        p_list.append(p_cells)
        e_list.append(e_cells)
        #print('Stat Collection Done')
        #print('')
        #print('')
        #print('')

    h_stats = open("A_" + file_name + str(r) + file_type, "a")
    line_holder = 'Tumor ' + str(r) + ' Stats'
    h_stats.write(line_holder)
    h_stats.write("\n")
    line_holder = 'Domain Size,' + str(initial_grid)
    h_stats.write(line_holder)
    h_stats.write("\n")
    line_holder = 'Divisions,' + str(division_counter)
    h_stats.write(line_holder)
    h_stats.write("\n")
    line_holder = 'Drivers,' + str(driver_counter)
    h_stats.write(line_holder)
    h_stats.write("\n")
    line_holder = 'Passengers,' + str(passenger_counter)
    h_stats.write(line_holder)
    h_stats.write("\n")
    line_holder = 'Total Mutations,' + str(driver_counter + passenger_counter)
    h_stats.write(line_holder)
    h_stats.write("\n")
    line_holder = 'Predicted Mutations,' + str(int(division_counter * ((passenger_rate + driver_rate) / 100)))
    h_stats.write(line_holder)
    h_stats.write("\n")

    for p in xrange(0, 2):
        line_holder = ''
        if p == 0:
            line_holder = 'Total Cell Pop'
        if p == 1:
            line_holder = 'Cooperator Pop'
        for t in xrange(0, len(population_stats[p])):
            line_holder += ',' + str(population_stats[p][t])
        h_stats.write(line_holder)
        h_stats.write("\n")

    heterogeneity = [[0], [1], [0]]
    s_clone_populations = []
    c_clone_populations = []
    for b in xrange(0, bin_number):
        s_clone_populations.append(0)
        c_clone_populations.append(0)
    for t in xrange(1, gens + 1):
        heterogeneity[0].append(0)
        heterogeneity[1].append(0)
        heterogeneity[2].append(0)
        richness = 0
        total_pop = population_stats[0][t]
        s_b_list = []
        c_b_list = []
        for b in xrange(0, bin_number):
            s_clone_populations[b] = selfish_bins[b][t] / float(total_pop)
            c_clone_populations[b] = cooperator_bins[b][t] / float(total_pop)
            if s_clone_populations[b] > 0:
                richness += 1
                s_b_list.append(s_clone_populations[b])
            if c_clone_populations[b] > 0:
                richness += 1
                c_b_list.append(c_clone_populations[b])
        heterogeneity[1][t] = richness
        if len(s_b_list) > 0:
            for b in xrange(0, len(s_b_list)):
                s_b_list[b] = s_b_list[b] * math.log(s_b_list[b])
        if len(c_b_list) > 0:
            for b in xrange(0, len(c_b_list)):
                c_b_list[b] = c_b_list[b] * math.log(c_b_list[b])
        if richness > 1:
            heterogeneity[0][t] = -1 * (math.fsum(s_b_list) + math.fsum(c_b_list))
            heterogeneity[2][t] = heterogeneity[0][t] / math.log(heterogeneity[1][t])
    for s in xrange(0, 3):
        line_holder = ''
        if s == 0:
            line_holder = 'Shannon Index'
        if s == 1:
            line_holder = 'Richness'
        if s == 2:
            line_holder = 'Equitability'
        for t in xrange(0, gens + 1):
            line_holder += ',' + str(heterogeneity[s][t])
        h_stats.write(line_holder)
        h_stats.write("\n")
    h_stats.close()

    if muller == 'on':
        m_stats = open("A_" + muller_file_name + str(r) + file_type, "a")
        line_holder = str(population_stats[0][0])
        for t in xrange(1, gens + 1):
            line_holder += ',' + str(population_stats[0][t])
        m_stats.write(line_holder)
        m_stats.write("\n")
        for p in xrange(0, 3):
            line_holder = str(ancestor_list[0][p])
            for a in xrange(1, len(ancestor_list)):
                line_holder += ',' + str(ancestor_list[a][p])
            m_stats.write(line_holder)
            m_stats.write("\n")
        for c in xrange(0, len(muller_array)):
            line_holder = str(muller_array[c][0])
            for h in range(1, 8):
                line_holder += ',' + str(muller_array[c][h])
            for t in xrange(0, gens + 1):
                line_holder += ',' + str(muller_array[c][8][t])
            m_stats.write(line_holder)
            m_stats.write("\n")
        m_stats.close()

    s_stats = open("A_" + plot_name + str(r) + file_type, "a")
    line_holder = 'Tumor ' + str(r)
    if population_stats[0][gens] > initial_grid ** 2:
        line_holder += ',Valid'
    else:
        line_holder += ',Null'
    for t in range(0, gens + 1):
        line_holder += ',' + str(heterogeneity[0][t])
    s_stats.write(line_holder)
    s_stats.write("\n")
    s_stats.close()

    shannon_index = [0]
    for t in range(0, gens + 1):
        shannon_index.append(0)
        unique = 0
        total_pop = population_stats[0][t]
        current_clones = []
        for c in range(0, len(muller_array)):
            if muller_array[c][8][t] > 0:
                unique += 1
                sum_element = muller_array[c][8][t] / float(total_pop)
                current_clones.append(sum_element * math.log(sum_element))
        if unique > 1:
            shannon_index[t] = -1 * math.fsum(current_clones)

    g_stats = open('A_G' + plot_name + str(r) + file_type, "a")
    line_holder = 'Tumor ' + str(r)
    if population_stats[0][gens] > initial_grid ** 2:
        line_holder += ',Valid'
    else:
        line_holder += ',Null'
    for t in range(0, gens + 1):
        line_holder += ',' + str(shannon_index[t])
    g_stats.write(line_holder)
    g_stats.close()

    p_stats = open("Phenotypes_" + file_name + str(r) + file_type, "a")
    line_holder = 'parents,clones'
    b_holder = '0,0'
    p_holder = '0,1'
    e_holder = '0,2'
    for t in range(0, gens + 1):
        line_holder += ',' + str(t)
        b_holder += ',' + str(b_list[t])
        p_holder += ',' + str(p_list[t])
        e_holder += ',' + str(e_list[t])
    p_stats.write(line_holder)
    p_stats.write("\n")
    p_stats.write(b_holder)
    p_stats.write("\n")
    p_stats.write(p_holder)
    p_stats.write("\n")
    p_stats.write(e_holder)
    p_stats.write("\n")
    p_stats.close()

    stats = open("Stat_analysis" + file_name + str(r) + file_type, "a")
    stats.write('Average, t=250, t=750, t=1500, t=2500')
    stats.write("\n")
    averages = np.average(shannon_index)
    stats.write(str(averages) + ',' + str(shannon_index[250]) + ',' + str(shannon_index[750]) + ',' + str(shannon_index[1500]) + ',' + str(shannon_index[gens]))
    stats.write("\n")
    averages = np.average(heterogeneity[0])
    stats.write(str(averages) + ',' + str(heterogeneity[0][250]) + ',' + str(heterogeneity[0][750]) + ',' + str(heterogeneity[0][1500]) + ',' + str(heterogeneity[0][gens]))
    stats.write("\n")
    stats.close()

    '''
    f_stats = open("A_Frequencies_" + file_name + str(r) + file_type, "a")
    clone_frequencies = []
    total_pop = population_stats[0][gens]
    extinct_clones = 0
    for c in xrange(0, len(muller_array)):
        if muller_array[c][8][gens] == 0:
            extinct_clones += 1
        else:
            freq = float(muller_array[c][8][gens])/total_pop
            clone_frequencies.append(freq)
    output_freq_table = [[], []]
    finest_resolution = 0.000001
    freq_values = [0]
    for q in range(1, 100):
        freq_values.append(finest_resolution * q)
    for q in range(0, 100):
        freq_values.append(finest_resolution * 100 + (q * finest_resolution * 10))
    for q in range(0, 100):
        freq_values.append(finest_resolution * 1000 + (q * finest_resolution * 100))
    for q in range(0, 10):
        freq_values.append(finest_resolution * 10000 + (q * finest_resolution * 10000))
    for q in range(0, 10):
        freq_values.append(0.1 + 0.1 * q)
    table_elements = len(freq_values)
    for k in xrange(0, table_elements):
        output_freq_table[0].append(freq_values[k])
        clone_num = 0
        if k == table_elements - 1:
            for c in xrange(0, len(clone_frequencies)):
                if clone_frequencies[c] >= freq_values[k]:
                    clone_num += 1
        else:
            for c in xrange(0, len(clone_frequencies)):
                if clone_frequencies[c] >= freq_values[k] and clone_frequencies[c] < freq_values[k + 1]:
                    clone_num += 1
        output_freq_table[1].append(clone_num)
    line_holder_a = str(output_freq_table[0][0])
    line_holder_b = str(output_freq_table[1][0])
    for k in xrange(1, table_elements):
        line_holder_a += ',' + str(output_freq_table[0][k])
        line_holder_b += ',' + str(output_freq_table[1][k])
    f_stats.write(line_holder_a)
    f_stats.write("\n")
    f_stats.write(line_holder_b)
    f_stats.write("\n")
    line_holder = str(len(clone_frequencies)) + ',' + str(extinct_clones) + ',' + str(len(clone_frequencies) + extinct_clones)
    f_stats.write(line_holder)
    f_stats.close()
    '''


    # Parameter Re-establishment
    g_start = initial_grid
    switch = 'on'
    max_grid = 601
    passenger_rate = 0.5
    driver_rate = 0.07
    selfish_bias = 0  # the amount favoring mutating selfish vs cooperative
    base_fitness = 50  # in percent
    selfish_driver_min = 0
    selfish_driver_max = 0
    cooperator_driver_min = 0
    cooperator_driver_max = 0
    if impact == 'low':
        selfish_driver_min = 2.5
        selfish_driver_max = 7.5
        cooperator_driver_min = 2.5
        cooperator_driver_max = 7.5
    elif impact == 'reg':
        selfish_driver_min = 10.5
        selfish_driver_max = 20
        cooperator_driver_min = 10.5
        cooperator_driver_max = 20
    switching_punishment = 1
    switching_penalty = 10  # in percent
    passenger_mod_range = 0.05  # in percent
    mod_resolution = 0.001  # in percent
    bin_number = 100
    factor_produce_chance = 40  # in percent
    base_death_rate = 15  # in percent
    s_penalty = 0  # in percent
    c_penalty = 0
    factor_radius = 2
    factor_threshold_perCell = 10
    cell_density_threshold = 80  # in percent
    chunk_size = 1
    membrane_thickness = initial_membrane - 1
    membrane_gap = initial_grid - 1
    gx_min = max_grid / 2 - g_start / 2 - 1
    gy_min = max_grid / 2 - g_start / 2 - 1
    gx_max = max_grid / 2 + g_start / 2 + 2
    gy_max = max_grid / 2 + g_start / 2 + 2
    if g_start == max_grid:
        gx_min = 0
        gy_min = 0
        gx_max = max_grid
        gy_max = max_grid
    rows = []
    n_rows = []
    data_rows = np.zeros((max_grid, max_grid))
    factor_grid = np.zeros((max_grid, max_grid))
    gsize = 2
    m_y = 2000
    scaling = 3
    m_x = gens * scaling
    division_counter = 0
    passenger_counter = 0
    driver_counter = 0
    clone_ID_counter = 0

    if factor_graphics == 'on':
        max_color = factor_radius + 1
        for f in range(1, factor_radius + 1):
            max_color += (factor_radius + 1 - f) * (2 * f + 1) ** 2 - 1

    if g_start == 25:
        frame_shift_g = membrane_gap + 1
        frame_shift_m = membrane_thickness / 3 - 1
    if g_start == 51:
        frame_shift_g = membrane_gap / 2 + membrane_thickness / 2 + 1
        frame_shift_m = 0
    if g_start == 101:
        frame_shift_g = 4 * membrane_gap / 5 + membrane_thickness / 2 - 1
        frame_shift_m = 0
    if g_start == 301:
        frame_shift_g = membrane_gap / 2 + membrane_thickness
        frame_shift_m = 0
    if g_start == 601:
        frame_shift_g = 0
        frame_shift_m = 0
    membrane_counter_x = frame_shift_m
    gap_counter_x = frame_shift_g
    membrane_counter_y = frame_shift_m
    gap_counter_y = frame_shift_g
    t_counter = 0
    initial_xes = 0

    # print('Starting array')
    # Array Establishment
    for y in xrange(0, max_grid):
        rows.append([])
        n_rows.append([])
        for x in xrange(0, max_grid):
            rows[y].append(['E'])
            n_rows[y].append(['E'])
    for y in xrange(0, max_grid):
        for x in xrange(0, max_grid):
            if gap_counter_x <= membrane_gap:
                gap_counter_x += 1
            elif membrane_counter_x <= membrane_thickness:
                rows[y][x] = ['X']
                n_rows[y][x] = ['X']
                if y == 0 or y == max_grid - 1 or x == 0 or x == max_grid - 1:
                    initial_xes += 1
                membrane_counter_x += 1
            else:
                gap_counter_x = 1
                membrane_counter_x = 0
        gap_counter_x = frame_shift_g
        membrane_counter_x = frame_shift_m
    for x in xrange(0, max_grid):
        for y in xrange(0, max_grid):
            if gap_counter_y <= membrane_gap:
                gap_counter_y += 1
            elif membrane_counter_y <= membrane_thickness:
                rows[y][x] = ['X']
                n_rows[y][x] = ['X']
                if y == 0 or y == max_grid - 1 or x == 0 or x == max_grid - 1:
                    initial_xes += 1
                membrane_counter_y += 1
            else:
                gap_counter_y = 1
                membrane_counter_y = 0
        gap_counter_y = frame_shift_g
        membrane_counter_y = frame_shift_m
    side_len = int(initial_cells ** 0.5)
    for y in xrange(side_len / 2 - side_len + 1, side_len / 2 + 1):
        for x in xrange(side_len / 2 - side_len + 1, side_len / 2 + 1):
            rows[max_grid // 2 + y][max_grid // 2 + x] = ['N', [0, 0], 0, 0, 0, 0, 0, 0, -12 + 110, 0]
            n_rows[max_grid // 2 + y][max_grid // 2 + x] = ['N', [0, 0], 0, 0, 0, 0, 0, 0, -12 + 110, 0]

"""
    def factor_calc():
    for Y in range(gy_min, gy_min + factor_radius):
        for X in range(gx_min, gx_min + factor_radius):
            factor_grid[Y][X] = 0
            if 'X' not in n_rows[Y][X]:
                up_radius = -Y
                left_radius = -X
                right_radius = factor_radius
                down_radius = factor_radius
                for y in range(up_radius, down_radius + 1):
                    for x in range(left_radius, right_radius + 1):
                        if 'E' not in n_rows[y + Y][x + X] and 'X' not in n_rows[y + Y][x + X]:
                            if n_rows[y + Y][x + X][3] == 1:
                                if abs(y) >= abs(x):
                                    factor_grid[Y][X] += factor_radius + 1 - abs(y)
                                else:
                                    factor_grid[Y][X] += factor_radius + 1 - abs(x)
        for X in range(gx_min + factor_radius, gx_max - factor_radius):
            factor_grid[Y][X] = 0
            if 'X' not in n_rows[Y][X]:
                up_radius = -Y
                left_radius = -factor_radius
                right_radius = factor_radius
                down_radius = factor_radius
                for y in range(up_radius, down_radius + 1):
                    for x in range(left_radius, right_radius + 1):
                        if 'E' not in n_rows[y + Y][x + X] and 'X' not in n_rows[y + Y][x + X]:
                            if n_rows[y + Y][x + X][3] == 1:
                                if abs(y) >= abs(x):
                                    factor_grid[Y][X] += factor_radius + 1 - abs(y)
                                else:
                                    factor_grid[Y][X] += factor_radius + 1 - abs(x)
        for X in range(gx_max - factor_radius, gx_max):
            factor_grid[Y][X] = 0
            if 'X' not in n_rows[Y][X]:
                up_radius = -Y
                left_radius = -factor_radius
                right_radius = gx_max - X
                down_radius = factor_radius
                for y in range(up_radius, down_radius + 1):
                    for x in range(left_radius, right_radius):
                        if 'E' not in n_rows[y + Y][x + X] and 'X' not in n_rows[y + Y][x + X]:
                            if n_rows[y + Y][x + X][3] == 1:
                                if abs(y) >= abs(x):
                                    factor_grid[Y][X] += factor_radius + 1 - abs(y)
                                else:
                                    factor_grid[Y][X] += factor_radius + 1 - abs(x)
    for Y in range(gy_min + factor_radius, gy_max - factor_radius):
        for X in range(gx_min, gx_min + factor_radius):
            factor_grid[Y][X] = 0
            if 'X' not in n_rows[Y][X]:
                up_radius = -factor_radius
                left_radius = -X
                right_radius = factor_radius
                down_radius = factor_radius
                for y in range(up_radius, down_radius + 1):
                    for x in range(left_radius, right_radius + 1):
                        if 'E' not in n_rows[y + Y][x + X] and 'X' not in n_rows[y + Y][x + X]:
                            if n_rows[y + Y][x + X][3] == 1:
                                if abs(y) >= abs(x):
                                    factor_grid[Y][X] += factor_radius + 1 - abs(y)
                                else:
                                    factor_grid[Y][X] += factor_radius + 1 - abs(x)
        for X in range(gx_min + factor_radius, gx_max - factor_radius):
            factor_grid[Y][X] = 0
            if 'X' not in n_rows[Y][X]:
                up_radius = -factor_radius
                left_radius = -factor_radius
                right_radius = factor_radius
                down_radius = factor_radius
                for y in range(up_radius, down_radius + 1):
                    for x in range(left_radius, right_radius + 1):
                        if 'E' not in n_rows[y + Y][x + X] and 'X' not in n_rows[y + Y][x + X]:
                            if n_rows[y + Y][x + X][3] == 1:
                                if abs(y) >= abs(x):
                                    factor_grid[Y][X] += factor_radius + 1 - abs(y)
                                else:
                                    factor_grid[Y][X] += factor_radius + 1 - abs(x)
        for X in range(gx_max - factor_radius, gx_max):
            factor_grid[Y][X] = 0
            if 'X' not in n_rows[Y][X]:
                up_radius = -factor_radius
                left_radius = -factor_radius
                right_radius = gx_max - X
                down_radius = factor_radius
                for y in range(up_radius, down_radius + 1):
                    for x in range(left_radius, right_radius):
                        if 'E' not in n_rows[y + Y][x + X] and 'X' not in n_rows[y + Y][x + X]:
                            if n_rows[y + Y][x + X][3] == 1:
                                if abs(y) >= abs(x):
                                    factor_grid[Y][X] += factor_radius + 1 - abs(y)
                                else:
                                    factor_grid[Y][X] += factor_radius + 1 - abs(x)
    for Y in range(gy_max - factor_radius, gy_max):
        for X in range(gx_min, gx_min + factor_radius):
            factor_grid[Y][X] = 0
            if 'X' not in n_rows[Y][X]:
                up_radius = -factor_radius
                left_radius = -X
                right_radius = factor_radius
                down_radius = gy_max - Y
                for y in range(up_radius, down_radius):
                    for x in range(left_radius, right_radius + 1):
                        if 'E' not in n_rows[y + Y][x + X] and 'X' not in n_rows[y + Y][x + X]:
                            if n_rows[y + Y][x + X][3] == 1:
                                if abs(y) >= abs(x):
                                    factor_grid[Y][X] += factor_radius + 1 - abs(y)
                                else:
                                    factor_grid[Y][X] += factor_radius + 1 - abs(x)
        for X in range(gx_min + factor_radius, gx_max - factor_radius):
            factor_grid[Y][X] = 0
            if 'X' not in n_rows[Y][X]:
                up_radius = -factor_radius
                left_radius = -factor_radius
                right_radius = factor_radius
                down_radius = gy_max - Y
                for y in range(up_radius, down_radius):
                    for x in range(left_radius, right_radius + 1):
                        if 'E' not in n_rows[y + Y][x + X] and 'X' not in n_rows[y + Y][x + X]:
                            if n_rows[y + Y][x + X][3] == 1:
                                if abs(y) >= abs(x):
                                    factor_grid[Y][X] += factor_radius + 1 - abs(y)
                                else:
                                    factor_grid[Y][X] += factor_radius + 1 - abs(x)
        for X in range(gx_max - factor_radius, gx_max):
            factor_grid[Y][X] = 0
            if 'X' not in n_rows[Y][X]:
                up_radius = -factor_radius
                left_radius = -factor_radius
                right_radius = gx_max - X
                down_radius = gy_max - Y
                for y in range(up_radius, down_radius):
                    for x in range(left_radius, right_radius):
                        if 'E' not in n_rows[y + Y][x + X] and 'X' not in n_rows[y + Y][x + X]:
                            if n_rows[y + Y][x + X][3] == 1:
                                if abs(y) >= abs(x):
                                    factor_grid[Y][X] += factor_radius + 1 - abs(y)
                                else:
                                    factor_grid[Y][X] += factor_radius + 1 - abs(x)

    
    
    g_start = initial_grid
    max_grid = 600
    gens = 50
    passenger_rate = 0.5
    driver_rate = 0.07
    selfish_bias = 0  # the amount favoring mutating selfish vs cooperative
    base_fitness = 50  # in percent
    selfish_driver_min = 10  # in percent
    selfish_driver_max = 20.5  # in percent
    cooperator_driver_min = 10  # in percent----
    cooperator_driver_max = 20.5  # in percent----
    switching_punishment = 1
    switching_penalty = 10  # in percent
    passenger_mod_range = 0.5  # in percent
    mod_resolution = 0.01  # in percent
    bin_number = 100
    factor_produce_chance = 40  # in percent
    base_death_rate = 15  # in percent
    s_penalty = 0  # in percent
    c_penalty = 0
    factor_radius = 2
    factor_threshold_perCell = 10
    cell_density_threshold = 80  # in percent
    chunk_size = 1
    membrane_thickness = initial_membrane - 1
    membrane_gap = initial_grid - 1
    gx_min = max_grid / 2 - g_start / 2 - 1
    gy_min = max_grid / 2 - g_start / 2 - 1
    gx_max = max_grid / 2 + g_start / 2 + 2
    gy_max = max_grid / 2 + g_start / 2 + 2
    rows = []
    n_rows = []
    data_rows = np.zeros((max_grid, max_grid))
    factor_grid = np.zeros((max_grid, max_grid))
    gsize = 1
    m_y = 2000
    scaling = 3
    m_x = gens * scaling
    division_counter = 0
    mutation_counter = 0
    driver_counter = 0

    tiles = max_grid / float(membrane_thickness + membrane_gap + 2)
    if tiles != int(tiles):
        tiles += 1
    tiles = int(tiles)
    if tiles / 2 == tiles / float(2):
        frame_shift_g = membrane_gap / 2 + membrane_thickness / 2 + 1
        frame_shift_m = 0
    else:
        frame_shift_g = membrane_gap + 1
        frame_shift_m = membrane_thickness / 2
    if g_start == 101:
        frame_shift_g = 2 * membrane_gap / 3 + membrane_thickness / 2
        frame_shift_m = 0
    membrane_counter_x = frame_shift_m
    gap_counter_x = frame_shift_g
    membrane_counter_y = frame_shift_m
    gap_counter_y = frame_shift_g

    # print('Starting array')
    # Array Establishment
    for y in range(0, max_grid):
        rows.append([])
        n_rows.append([])
        for x in range(0, max_grid):
            rows[y].append(['E'])
            n_rows[y].append(['E'])
    for y in range(0, max_grid):
        for x in range(0, max_grid):
            if gap_counter_x <= membrane_gap:
                gap_counter_x += 1
            elif membrane_counter_x <= membrane_thickness:
                rows[y][x] = ['X']
                n_rows[y][x] = ['X']
                membrane_counter_x += 1
            else:
                gap_counter_x = 1
                membrane_counter_x = 0
        gap_counter_x = frame_shift_g
        membrane_counter_x = frame_shift_m
    for x in range(0, max_grid):
        for y in range(0, max_grid):
            if gap_counter_y <= membrane_gap:
                gap_counter_y += 1
            elif membrane_counter_y <= membrane_thickness:
                rows[y][x] = ['X']
                n_rows[y][x] = ['X']
                membrane_counter_y += 1
            else:
                gap_counter_y = 1
                membrane_counter_y = 0
        gap_counter_y = frame_shift_g
        membrane_counter_y = frame_shift_m
    side_len = int(initial_cells ** 0.5)
    for y in range(side_len / 2 - side_len + 1, side_len / 2 + 1):
        for x in range(side_len / 2 - side_len + 1, side_len / 2 + 1):
            rows[max_grid // 2 + y][max_grid // 2 + x] = ['N', [0, 0], 0, 0, 0, 0, 0]
            n_rows[max_grid // 2 + y][max_grid // 2 + x] = ['N', [0, 0], 0, 0, 0, 0, 0]
            
    
    m_stats = open(muller_file_name, "a")
    m_stats.write("Muller Plot Data")
    m_stats.write("\n")
    m_stats.write("Population List Start")
    m_stats.write("\n")
    for t in range(0, gens + 1):
        m_stats.write(str(population_stats[0][t]))
        m_stats.write("\n")
    m_stats.write("Population List End")
    m_stats.write("\n")
    m_stats.write("\n")

    m_stats.write("Ancestor List Start")
    m_stats.write("\n")
    for a in range(0, len(ancestor_list)):
        for q in range(0, 3):
            m_stats.write(str(ancestor_list[a][q]))
            m_stats.write("\n")
    m_stats.write("Ancestor List End")
    m_stats.write("\n")
    m_stats.write("\n")

    m_stats.write("Muller Array Start")
    m_stats.write("\n")
    for m in range(0, len(muller_array)):
        m_stats.write(str(muller_array[m][0]))
        m_stats.write("\n")
        m_stats.write(str(muller_array[m][1]))
        m_stats.write("\n")
        for t in range(0, gens + 1):
            m_stats.write(str(muller_array[m][2][t]))
            m_stats.write("\n")
    m_stats.write("Muller Array End")
    m_stats.write("\n")
    m_stats.close()

    total_pop = population_stats[0][gens]
    c_pop = population_stats[1][gens]
    cooperator_list[index_r].append(total_pop)
    if c_pop > 0:
        cooperator_list[index_r].append(c_pop / float(total_pop))
        cooperator_list[index_r].append(c_pop)
    else:
        cooperator_list[index_r].append(0)
        cooperator_list[index_r].append(0)
    if total_pop <= initial_grid ** 2 + initial_grid:
        cooperator_list[index_r].append('Null')
    else:
        cooperator_list[index_r].append('Valid')
"""

"""
        border_delay += 15
        if r == 20:
            seeding_grid_low_y = grid_size_y // 3 + 1
            seeding_grid_high_y = 2 * grid_size_y // 3
            seeding_grid_low_x = grid_size_x // 3 + 1
            seeding_grid_high_x = 2 * grid_size_x // 3
            expansion_size = 30
        if r == 30:
            expansion_size = 15
            seeding_grid_low = 25
            seeding_grid_high_y = grid_size_y - 24
            seeding_grid_high_x = grid_size_x - 24
        gsize = 450 / ((grid_size_y + grid_size_x)/2)
        expansions = 0
        rows = []
        n_rows = []
        for y in range(0, grid_size_y):
            rows.append([])
            n_rows.append([])
            for x in range(0, grid_size_x):
                rows[y].append(['E'])
                n_rows[y].append(['E'])
        for y in range(seeding_grid_low_y, seeding_grid_high_y):
            for x in range(seeding_grid_low_x, seeding_grid_high_x):
                rows[y][x] = ['H', rd.randint(0, lifespan - 2), 0, [[0, 0]], []]
                n_rows[y][x] = ['H', rd.randint(0, lifespan - 2), 0, [[0, 0]], []]
        data_rows = np.zeros((grid_size_y, grid_size_x))

    print(str(l) + ' executions completed')


    # Legends
    count = 1
    grid_size = (mutation_number + 2) * 4
    data_rows = np.zeros((grid_size, grid_size))
    for y in range(0, grid_size):
        for x in range(0, grid_size):
            data_rows[y][x] = count
        if count < mutation_number + 2 and (y + 1) // 4 == (y + 1)/ 4:
            count += 1

    Space = np.array(data_rows)
    size = np.array(Space.shape) * gsize
    dpi = 72.0
    figsize = size[1] / float(dpi), size[0] / float(dpi)
    fig = plt.figure(figsize=figsize, dpi=dpi, facecolor="white")
    fig.add_axes([0.0, 0.0, 1.0, 1.0], frameon=False)
    plt.imshow(Space, interpolation='nearest', cmap=plt.cm.nipy_spectral_r, vmin=1, vmax=mutation_number + 2)
    plt.xticks([]), plt.yticks([])
    plt.title('Legend')
    plt.savefig(file_name + 'Mutation Tracking Key.png')
    plt.close('all')

    P_cells_1 = 0
    A_cells_1 = 0
    I_cells_1 = 0
    for y in range(0, grid_size):
        for x in range(0, grid_size):
            if 'M' in n_rows[y][x] and len(n_rows[y][x]) <= 3:
                pass
            elif 'E' in n_rows[y][x]:
                pass
            elif 'P1' in n_rows[y][x][3]:
                P_cells_1 += 1
            elif 'P2' in n_rows[y][x][3]:
                P_cells_1 += 1
            elif 'P3' in n_rows[y][x][3]:
                P_cells_1 += 1
            elif 'P4' in n_rows[y][x][3]:
                P_cells_1 += 1
            elif 'P5' in n_rows[y][x][3]:
                P_cells_1 += 1
            elif 'A1' in n_rows[y][x][3]:
                A_cells_1 += 1
            elif 'A2' in n_rows[y][x][3]:
                A_cells_1 += 1
            elif 'A3' in n_rows[y][x][3]:
                A_cells_1 += 1
            elif 'A4' in n_rows[y][x][3]:
                A_cells_1 += 1
            elif 'A5' in n_rows[y][x][3]:
                A_cells_1 += 1
            elif 'I1' in n_rows[y][x][3]:
                I_cells_1 += 1
            elif 'I2' in n_rows[y][x][3]:
                I_cells_1 += 1
            elif 'I3' in n_rows[y][x][3]:
                I_cells_1 += 1
            elif 'I4' in n_rows[y][x][3]:
                I_cells_1 += 1
            elif 'I5' in n_rows[y][x][3]:
                I_cells_1 += 1

    P_1_popu_list.append(P_cells_1)
    A_1_popu_list.append(A_cells_1)
    I_1_popu_list.append(I_cells_1)
    P_1_prop_list.append(P_cells_1 / cell_total)
    A_1_prop_list.append(A_cells_1 / cell_total)
    I_1_prop_list.append(I_cells_1 / cell_total)
    #print(P_cells_1)
    #print(A_cells_1)
    #print(I_cells_1)
    #print('')
    #print('')
    #print('')



plt.plot(range(0, gens + 1), P_prop_list, label='Frequently Proliferating Cells', linewidth=1)
plt.plot(range(0, gens + 1), A_prop_list, label='Self Sustaining Cells', linewidth=1)
plt.plot(range(0, gens + 1), I_prop_list, label='Invasive Cells', linewidth=1)
plt.plot(range(0, gens + 1), stem_prop_list, label='Original Cells', linewidth=1)
plt.axis([1, gens + 1, 0, 1.2])
plt.ylabel('Proportion of population')
plt.xlabel('Generation')
plt.legend()
plt.savefig(file_name+' proportion plot.png')
plt.close('all')

plt.plot(range(0, gens + 1), P_popu_list, label='Frequently Proliferating Cells', linewidth=1)
plt.plot(range(0, gens + 1), A_popu_list, label='Self Sustaining Cells', linewidth=1)
plt.plot(range(0, gens + 1), I_popu_list, label='Invasive Cells', linewidth=1)
plt.plot(range(0, gens + 1), stem_popu_list, label='Original Cells', linewidth=1)
plt.axis([1, gens + 1, 0, cell_total])
plt.ylabel('Number of Cells')
plt.xlabel('Generation')
plt.legend()
plt.savefig(file_name+' separate population plot.png')
plt.close('all')

plt.plot(range(0, gens + 1), P_1_prop_list, label='Frequently Proliferating Cells', linewidth=1)
plt.plot(range(0, gens + 1), A_1_prop_list, label='Self Sustaining Cells', linewidth=1)
plt.plot(range(0, gens + 1), I_1_prop_list, label='Invasive Cells', linewidth=1)
plt.plot(range(0, gens + 1), stem_prop_list, label='Original Cells', linewidth=1)
plt.axis([1, gens + 1, 0, 1.2])
plt.ylabel('Proportion of population')
plt.xlabel('Generation')
plt.legend()
plt.savefig(file_name+' proportion plot_1.png')
plt.close('all')

plt.plot(range(0, gens + 1), P_1_popu_list, label='Frequently Proliferating Cells', linewidth=1)
plt.plot(range(0, gens + 1), A_1_popu_list, label='Self Sustaining Cells', linewidth=1)
plt.plot(range(0, gens + 1), I_1_popu_list, label='Invasive Cells', linewidth=1)
plt.plot(range(0, gens + 1), stem_popu_list, label='Original Cells', linewidth=1)
plt.axis([1, gens + 1, 0, cell_total])
plt.ylabel('Number of Cells')
plt.xlabel('Generation')
plt.legend()
plt.savefig(file_name+' separate population plot_1.png')
plt.close('all')
"""

'''
# Bottom Edge
        for L in range(0, factor_radius):
            cell_density = 0
            up_radius = -factor_radius - 1
            left_radius = -L
            right_radius = factor_radius
            for y in range(grid_size_y + up_radius, grid_size_y):
                for x in range(left_radius, right_radius + 1):
                    if 'E' in n_rows[y][L + x]:
                        pass
                    elif 'X' in n_rows[y][L + x]:
                        pass
                    else:
                        if n_rows[y][L + x][3] == 1:
                            cell_density += 1
            factor_density[0][L] = cell_density
        for L in range(factor_radius, grid_size_x - factor_radius):
            cell_density = 0
            up_radius = -factor_radius - 1
            left_radius = -factor_radius
            right_radius = factor_radius
            for y in range(grid_size_y + up_radius, grid_size_y):
                for x in range(left_radius, right_radius + 1):
                    if 'E' in n_rows[y][L + x]:
                        pass
                    elif 'X' in n_rows[y][L + x]:
                        pass
                    else:
                        if n_rows[y][L + x][3] == 1:
                            cell_density += 1
            factor_density[0][L] = cell_density
        for L in range(grid_size_x - factor_radius, grid_size_x):
            cell_density = 0
            up_radius = -factor_radius - 1
            left_radius = -factor_radius
            right_radius = grid_size_x - L
            for y in range(grid_size_y + up_radius, grid_size_y):
                for x in range(left_radius, right_radius):
                    if 'E' in n_rows[y][L + x]:
                        pass
                    elif 'X' in n_rows[y][L + x]:
                        pass
                    else:
                        if n_rows[y][L + x][3] == 1:
                            cell_density += 1
                        pass

    for X in range(0, grid_size_x):
        # Left Edge
        for L in range(0, factor_radius):
            cell_density = 0
            up_radius = -L
            right_radius = factor_radius
            down_radius = factor_radius
            for y in range(up_radius, down_radius + 1):
                for x in range(0, right_radius + 1):
                    if 'E' in n_rows[L + y][x]:
                        pass
                    elif 'X' in n_rows[L + y][x]:
                        pass
                    else:
                        if n_rows[L + y][x][3] == 1:
                            cell_density += 1
            factor_density[L][0] = cell_density
        for L in range(factor_radius, grid_size_y - factor_radius):
            cell_density = 0
            up_radius = -factor_radius
            right_radius = factor_radius
            down_radius = factor_radius
            for y in range(up_radius, down_radius + 1):
                for x in range(0, right_radius + 1):
                    if 'E' in n_rows[L + y][x]:
                        pass
                    elif 'X' in n_rows[L + y][x]:
                        pass
                    else:
                        if n_rows[L + y][x][3] == 1:
                            cell_density += 1
            factor_density[L][0] = cell_density
        for L in range(grid_size_y - factor_radius, grid_size_y):
            cell_density = 0
            up_radius = -factor_radius
            right_radius = factor_radius
            down_radius = grid_size_y - L
            for y in range(up_radius, down_radius):
                for x in range(0, right_radius + 1):
                    if 'E' in n_rows[L + y][x]:
                        pass
                    elif 'X' in n_rows[L + y][x]:
                        pass
                    else:
                        if n_rows[L + y][x][3] == 1:
                            cell_density += 1
            factor_density[L][0] = cell_density

        # Right Edge
        for L in range(0, factor_radius):
            cell_density = 0
            up_radius = -L
            left_radius = -factor_radius - 1
            down_radius = factor_radius
            for y in range(up_radius, down_radius + 1):
                for x in range(grid_size_x + left_radius, grid_size_x):
                    if 'E' in n_rows[L + y][x]:
                        pass
                    elif 'X' in n_rows[L + y][x]:
                        pass
                    else:
                        if n_rows[L + y][x][3] == 1:
                            cell_density += 1
            factor_density[L][0] = cell_density
        for L in range(factor_radius, grid_size_y - factor_radius):
            cell_density = 0
            up_radius = -factor_radius
            left_radius = -factor_radius - 1
            down_radius = factor_radius
            for y in range(up_radius, down_radius + 1):
                for x in range(grid_size_x + left_radius, grid_size_x):
                    if 'E' in n_rows[L + y][x]:
                        pass
                    elif 'X' in n_rows[L + y][x]:
                        pass
                    else:
                        if n_rows[L + y][x][3] == 1:
                            cell_density += 1
            factor_density[L][0] = cell_density
        for L in range(grid_size_y - factor_radius, grid_size_y):
            cell_density = 0
            up_radius = -factor_radius
            left_radius = -factor_radius + 1
            down_radius = grid_size_y - L
            for y in range(up_radius, down_radius):
                for x in range(grid_size_x + left_radius, grid_size_x):
                    if 'E' in n_rows[L + y][x]:
                        pass
                    elif 'X' in n_rows[L + y][x]:
                        pass
                    else:
                        if n_rows[L + y][x][3] == 1:
                            cell_density += 1
            factor_density[L][0] = cell_density

        factors = np.zeros((grid_size_y, grid_size_x))
        for y in range(0, grid_size_y):
            for x in range(0, grid_size_x):
                if 'E' in n_rows[y][x]:
                    pass
                elif 'X' in n_rows[y][x]:
                    pass
                else:
                    if n_rows[y][x][3] == 1:
                        factors[y][x] += 1
        print(factors)
        print('')
        print(factor_density)


    cell_list = []
    for y in range(0, grid_size_y):
        for x in range(0, grid_size_x):
            if 'E' in rows[y][x]:
                pass
            elif 'X' in rows[y][x]:
                cell_list.append([y, x, 'X'])

    if len(cell_list) <= 0:
        return
    rd.shuffle(cell_list)
    while len(cell_list) > 0:
        if cell_list[0][0] != 0 and cell_list[0][1] != 0 and cell_list[0][0] != (grid_size_y - 1) \
                and cell_list[0][1] != (grid_size_x - 1):
            space_check(cell_list[0][0], cell_list[0][1], [0])
        elif cell_list[0][0] == 0 and cell_list[0][1] == 0:
            space_check(0, 0, [1, 2, 3, 4, 6])
        elif cell_list[0][0] == 0 and cell_list[0][1] == (grid_size_x - 1):
            space_check(0, grid_size_x - 1, [1, 2, 3, 5, 8])
        elif cell_list[0][0] == (grid_size_y - 1) and cell_list[0][1] == 0:
            space_check(grid_size_y - 1, 0, [1, 4, 6, 7, 8])
        elif cell_list[0][0] == (grid_size_y - 1) and cell_list[0][1] == (grid_size_x - 1):
            space_check(grid_size_y - 1, grid_size_x - 1, [3, 5, 6, 7, 8])
        elif cell_list[0][0] == 0 and cell_list[0][1] != 0 and cell_list[0][1] != (grid_size_x - 1):
            space_check(0, cell_list[0][1], [1, 2, 3])
        elif cell_list[0][0] == (grid_size_y - 1) and cell_list[0][1] != 0 and cell_list[0][1] != (grid_size_x - 1):
            space_check(grid_size_y - 1, cell_list[0][1], [6, 7, 8])
        elif cell_list[0][0] != 0 and cell_list[0][0] != (grid_size_y - 1) and cell_list[0][1] == 0:
            space_check(cell_list[0][0], 0, [1, 4, 6])
        elif cell_list[0][0] != 0 and cell_list[0][0] != (grid_size_y - 1) and cell_list[0][1] == (grid_size_x - 1):
            space_check(cell_list[0][0], (grid_size_x - 1), [3, 5, 8])
        del cell_list[0]


def space_check(fi, si, restriction_list):
    if 1 not in restriction_list:
        if 'X' in n_rows[fi - 1][si - 1]:
            pass
        else:
            if factor_density[fi - 1][si - 1] > factor_threshold:
                n_rows[fi][si] = 'E'
                return
    if 2 not in restriction_list:
        if 'X' in n_rows[fi - 1][si]:
            pass
        else:
            if factor_density[fi - 1][si] > factor_threshold:
                n_rows[fi][si] = 'E'
                return
    if 3 not in restriction_list:
        if 'X' in n_rows[fi - 1][si + 1]:
            pass
        else:
            if factor_density[fi - 1][si + 1] > factor_threshold:
                n_rows[fi][si] = 'E'
                return
    if 4 not in restriction_list:
        if 'X' in n_rows[fi][si - 1]:
            pass
        else:
            if factor_density[fi][si - 1] > factor_threshold:
                n_rows[fi][si] = 'E'
                return
    if 5 not in restriction_list:
        if 'E' in n_rows[fi][si + 1]:

    if 6 not in restriction_list:
        if 'E' in n_rows[fi + 1][si - 1]:

    if 7 not in restriction_list:
        if 'E' in n_rows[fi + 1][si]:

    if 8 not in restriction_list:
        if 'E' in n_rows[fi + 1][si + 1]:


'''

"""
    for y in range(seeding_grid_low_y, seeding_grid_high_y):
        for x in range(seeding_grid_low_x, seeding_grid_high_x):
            rand_mut = 0
            if rd.randint(1, 100) <= 0:
                rd.shuffle(mutation_list_global)
                rand_mut = mutation_list_global[0]
                rows[y][x] = ['H', rd.randint(0, lifespan - 2), rand_mut, [[rand_mut, 0]], [mutation_type + str(rand_mut)]]
                n_rows[y][x] = ['H', rd.randint(0, lifespan - 2), rand_mut, [[rand_mut, 0]], [mutation_type + str(rand_mut)]]
            else:
                rows[y][x] = ['H', rd.randint(0, lifespan - 2), 0, [[0, 0]], []]
                n_rows[y][x] = ['H', rd.randint(0, lifespan - 2), 0, [[0, 0]], []]
"""