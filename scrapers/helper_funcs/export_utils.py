import csv
from datetime import date

def write_lstOfdicts_into_csv(input_lst_dicts:list, field_names: list):
    ouput_csv_name = f'export_{date.today().strftime("%d%m%y")}.csv'
    with open(ouput_csv_name, 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(input_lst_dicts)
