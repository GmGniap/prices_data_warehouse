from datetime import timedelta


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

def compare_two_dictionaries(first_dict : dict, second_dict : dict) -> bool:
    for key in first_dict.keys():
        if first_dict[key] != second_dict[key]:
            return False
    return True

