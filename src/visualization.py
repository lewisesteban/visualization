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
max_pop = -1
min_pop = -1
if len(sys.argv) >= 3:
    if sys.argv[2].startswith(">"):
        min_pop = int(sys.argv[2][1:])
    elif sys.argv[2].startswith("<"):
        max_pop = int(sys.argv[2][1:])
if len(sys.argv) >= 4:
    if sys.argv[3].startswith(">"):
        min_pop = int(sys.argv[3][1:])
    elif sys.argv[3].startswith("<"):
        max_pop = int(sys.argv[3][1:])

if max_pop != -1:
    print("Only cities with an initial population of " + str(max_pop) + " maximum will be selected")
if min_pop != -1:
    print("Only cities with an initial population of " + str(min_pop) + " minimum will be selected")
if fraction != 1:
    print("Approximately " + str(fraction * 100) + "% of the cities will be randomly selected")
print()

"""
    Read file
"""

file_name = 'data.csv'
print("Reading '" + file_name + "'...")

nb_cities = 0
accepted_cities = []
col_city = []
col_year = []
col_region = []
col_npg = []  # natural population growth: difference between birth rate and death rate
col_birth = []  # number of births this year per 1000 people
col_death = []  # number of deaths this year per 1000 people
col_migration = []  # number of migrants coming to the city this year per 1000 people (negative if people are leaving)
col_population = []


def safe_cast(val, to_type, default=None):
    try:
        return to_type(val)
    except (ValueError, TypeError):
        return default


with open(file_name, 'r') as f:
    reader = csv.reader(f)
    first = True
    for row in reader:
        if first:
            first = False
        else:
            nb_cities += 1
            year = safe_cast(row[0], int)
            city = row[1]
            population = safe_cast(row[6], float)
            if year is not None:
                accepted = True
                if year == 1990:
                    if population is None:
                        accepted = False
                    else:
                        if max_pop != -1 and population > max_pop:
                            accepted = False
                        if min_pop != -1 and population < min_pop:
                            accepted = False
                    if accepted:
                        nb_should_be_accepted = round((nb_cities - 1) * fraction)
                        if len(accepted_cities) - nb_should_be_accepted >= 2:
                            accepted = False
                        elif len(accepted_cities) - nb_should_be_accepted <= -2:
                            accepted = True
                        else:
                            accepted = random.uniform(0, 1) <= fraction
                        if accepted:
                            accepted_cities.append(city)
                else:
                    accepted = city in accepted_cities
                if accepted:
                    col_year.append(year)
                    col_city.append(city)
                    col_npg.append(safe_cast(row[2], float))
                    col_birth.append(safe_cast(row[3], float))
                    col_death.append(safe_cast(row[4], float))
                    col_migration.append(safe_cast(row[5], float))
                    col_population.append(population)

col_year = np.asarray(col_year)
col_npg = np.asarray(col_npg)
col_birth = np.asarray(col_birth)
col_death = np.asarray(col_death)
col_migration = np.asarray(col_migration)
col_population = np.asarray(col_population)

print(str(len(accepted_cities)) + " cities selected, " + str(len(col_city)) + " selected entries in total")
