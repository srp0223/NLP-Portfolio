# Homework 1
# Supraj Punnam
# CS 4395.001
import pathlib
import pickle
import re
import sys


# Defines a Person class with input fields of last, first, mi, id, and phone
class Person:
    def __init__(self, last, first, mi, id, phone):
        self.last = last
        self.first = first
        self.mi = mi
        self.id = id
        self.phone = phone

    # Outputs the fields as shown in the examples
    def display(self):
        print('Employee id: ', self.id)
        print('\t', self.first, ' ', self.mi, ' ', self.last)
        print('\t', self.phone, '\n')


def process_lines(persons):
    while True:
        line = f.readline().strip()
        # Break if there is no line
        if not line:
            break
        # Split on the comma to get the input fields as separate variables
        temp_list = line.split(',')

        # Make last name and first name be capitalized
        temp_list[0] = temp_list[0].capitalize()
        temp_list[1] = temp_list[1].capitalize()

        # Use 'X' as a middle initial if one is missing or more than one letter
        if len(temp_list[2]) != 1:
            temp_list[2] = 'X'
        # Make the middle initial a capital letter
        temp_list[2] = temp_list[2].capitalize()

        # Modify id using regex if needed
        while re.match('[A-Za-z][A-Za-z]\d{4}', temp_list[3]) is None:
            print('ID invalid: ', temp_list[3])
            print('ID is two letters followed by 4 digits')
            temp_list[3] = input('Please enter a valid id: ')

        # Modify phone number using regex if needed
        while re.match('\w{3}-\w{3}-\w{4}', temp_list[4]) is None:
            print('Phone ', temp_list[4], ' is invalid')
            print('Enter phone number in form 123-456-7890')
            temp_list[4] = input('Enter phone number: ')

        # Create a Person object
        person = Person(temp_list[0], temp_list[1], temp_list[2], temp_list[3], temp_list[4])
        # Save the object to a dict of persons and have id as the key
        persons[temp_list[3]] = person

    # Return the dict of persons
    return persons


# Main Function
if __name__ == '__main__':
    # Check if the user has specified a sysarg
    if len(sys.argv) < 2:
        print('Please enter a filename as a system arg')
        quit()

    #  Read the file and remove the heading line
    f = open(pathlib.Path.cwd().joinpath(sys.argv[1]), 'r')
    line = f.readline()
    employees = {}
    employees = process_lines(employees)

    # pickles the employees
    pickle.dump(employees, open('employees.pickle', 'wb'))

    # reads the pickle back in
    employees_in = pickle.load(open('employees.pickle', 'rb'))

    # outputs the employees
    print('\n\nEmployee list:')

    for emp_id in employees_in.keys():
        employees_in[emp_id].display()
