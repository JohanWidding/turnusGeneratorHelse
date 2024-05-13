import copy
import math
import random
from multiprocessing import Pool

from matplotlib import pyplot as plt
from tqdm import tqdm


# Function to generate Gantt chart
def plot_gantt(all_workers, workers, n_weeks):
    fig, gnt = plt.subplots()

    # Setting Y-axis limits
    gnt.set_ylim(0, 50)

    # Setting X-axis limits
    gnt.set_xlim(0, len(list(all_workers.values())[0]) * 48)

    # Setting labels for x-axis and y-axis
    gnt.set_xlabel('Tid')
    new_all_workers = {}
    for name, nested_lists in all_workers.items():
        _list = []
        for sublist in nested_lists:
            _list.extend(sublist)
        new_all_workers[name] = _list
    all_workers = new_all_workers
    weeks = ["Mandag", "Tirsdag", "Onsdag", "Torsdag", "Fredag", "Lørdag", "Søndag"] * n_weeks + ["Mandag"]

    workers_working = {worker: [] for worker in all_workers.keys()}
    worker_info = {worker: "" for worker in all_workers.keys()}

    for name, shift in all_workers.items():
        t = 0
        for i in shift:
            if i == 1:
                workers_working[name].append((t + 15, 25))
            t += 48

    # Setting ticks on y-axis
    gnt.set_yticks([15 + i * 15 for i in range(len(all_workers))])

    # Labelling ticks of y-axis
    gnt.set_yticklabels(all_workers)

    # Setting ticks on x-axis
    gnt.set_xticks([i * 48 for i in range(len(list(all_workers.values())[0])+1)])

    # Labelling ticks of x-axis
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
            elif tu[-1] == 15:
                gnt.broken_barh([tu], (counter, 9), facecolors=('tab:red'))
            elif tu[-1] == 14:
                gnt.broken_barh([tu], (counter, 9), facecolors=('tab:purple'))
            else:
                gnt.broken_barh([tu], (counter, 9), facecolors=('tab:blue'))
        # Declaring a bar in schedule
        worker_info[w] = str(sum(hours) / 2)
        counter += 15
    worker_info = [w + " " + str(int(workers[w]*100)) + "% (" + t + "t)" for w, t in worker_info.items()]
    gnt.set_yticklabels(worker_info)

    plt.show()
def find_empty_sublists(data, position):
    result = []

    for person, values in data.items():
        if position < len(values) and not values[position]:
            result.append(person)

    return result

def week_possabilities():
    weekend_p = [
        [1, 0, 0, 0, 1, 1, 1],
        [0, 0, 0, 0, 1, 1, 1]
    ]
    workday_p = [
        [1, 1, 1, 0, 0, 0, 0],
        [0, 1, 1, 1, 0, 0, 0],
        [1, 0, 1, 1, 0, 0, 0],
        [1, 1, 0, 1, 0, 0, 0],
        [1, 1, 0, 0, 0, 0, 0],
        [1, 0, 1, 0, 0, 0, 0],
        [1, 0, 0, 1, 0, 0, 0],
        [0, 1, 1, 0, 0, 0, 0],
        [0, 1, 0, 1, 0, 0, 0],
        [0, 0, 1, 1, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0]
    ]
    return weekend_p, workday_p

def check_shifts(shiftworkers_per_day, shift, index):
    shiftworkers_per_day = shiftworkers_per_day[index*7:index*7+7]
    for ind, s in shift.items():
        for i in range(len(s[index])):
            shiftworkers_per_day[i] -= s[index][i]
    all_zero = all(num == 0 for num in shiftworkers_per_day)
    if all_zero:
        return False
    else:
        return True

def combination_generator(n_on, employees, n_weeks, weekend_frequency):
    normalized_workers_dict = {key: int(round((value * 37.5 * n_weeks) / 12.5)) for key, value in workers.items()}
    # Creating a copy of the normalized dictionary
    worker_control = copy.deepcopy(normalized_workers_dict)

    weekend_p, workday_p = week_possabilities()

    shiftworkers_per_day = [n_on for _ in range(n_weeks*7)]



    shift = {e: [[] for _ in range(n_weeks)] for e, d in employees.items()}

    weekend_control = {number: n_on for number in range(weekend_frequency)}


    for e, d in employees.items():


        # Setter av helgene vedkommende skal jobbe:
        keys_with_value_larger_than_zero = [key for key, value in weekend_control.items() if value > 0]
        if len(keys_with_value_larger_than_zero) == 0: pass
        else:
            random_key = random.choice(keys_with_value_larger_than_zero)
            weekend_control[random_key] -= 1
            # Loop through the weeks and edit every weekend_frequency element
            for i in range(random_key, n_weeks, weekend_frequency):
                random_shift = random.choice(weekend_p)
                shift[e][i] = random_shift
                worker_control[e] -= sum(random_shift)

    for w in range(n_weeks):
        possible_workers = find_empty_sublists(shift, w)
        names_with_nonzero_values = [name for name, value in worker_control.items() if value > 0]
        overlapping_names = list(set(possible_workers) & set(names_with_nonzero_values))
        not_valid = True
        counter = 0
        while not_valid:
            if counter >= 1000: return False
            not_enough_breakes = False
            for name in overlapping_names:
                random_shift = random.choice(workday_p)
                shift[name][w] = random_shift
                if w != 0:
                    if shift[name][w-1][-1] == 1:
                        mon_tue = shift[name][w][0:2]
                        if sum(mon_tue) > 0:
                            not_enough_breakes = True
                            break
            if not_enough_breakes: continue

            too_many_workers = check_shifts(shiftworkers_per_day, shift, w)
            if too_many_workers:
                pass
            else:
                for name, shifts in shift.items():
                    worker_control[name] = normalized_workers_dict[name] - sum(sum(sublist) for sublist in shifts)
                if all(value >= 0 for value in worker_control.values()):
                    not_valid = False
            counter += 1




    return shift

def generate_work_shift(_):
    """
    Function to generate work shifts.
    """
    return combination_generator(n_on, workers, n_weeks, weekend_freq)



if __name__ == "__main__":
    workers = {'Alice': 1, 'Bernt': 1, "Paul": 0.75, 'Bob': 0.66, 'David': 0.66, 'Helena': 0.55}
    n_on = 2
    n_weeks = 4
    weekend_freq = 3

    valid = False
    iterations = 0



    # Initialize tqdm progress bar
    pbar = tqdm(total=0)


    while not valid:
        iterations += 1
        work_shift = combination_generator(n_on, workers, n_weeks, weekend_freq)
        # Update progress bar
        pbar.set_description(f"Iteration {iterations}")
        pbar.update(1)
        if work_shift == False:
            continue
        else:
            valid = True
            plot_gantt(work_shift, workers, n_weeks)

    # Close the progress bar
    pbar.close()


