"""Example of a simple nurse scheduling problem.

Problem minimer antall arbeidere som trengs for å fylle skift og arbeidsbehov

Tenker modellen kan deles opp slik at hvert vaktskifte kjører algoritmen for seg selv. og kobineres senere.
Trenger et kriterie som avgjør om sykepleieren jobber for mye en uke. Og hver sykepleier jobber ulik maks timer.
Trenger et kriterie som gjør at pleierene ikke jobber mer enn hver 3 helg.


162,5 arbeids-timer i en måned


"""
import random

from tqdm import tqdm
from ortools.sat.python import cp_model
from collections import Counter
import itertools

num_days = 7

# Data.
dagvakt1 = ['Alice', 'Bernt', "Paul"]
dagvakt2 = ['Bob', 'David', 'Helena']
dagvakt3 = ['Eva', 'Finn', 'Greta', 'Lars']
nattvakt1 = ['Hannah', 'Ian', 'Joben']
nattvakt2 = ['Jack', 'Katie', 'Liam', 'Ellen']
all_workers = dagvakt1+dagvakt2+dagvakt3+nattvakt1+nattvakt2

# Lister
weeks = ["Mandag", "Tirsdag", "Onsdag", "Torsdag", "Fredag", "Lørdag", "Søndag"]

# Creates the model.
model = cp_model.CpModel()

# Creates shift variables. (Dummy variables)
# shifts[(n, d, s)]: nurse 'n' works shift 's' on day 'd'.
shifts = {}
for d1 in dagvakt1:
    for d2 in dagvakt2:
        for d3 in dagvakt3:
            for n1 in nattvakt1:
                for n2 in nattvakt2:
                    for ev1 in dagvakt1+dagvakt2+dagvakt3:
                        if ev1 == d1 or ev1 == d2 or ev1 == d3:
                            pass
                        else:
                            shifts[(n1, n2, ev1, d1, d2, d3)] = model.new_bool_var(f"shifts_n{n1}_n{n2}_e{ev1}_d{d1}_d{d2}_d{d3}")

# Shuffle the keys of the shifts dictionary
random.seed(555)  # for reproducibility
shifts_keys = list(shifts.keys())
random.shuffle(shifts_keys)

# Generate all combinations of 7 shifts with some randomness
all_combinations = itertools.islice(
    (random.sample(shifts_keys, num_days) for _ in itertools.count()),
    100000000
)

# Filter combinations based on criteria
valid_combinations = []
# Initialize the set of names in the last three combinations
last_three_names = set()
for combination in tqdm(all_combinations, desc="Processing", unit=" combinations"):
    # Flatten the combination to get a list of all names
    names = [name for shift in combination for name in shift]

    # Count occurrences of each name using Counter for efficiency
    name_counts = Counter(names)

    name_counts_weekend = Counter(names[24:])


    # Check if no person is mentioned more than 3 times
    if all(count <= 3 for count in name_counts.values()):
        # Check if the names in this combination are also in the last three combinations
        if len(name_counts_weekend) == 9:
            valid_combinations.append(combination)



    # Stop if we have found enough valid combinations
    if len(valid_combinations) >= 2:
        break






# Importing the matplotlib.pyplot
import matplotlib.pyplot as plt

num_half_hours = 24*2*num_days




# Print valid combinations
for i, combination in enumerate(valid_combinations, 1):
    print(f"Combination {i}:")
    # Declaring a figure "gnt"
    fig, gnt = plt.subplots()

    # Setting Y-axis limits
    gnt.set_ylim(0, 50)

    # Setting X-axis limits
    gnt.set_xlim(0, num_half_hours)

    # Setting labels for x-axis and y-axis
    gnt.set_xlabel('Tid')
    workers_working = {worker: [] for worker in all_workers}
    worker_info = {worker: "" for worker in all_workers}
    t = 0
    for shift in combination:
        vakter = str(shifts[shift]).split("_")[1:]
        workers_working[vakter[0][1:]].append((t+40, 24))
        workers_working[vakter[1][1:]].append((t+40, 24))
        workers_working[vakter[2][1:]].append((t+40, 5))
        workers_working[vakter[3][1:]].append((t+15, 25))
        workers_working[vakter[4][1:]].append((t+15, 25))
        workers_working[vakter[5][1:]].append((t+15, 25))
        t += 48
    # Setting ticks on y-axis
    gnt.set_yticks([15 + i * 15 for i in range(len(all_workers))])
    # Labelling tickes of y-axis


    # Setting ticks on y-axis
    gnt.set_xticks([i * 48 for i in range(num_days)])
    # Labelling tickes of y-axis
    gnt.set_xticklabels(weeks)

    # Setting graph attribute
    gnt.grid(True)
    counter = 10
    for w, on in workers_working.items():
        hours = []
        for tu in on:
            hours.append(tu[-1])
            if tu[-1] == 25:
                gnt.broken_barh([tu], (counter, 9), facecolors=('tab:orange'))
            elif  tu[-1] == 5:
                gnt.broken_barh([tu], (counter, 9), facecolors=('tab:red'))
            else:
                gnt.broken_barh([tu], (counter, 9), facecolors=('tab:blue'))
        # Declaring a bar in schedule
        worker_info[w] = str(sum(hours) / 2)
        counter += 15
    worker_info = [w+" ("+t+"t)" for w, t in worker_info.items()]
    gnt.set_yticklabels(worker_info)

    plt.show()

