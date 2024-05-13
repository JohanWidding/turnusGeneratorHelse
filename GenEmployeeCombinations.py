from ortools.sat.python import cp_model
import itertools

from SampleEmployee import sample_shifts


def generate_shifts(shift_workers_dict, num_shifts, sample_size):
    # Creates the model.
    model = cp_model.CpModel()

    # Creates shift variables.
    shifts = {}
    # Construct the for loop as a string with multiple lines
    loop_string = """comparison_list = {}\n"""
    for i in range(1, num_shifts+1):
        loop_string += f"for d{i} in shift_workers_dict.keys():\n"+("\t"*i)+f"comparison_list[{i}] = d{i}\n"+("\t"*i)
    loop_string += f"if len(comparison_list.values()) == len(set(comparison_list.values())):\n"+("\t"*(num_shifts+1))
    loop_string += 'shifts[('+''.join("d"+str(i)+"," for i in range(1, num_shifts+1))[:-1]+')] = model.new_bool_var(f"shifts_'+''.join("{d"+str(i)+"}_" for i in range(1, num_shifts+1))[:-1]+'")'

    # Execute the constructed string as code
    exec(loop_string)

    best_shifts = sample_shifts(shift_workers_dict, shifts, sample_size=12, seed=42)

    for i in best_shifts:
        print(i)

    return best_shifts

