import numpy as np
import matplotlib.pyplot as plt
import csv
import scipy.optimize
import sys
import random

if len(sys.argv) < 2:
    print("Required argument: fraction of entries to process (float)")
    sys.exit(0)

"""
    Read arguments
"""

fraction = float(sys.argv[1])
max_age = -1
min_age = -1
if len(sys.argv) >= 3:
    if sys.argv[2].startswith(">"):
        min_age = int(sys.argv[2][1:])
    elif sys.argv[2].startswith("<"):
        max_age = int(sys.argv[2][1:])
if len(sys.argv) >= 4:
    if sys.argv[3].startswith(">"):
        min_age = int(sys.argv[3][1:])
    elif sys.argv[3].startswith("<"):
        max_age = int(sys.argv[3][1:])

if max_age != -1:
    print("Maximum age: " + str(max_age))
if min_age != -1:
    print("Minimum age " + str(min_age))
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
            age = int(row[7])
            if max_age != -1 and age > max_age:
                accepted = False
            if min_age != -1 and age < min_age:
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
                col_age.append(age)
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
print(col_preg[:5])
print(col_gluc[:5])
print(col_age[:5])
print(col_outc[:5])