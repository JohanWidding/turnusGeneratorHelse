import math
from collections import Counter
from multiprocessing import Pool
from tqdm import tqdm
from SampleEmployee import normalize_dict
from check_name_repetition import check_name_repetition

class CombinationValidator3:
    def __init__(self, combinations, N_on_shift, workers_dict, N_sample, num_days):
        self.combinations = combinations
        self.N_on_shift = N_on_shift
        self.workers_dict = workers_dict
        self.N_sample = N_sample
        self.num_days = num_days

    def f(self, combination, N_on_shift, normalized_workers_dict):
        combination, _, _ = combination  # Adjust unpacking to match the structure of the combination tuple

        all_names = [name for shift in combination for name in shift]
        name_counts = Counter(name for name in all_names)

        set_weekend1 = set(all_names[N_on_shift * 4:N_on_shift * 6])
        set_weekend2 = set(all_names[N_on_shift * 11:N_on_shift * 13])

        is_less_or_equal = all(name_counts[name] <= normalized_workers_dict[name] for name in name_counts)

        if is_less_or_equal:
            if set_weekend1.isdisjoint(set_weekend2):
                failed = False
                for name in name_counts.keys():
                    if check_name_repetition(all_names, name, 3, 2, N_on_shift):
                        failed = True
                        break

                if not failed:
                    return combination

    def validate_combinations(self):
        num_combinations = math.comb(self.N_sample + self.num_days - 1, self.num_days)
        normalized_workers_dict = Counter({key: math.ceil(((value*37.5) * (self.num_days/7))/12.5) for key, value in self.workers_dict.items()})
        print(normalized_workers_dict)
        valid_combinations = []

        pool = Pool(4)

        for combination in tqdm(self.combinations, total=num_combinations):
            # Apply async with the function and its arguments
            result = pool.apply_async(self.f, args=(combination, self.N_on_shift, normalized_workers_dict))
            # Get the result from the async call
            combination_result = result.get()
            if combination_result:
                valid_combinations.append(combination_result)

        return valid_combinations
