import random
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def find_most_similar(base, samples):
    base_vector = np.array(list(base.values())).reshape(1, -1)
    similarities = []
    for sample in samples:
        sample_vector = np.array(list(sample.values())).reshape(1, -1)
        similarity = cosine_similarity(base_vector, sample_vector)[0][0]
        similarities.append(similarity)
    most_similar_index = np.argmax(similarities)
    return samples[most_similar_index], most_similar_index

def calculate_percentage_share(names_list):
    # Step 1: Count occurrences of each name
    name_counts = {}
    for pair in names_list:
        for name in pair:
            name_counts[name] = name_counts.get(name, 0) + 1

    # Step 2: Calculate total number of names
    total_names = sum(name_counts.values())

    # Step 3 & 4: Compute percentage share and store in dictionary
    percentage_share = {name: (count / total_names) for name, count in name_counts.items()}

    return percentage_share

def normalize_dict(input_dict):
    total = sum(input_dict.values())
    normalized_dict = {key: value / total for key, value in input_dict.items()}
    return normalized_dict



def sample_shifts(shift_workers_dict, all_combinations, sample_size=12, n = 1000, seed=42):
    """
    Ensure all workers are included in a random selection of shifts.

    Args:
    - shifts (dict): Dictionary containing shifts information.
    - all_workers (list): List of all workers' names.
    - N (int): Number of shifts to include in each set (default is 12).
    - seed (int): Seed for randomization (default is 555).

    Returns:
    - sample (list): List of N shifts ensuring all workers are included.
    """
    # Shuffle the keys of the shifts dictionary (Etter en for-løkke er skiftene sortert etter langvakter i dette tilfellet)
    random.seed(seed)  # for reproducibility
    shifts_keys = list(all_combinations.keys())
    random.shuffle(shifts_keys)

    N = sample_size
    # Sørg for at alle navnene er inkludert i skiftene
    list_of_samples = []
    while True:
        sample = (random.sample(shifts_keys, N))
        uniqe_names = []
        for shift in sample:
            for name in shift:
                if name in uniqe_names:
                    pass
                else:
                    uniqe_names.append(name)
        if set(uniqe_names) == set(shift_workers_dict.keys()):
            list_of_samples.append(sample)
            if len(list_of_samples) >= n:
                break
        else:
            pass

    base_dict = dict(sorted(normalize_dict(shift_workers_dict).items()))


    sample_dicts = []
    for names_list in list_of_samples:
        name_percentage_share_dict = dict(sorted(calculate_percentage_share(names_list).items()))
        sample_dicts.append(name_percentage_share_dict)

    most_similar_dict, most_similar_index = find_most_similar(base_dict, sample_dicts)

    return list_of_samples[most_similar_index]