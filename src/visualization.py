import numpy as np
import matplotlib.pyplot as plt
import csv
import scipy.optimize
import sys
import random

if len(sys.argv) < 2:
    print("Arguments:")
    print("1. (Required) Fraction of entries to process. Decimal number between 0 and 1. 1 means all, 0 means none. ")
    print("2. (Optional) Index of a column to apply a limit on (0-based). 0 for pregnancy, 1 for glucose, etc.")
    print("2. (Optional) Upper limit to apply on the chosen column. Must start with '<'. Example: '<24'")
    print("3. (Optional) Lower limit to apply on the chosen column. Must start with '>'. Example: '>5.7'")
    print("You may choose to apply only an upper limit or only a lower limit.")
    sys.exit(0)

"""
    Read arguments
"""

fraction = float(sys.argv[1])
limit_max = -1
limit_min = -1
limit_col = -1
if len(sys.argv) >= 3:
    limit_col = int(sys.argv[2])
if len(sys.argv) >= 4:
    if sys.argv[3].startswith(">"):
        limit_min = int(sys.argv[3][1:])
    elif sys.argv[3].startswith("<"):
        limit_max = int(sys.argv[3][1:])
if len(sys.argv) >= 5:
    if sys.argv[4].startswith(">"):
        limit_min = int(sys.argv[4][1:])
    elif sys.argv[4].startswith("<"):
        limit_max = int(sys.argv[4][1:])

if limit_max != -1:
    print("Limit on column " + str(limit_col) + ": maximum " + str(limit_max))
if limit_min != -1:
    print("Limit on column " + str(limit_col) + ": minimum " + str(limit_min))
if fraction != 1:
    print(str(fraction * 100) + "% of entries will be randomly selected")
print()

"""
    Read file
"""

file_name = 'data.csv'
print("Reading '" + file_name + "'...")

total_nb_entries = 0
col_preg = []  # number of pregnancies
col_gluc = []  # result of glucose tolerance test
col_bldp = []  # blood pressure
col_skin = []  # triceps skin fold thickness
col_insu = []  # insulin
col_bmi = []  # Body Mass Index
col_dpf = []  # Diabetes Pedigree Function
col_age = []  # age
col_outc = []  # outcome: whether or not that person has diabetes

with open(file_name, 'r') as f:
    reader = csv.reader(f)
    first = True
    for row in reader:
        if first:
            first = False
        else:
            accepted = True
            if limit_col != -1:
                limited_val = float(row[limit_col])
                if limit_max != -1 and limited_val > limit_max:
                    accepted = False
                if limit_min != -1 and limited_val < limit_min:
                    accepted = False
            if accepted:
                nb_should_be_accepted = round(total_nb_entries * fraction)
                if len(col_outc) - nb_should_be_accepted >= 2:
                    accepted = False
                elif len(col_outc) - nb_should_be_accepted <= -2:
                    accepted = True
                else:
                    accepted = random.uniform(0, 1) <= fraction
                total_nb_entries += 1
            if accepted:
                col_preg.append(int(row[0]))
                col_gluc.append(float(row[1]))
                col_bldp.append(float(row[2]))
                col_skin.append(float(row[3]))
                col_insu.append(float(row[4]))
                col_bmi.append(float(row[5]))
                col_dpf.append(float(row[6]))
                col_age.append(int(row[7]))
                col_outc.append(int(row[8]))

col_preg = np.asarray(col_preg)
col_gluc = np.asarray(col_gluc)
col_bldp = np.asarray(col_bldp)
col_skin = np.asarray(col_skin)
col_insu = np.asarray(col_insu)
col_bmi = np.asarray(col_bmi)
col_dpf = np.asarray(col_dpf)
col_age = np.asarray(col_age)
col_outc = np.asarray(col_outc)

print(str(len(col_outc)) + " entries selected")
print()

"""
    Parallel coordinates
"""
"""
print("Creating parallel coordinate plot")

fig = plt.figure()

for i in range(len(col_outc)):
    row = [col_preg[i] * 13, col_gluc[i], col_bldp[i] * 1.5, col_skin[i] * 3, col_insu[i] / 3, (col_bmi[i] - 15) * 4, col_dpf[i] * 120, col_age[i] * 3,
           col_outc[i] * 200]
    plt.plot(range(len(row)), row)

labels = ["Pregn", "Glucose", "Bld pr.", "Skin.", "Insulin", "BMI.", "DPF.", "Age", "Diabetes?"]
plt.title("parallel coordinate plot")
plt.xticks([0, 1, 2, 3, 4, 5, 6, 7, 8], labels=labels)
plt.savefig("parallel_coordinates.pdf")
plt.close()
"""

"""
    Scatter plot matrix
"""


def calculate_position(x, y):
    return y * len(columns) + x + 1


def create_scatter_plot(x_axis_vals, y_axis_vals, x_axis_name, y_axis_name, pos_x, pos_y):
    subplot_index = calculate_position(pos_x, pos_y)
    col_map = {0: "green", 1: "red"}
    colors = list(map(lambda x: col_map.get(x), col_outc))
    plt.subplot(len(columns), len(columns), subplot_index)
    plt.scatter(x_axis_vals, y_axis_vals, s=4, marker=".", alpha=0.7, c=colors)
    if pos_x == 0:
        plt.ylabel(y_axis_name)
    if pos_y == len(columns) - 1:
        plt.xlabel(x_axis_name)
    plt.xticks([])
    plt.yticks([])


columns = {
    "pregn.": col_preg,
    "gluc.": col_gluc,
    "press.": col_bldp,
    "skin": col_skin,
    "insulin": col_insu,
    "BMI": col_bmi,
    "DPF": col_dpf,
    "age": col_age
}

print("Creating scatter matrix...")
for x in range(len(columns)):
    col1_name = list(columns.keys())[x]
    for y in range(len(columns)):
        col2_name = list(columns.keys())[y]
        if y != x:
            create_scatter_plot(columns.get(col1_name), columns.get(col2_name), col1_name, col2_name, x, y)

for col_nb in range(len(columns)):
    subplot_index = calculate_position(col_nb, col_nb)
    data = columns.get(list(columns.keys())[col_nb])
    red_data, green_data = [], []
    for i in range(len(col_outc)):
        if col_outc[i] == 0:
            green_data.append(data[i])
        else:
            red_data.append(data[i])
    plt.subplot(len(columns), len(columns), subplot_index)
    plt.hist(green_data, bins=30, fc=(0, 0.5, 0, 0.5))
    plt.hist(red_data, bins=30, fc=(1, 0, 0, 0.5))
    plt.xticks([])
    plt.yticks([])
    if col_nb == 0:
        plt.ylabel(list(columns.keys())[col_nb])
    elif col_nb == len(columns) - 1:
        plt.xlabel(list(columns.keys())[col_nb])

plt.savefig("scatter_matrix.pdf")
plt.close()

print("Done")
