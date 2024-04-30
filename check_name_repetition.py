
def split_names(names, sublist_length):
    return [names[i:i+sublist_length] for i in range(0, len(names), sublist_length)]


def check_name_repetition(names_list, name, allowed_repetitions, min_rest_days, split):
    split_list = split_names(names_list, split)
    name_count = 0
    rest_count = min_rest_days

    for l in split_list:

        if name in l:
            if rest_count < min_rest_days:
                if rest_count <= 0:
                    pass
                else:
                    return True
            rest_count = min_rest_days
            name_count += 1
            if name_count > allowed_repetitions:
                return True
        else:
            name_count = 0
            rest_count -= 1

    # Return False if no consecutive occurrences of the same name were found
    return False