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
import itertools
import random

from GenEmployeeCombinations import generate_shifts
import math
from itertools import combinations_with_replacement
from check_name_repetition import check_name_repetition
from combination_validator_v1 import combination_validator_v1
from combination_validator_v2 import combination_validator_v2
from concurrent.futures import ProcessPoolExecutor

from combination_validator_v3 import CombinationValidator3

# Langvakter jobber 12.5 timer på dagtid (07:30-08:00)
# Ordinærvakter jobber 7.5 timer på dagtid og kveldstid (07:30-15:00) og (14:30-22:00)
# Nattvakter jobber 12 timer på nattid (20:00-08:00)

if __name__ == '__main__':
    executor = ProcessPoolExecutor(max_workers=8)

    langvakter = {'Alice':1, 'Bernt':1, "Paul":1, 'Bob':1, 'David':1, 'Helena':1, 'Ulrik':0.8}
    N_sample = 12
    N_on_shift = 2
    sample = generate_shifts(langvakter, N_on_shift, N_sample)


    all_workers = list(langvakter.keys())
    weeks = ["Mandag", "Tirsdag", "Onsdag", "Torsdag", "Fredag", "Lørdag", "Søndag"]*3
    num_days = len(weeks)
    num_combinations = math.comb(N_sample + num_days - 1, num_days)

    print(f"Antall ansatte: {len(all_workers)}")
    print(f"Mulige kombinasjoner gitt N ({N_sample}) og r ({num_days}): {num_combinations}")

    # Generate all combinations with repetition using itertools.product()
    #combinations = combinations_with_replacement(sample, num_days)
    combinations = itertools.product(sample, repeat=num_days)


    # My try to create a multiprocessing class
    #validtor = CombinationValidator3(combinations, N_on_shift, langvakter, N_sample, num_days)
    #valid_combinations = validtor.validate_combinations()

    #Use a while loop to randomly make combinations, Theroeticly following the law of large numbers, all combinations will eventially appare.


    # Working function
    valid_combinations = combination_validator_v1(combinations, N_on_shift, langvakter, N_sample,num_days)

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
            workers_working[shift[0]].append((t+15, 25))
            workers_working[shift[1]].append((t+15, 25))
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

