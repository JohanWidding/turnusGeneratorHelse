import math
from collections import Counter

from tqdm import tqdm

from SampleEmployee import normalize_dict
from check_name_repetition import check_name_repetition


def combination_validator_v1(combinations, N_on_shift, workers_dict, N_sample, num_days):
    num_combinations = math.comb(N_sample + num_days - 1, num_days)
    normalized_workers_dict = Counter({key: math.ceil(((value*37.5) * (num_days/7))/12.5) for key, value in workers_dict.items()})
    print(normalized_workers_dict)
    # Filter combinations based on criteria
    valid_combinations = []
    # Initialize the set of names in the last three combinations

    for combination in tqdm(combinations, desc="Processing", unit=" combinations", total=num_combinations):
        # Flatten the combination to get a list of all names
        all_names = [name for shift in combination for name in shift]

        # Count occurrences of each name using Counter for efficiency
        name_counts = Counter(name for name in all_names)

        set_weekend1 = set(all_names[N_on_shift * 4:N_on_shift * 6])
        set_weekend2 = set(all_names[N_on_shift * 11:N_on_shift * 13])
        # Check if name_counts is less than or equal to normalized_workers_dict
        is_less_or_equal = all(name_counts[name] <= normalized_workers_dict[name] for name in name_counts)

        # Check if no person is mentioned more than 3 times
        if is_less_or_equal:
            if set_weekend1.isdisjoint(set_weekend2):
                #if len(set_weekend1) == 2:
                   # if len(set_weekend2) == 2:
                        failed = False
                        for name in name_counts.keys():
                            if check_name_repetition(all_names, name, 3, 2, N_on_shift):
                                failed = True
                                break

                        if not failed:
                            valid_combinations.append(combination)

        # Stop if we have found enough valid combinations
        if len(valid_combinations) >= 10:
            return valid_combinations

    return valid_combinations