# *****************************************************************************
# Author:           Mike Winebarger
# Date:             January 16, 2023,
# Description:      This file provides input validation for simple data types
# Input:            Various
# Output:           Various
# *****************************************************************************

def input_number(prompt="", error="", conversion=int, le=None, lt=None, ge=None, gt=None):
    """This function validates int and float data types"""

    while True:
        try:
            num = conversion(input(prompt))

            if le is not None and num > le:
                print(f"Value must be less than or equal to {le}")
                continue
            if lt is not None and num >= lt:
                print(f"Value must be less than {lt}")
                continue
            if ge is not None and num < ge:
                print(f"Value must be greater than or equal to {ge}")
                continue
            if gt is not None and num <= gt:
                print(f"Value must be greater than {gt}")
                continue

            return num

        except ValueError:
            print(error)


def input_int(prompt="Enter a whole number: ", error="That is not a whole number", **kwargs):
    return input_number(prompt=prompt, error=error, conversion=int, **kwargs)


# noinspection PyTypeChecker
def input_float(prompt="Enter a decimal number: ", error="That is not a decimal number", **kwargs):
    return input_number(prompt=prompt, error=error, conversion=float, **kwargs)


def input_string(prompt="Please enter a string: ", error="String must not be empty"):
    """This function ensures that input strings are not empty"""

    while True:
        s = str(input(prompt))

        if s:
            return s

        print(error)


def y_or_n(prompt="Yes or No: ", error="You must enter a variant of a yes or no answer"):
    """This function validates a 'yes or no' response"""

    no_list = ["n", "no"]
    yes_list = ["y", "yes"]

    while True:
        ans = str(input(prompt).lower())

        if ans in yes_list:
            return True

        if ans in no_list:
            return False

        print(error)


def password(prompt="\nEnter new password: ", error="\nPasswords must match and/or not be empty"):
    """This function validates a password input"""

    while True:
        passwd = str(input(prompt))
        verify = str(input("Re-enter new password: "))

        if passwd and passwd == verify:
            return passwd

        print(error)


def select_item(choices=None, conv=None, prompt="Please select an entry from the list of choices: ",
                error="That is not a valid selection"):
    """This function takes a list of choices and validates item selection"""

    if choices is None:
        choices = []
    if conv is None:
        conv = {}
    while True:
        for choice in choices:
            conv[choice.lower()] = choice

        choice_lower = input(prompt).lower()

        if choice_lower in conv:
            return conv[choice_lower]

        print(error)


def input_value(input_type, **kwargs):
    """This function facilitates a single function call for validating
     multiple data types"""

    match input_type:
        case "int":
            return input_int(**kwargs)
        case "float":
            return input_float(**kwargs)
        case "string":
            input_string(**kwargs)
        case "yorn":
            y_or_n(**kwargs)
        case _:
            print("That is not a valid choice")
