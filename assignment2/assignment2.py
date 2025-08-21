import csv
import os
import custom_module

from datetime import datetime

# Task 2: Read a CSV File


def read_employees():
    data = {}  # to store the key/value pair
    rows = []  # to store the rows

    try:
        with open("csv/employees.csv", "r") as file:
            reader = csv.reader(file)
            for i, row in enumerate(reader):
                if i == 0:
                    data["fields"] = row
                else:
                    rows.append(row)
        data["rows"] = rows
    except Exception as e:
        print("Error:", e)

    return data


employees = read_employees()
print(employees)

# Task 3: Find the Column Index


def column_index(header):
    column_index = employees["fields"].index(header)
    return column_index


employee_id_column = column_index("employee_id")

# Task 4: Find the Employee First Name


def first_name(row):
    col = column_index("first_name")
    selected_row = employees["rows"][row]
    selected_row[col]

    return selected_row[col]


# Task 5: Find the Employee: a Function in a Function


def employee_find(employee_id):

    def employee_match(row):
        return int(row[employee_id_column]) == employee_id

    matches = list(filter(employee_match, employees["rows"]))

    return matches


# Task 6: Find the Employee with a Lambda


def employee_find_2(employee_id):
    matches = list(
        filter(
            lambda row: int(row[employee_id_column]) == employee_id, employees["rows"]
        )
    )
    return matches


# Task 7: Sort the Rows by last_name Using a Lambda


def sort_by_last_name():
    employees["rows"].sort(key=lambda row: row[column_index("last_name")])
    return employees["rows"]


sort_by_last_name()
print(employees)

# Task 8: Create a dict for an Employee


def employee_dict(row):

    # employee = {}
    # for i, key in enumerate(employees["fields"]):
    #     if key != "employee_id":
    #         employee[key] = row[i]
    # return employee

    employee_all_fields = zip(employees["fields"], row)
    employee = {k: v for k, v in employee_all_fields if k != "employee_id"}

    return employee


# Task 9: A dict of dicts, for All Employees


def all_employees_dict():
    all_employees = {}

    for row in employees["rows"]:
        employee_id = row[column_index("employee_id")]
        all_employees[employee_id] = employee_dict(row)

    return all_employees


print(all_employees_dict())

# Task 10: Use the os Module


def get_this_value():
    return os.getenv("THISVALUE")


# Task 11: Creating Your Own Module


def set_that_secret(secret):

    custom_module.set_secret(secret)


set_that_secret("Secret")
print(custom_module.secret)


# Task 12: Read minutes1.csv and minutes2.csv


def read_csv(path):
    with open(path, "r", newline="") as file:
        reader = csv.reader(file)
        fields = next(reader)
        rows = [tuple(row) for row in reader]
        return {"fields": fields, "rows": rows}


def read_minutes():

    minutes1 = read_csv("csv/minutes1.csv")
    minutes2 = read_csv("csv/minutes2.csv")

    return minutes1, minutes2


minutes1, minutes2 = read_minutes()

print("Minutes 1:", minutes1)
print("Minutes 2:", minutes2)


# Task 13: Create minutes_set
def create_minutes_set():

    set1 = set(minutes1["rows"])
    set2 = set(minutes2["rows"])

    return set1.union(set2)


minutes_set = create_minutes_set()
print("Minutes Set:", minutes_set)


# Task 14: Convert to datetime


def create_minutes_list():
    new_list = list(minutes_set)
    new_list = list(
        map(lambda x: (x[0], datetime.strptime(x[1], "%B %d, %Y")), new_list)
    )

    return new_list


minutes_list = create_minutes_list()
print("Minutes List: ", minutes_list)

# Task 15: Write Out Sorted List


def write_sorted_list():
    sorted_list = sorted(minutes_list, key=lambda x: x[1])

    converted_list = list(
        map(lambda x: (x[0], datetime.strftime(x[1], "%B %d, %Y")), sorted_list)
    )

    with open("./minutes.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(minutes1["fields"])
        writer.writerows(converted_list)

    return converted_list


write_sorted_list()
