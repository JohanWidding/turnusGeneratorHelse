from itertools import groupby

def split_names(names, sublist_length):
    return [names[i:i+sublist_length] for i in range(0, len(names), sublist_length)]



def check_name_repetition(names_list, name, allowed_repetitions, min_rest_days, split):
    split_list = split_names(names_list, split)
    rest_count = min_rest_days

    for _, group in groupby(split_list, key=lambda x: name in x):
        if _:
            if rest_count < min_rest_days:
                if rest_count <= 0:
                    pass
                else:
                    return True
            rest_count = min_rest_days
            if len(list(group)) > allowed_repetitions:
                return True
        else:
            rest_count -= len(list(group))

    return False
