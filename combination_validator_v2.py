from check_name_repetition import check_name_repetition
from collections import Counter
from tqdm import tqdm
import math


def combination_validator_v2(combinations, N_on_shift, workers_dict, N_sample, num_days):
    num_combinations = math.comb(N_sample + num_days - 1, num_days)
    normalized_workers_dict = Counter(
        {key: math.ceil(((value * 37.5) * (num_days / 7)) / 12.5) for key, value in workers_dict.items()})
    print(normalized_workers_dict)

    valid_combinations = []
    set_weekend1 = set()
    set_weekend2 = set()

    for combination in tqdm(combinations, desc="Processing", unit=" combinations", total=num_combinations):
        all_names = set(name for shift in combination for name in shift)
        name_counts = Counter(all_names)

        set_weekend1.clear()
        set_weekend2.clear()

        # Extract weekend shifts from all_names directly
        weekend1_names = set(name for shift in combination[N_on_shift * 4:N_on_shift * 6] for name in shift)
        weekend2_names = set(name for shift in combination[N_on_shift * 11:N_on_shift * 13] for name in shift)

        set_weekend1.update(weekend1_names)
        set_weekend2.update(weekend2_names)

        if all(name_counts[name] <= normalized_workers_dict[name] for name in name_counts):
            if set_weekend1.isdisjoint(set_weekend2):
                failed = False
                for name in name_counts:
                    if check_name_repetition(all_names, name, 3, 2, N_on_shift):
                        failed = True
                        break
                if not failed:
                    valid_combinations.append(combination)
                    if len(valid_combinations) >= 10:
                        return valid_combinations

    return valid_combinations
