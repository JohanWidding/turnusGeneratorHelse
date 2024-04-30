"""Example of a simple nurse scheduling problem.

Problem: Gitt de ansatte en bolig har - hva er den optimalt kostnadsbesparende turnusen vi kan oppnå?

Min(lønnskostnader)

Gitt:
Hver ansatt er fri til å velge stillingsprosent: 20-40-60-80-100
Hver ansatt skal jobbe minst hver 3 helg, vi tester også med at langvakter skal jobbe hver 4 helg.
Å jobbe helg betyr at den ansatte skal ha vakt fredag - søndag
En ansatt skal ikke jobbe mer enn det stillingsprosenten tillater, ex. 100% = 37.5 timer i uken, 162,5 arbeids-timer i en måned.


Videre plan:
Ansatte kan velge dager de ønsker fri fra arbeid.




"""
import math
import random

from tqdm import tqdm
from ortools.sat.python import cp_model
from collections import Counter
import itertools
from itertools import combinations_with_replacement

from check_name_repetition import check_name_repetition

# Data.
# Langvakter jobber 12.5 timer på dagtid (07:30-08:00)
# Ordinærvakter jobber 7.5 timer på dagtid og kveldstid (07:30-15:00) og (14:30-22:00)
# Nattvakter jobber 12 timer på nattid (20:00-08:00)
langvakter = ['Alice', 'Bernt', "Paul", 'Bob', 'David', 'Helena', 'Ulrik', 'Steffen', 'Inge', 'Leif']
ordinærvakter = ['Eva', 'Finn', 'Greta', 'Lars', 'Stian', 'Fredrik', 'Jens']
nattvakter = ['Hannah', 'Ian', 'Joben', 'Jack', 'Katie', 'Liam', 'Ellen', 'Preben', 'Dennis']
all_workers = langvakter+ordinærvakter+nattvakter

print(f"Antall ansatte: {len(all_workers)}")

# Lister
weeks = ["Mandag", "Tirsdag", "Onsdag", "Torsdag", "Fredag", "Lørdag", "Søndag"]*2
num_days = len(weeks)

# Creates the model.
model = cp_model.CpModel()

# Creates shift variables. (Dummy variables)
# skiftet består av minimumskravet til boligen som i dette eksempelet er 3 må være på fra 08-22, 2 må være på fra 22-08
shifts = {}
for l1 in langvakter:
    for l2 in langvakter:
        for d1 in ordinærvakter:
            for k1 in ordinærvakter:
                for n1 in nattvakter:
                    for n2 in nattvakter:
                        if l1 == l2 or d1 == k1 or n1 == n2:
                            pass
                        else:
                            shifts[(l1, l2, d1, k1, n1, n2)] = model.new_bool_var(f"shifts_l{l1}_l{l2}_d{d1}_k{k1}_n{n1}_n{n2}")
print(f"Mulige kombinasjoner av de ansatte: {len(shifts)}")


# Shuffle the keys of the shifts dictionary (Etter en for-løkke er skiftene sortert etter langvakter i dette tilfellet)
random.seed(555)  # for reproducibility
shifts_keys = list(shifts.keys())
random.shuffle(shifts_keys)

# Det er mulig å dele skiftene opp i sett på randome utvalg på 12 stk. -> Videre dersom man sjekker alle mulig kombinasjoner av disse 12 vakskiftene på 14 dager:
# Noe som gir 4,457,400 mulige kombinasjoner når det er mulighet for repitisjon av skiftene
N = 12
# Sørg for at alle navnene er inkludert i skiftene
while True:
    sample = (random.sample(shifts_keys, N))
    uniqe_names = []
    for shift in sample:
        for name in shift:
            if name in uniqe_names:
                pass
            else:
                uniqe_names.append(name)
    if set(uniqe_names) == set(all_workers):
        break
    else:
        pass
for shift in sample: print(shift)
# Generate all combinations with repetition using itertools.product()
combinations = combinations_with_replacement(sample, num_days)
print(f"Mulige kombinasjoner gitt N ({N}) og r ({num_days}): {math.comb(N + num_days - 1, num_days)}")
# Filter combinations based on criteria
valid_combinations = []
# Initialize the set of names in the last three combinations
for combination in tqdm(combinations, desc="Processing", unit=" combinations"):
    # Flatten the combination to get a list of all names
    all_names = [name for shift in combination for name in shift]

    # Count occurrences of each name using Counter for efficiency
    name_counts_langvakt = Counter(name for name in all_names if name in langvakter+nattvakter)

    set_weekend1 = set(all_names[24:42])
    set_weekend2 = set(all_names[66:84])

    # Check if no person is mentioned more than 3 times
    if all(count <= 6 for count in name_counts_langvakt.values()):
        if set_weekend1.isdisjoint(set_weekend2):
            if len(set_weekend1) == 6:
                if len(set_weekend2) == 6:
                    failed = False
                    for name in name_counts_langvakt.keys():
                        too_repetative = check_name_repetition(all_names, name, 3, 2, 6)
                        if too_repetative:
                            failed = True

                    if failed:
                        continue
                    else:
                        # Check if the names in this combination are also in the last three combinations
                        valid_combinations.append(combination)



    # Stop if we have found enough valid combinations
    if len(valid_combinations) >= 1:
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
        workers_working[vakter[0][1:]].append((t+15, 25))
        workers_working[vakter[1][1:]].append((t+15, 25))
        workers_working[vakter[2][1:]].append((t+15, 15))
        workers_working[vakter[3][1:]].append((t+30, 14))
        workers_working[vakter[4][1:]].append((t+40, 24))
        workers_working[vakter[5][1:]].append((t+40, 24))
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
            elif  tu[-1] == 15:
                gnt.broken_barh([tu], (counter, 9), facecolors=('tab:red'))
            elif tu[-1] == 14:
                gnt.broken_barh([tu], (counter, 9), facecolors=('tab:purple'))
            else:
                gnt.broken_barh([tu], (counter, 9), facecolors=('tab:blue'))
        # Declaring a bar in schedule
        worker_info[w] = str(sum(hours) / 2)
        counter += 15
    worker_info = [w+" ("+t+"t)" for w, t in worker_info.items()]
    gnt.set_yticklabels(worker_info)

    plt.show()

